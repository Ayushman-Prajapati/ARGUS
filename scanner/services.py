"""
ARGUS scan orchestration service.

Handles turning an uploaded file / zip / pasted snippet / GitHub URL into a
directory of code on disk, then runs the Bandit, Semgrep, and ARGUS AST
engines against it and persists normalized Finding rows.
"""
import shutil
import time
import zipfile
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from .engines.ast_engine import scan_source
from .engines.bandit_engine import run_bandit
from .engines.semgrep_engine import run_semgrep
from .models import Finding, ScanProject

PYTHON_EXTENSIONS = {".py", ".pyw"}
SCANNABLE_TEXT_EXTENSIONS = {
    ".py", ".pyw", ".js", ".jsx", ".ts", ".tsx", ".html", ".yaml", ".yml", ".json",
}


class IngestionError(Exception):
    pass


def _project_dir(project: ScanProject) -> Path:
    return Path(settings.ARGUS_UPLOAD_DIR) / str(project.id)


def ingest_single_file(project: ScanProject, uploaded_file) -> Path:
    target_dir = _project_dir(project)
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / uploaded_file.name
    with open(dest, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    return target_dir


def ingest_zip(project: ScanProject, uploaded_file) -> Path:
    if uploaded_file.size > settings.ARGUS_MAX_ZIP_SIZE:
        raise IngestionError(
            f"Archive exceeds max size of {settings.ARGUS_MAX_ZIP_SIZE // (1024*1024)}MB."
        )
    target_dir = _project_dir(project)
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_path = target_dir / "upload.zip"
    with open(zip_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    try:
        with zipfile.ZipFile(zip_path) as zf:
            _safe_extract(zf, target_dir)
    except zipfile.BadZipFile:
        raise IngestionError("Uploaded file is not a valid .zip archive.")
    finally:
        zip_path.unlink(missing_ok=True)
    return target_dir


def _safe_extract(zf: zipfile.ZipFile, target_dir: Path):
    """Extract while guarding against zip-slip path traversal."""
    target_dir_resolved = target_dir.resolve()
    for member in zf.infolist():
        member_path = (target_dir / member.filename).resolve()
        if not str(member_path).startswith(str(target_dir_resolved)):
            raise IngestionError(f"Unsafe path in archive: {member.filename}")
    zf.extractall(target_dir)


def ingest_pasted_code(project: ScanProject, code: str, filename: str = "snippet.py") -> Path:
    target_dir = _project_dir(project)
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_name = filename.strip() or "snippet.py"
    if not safe_name.endswith(".py"):
        safe_name += ".py"
    dest = target_dir / safe_name
    dest.write_text(code, encoding="utf-8")
    return target_dir


def ingest_github_repo(project: ScanProject, repo_url: str, timeout: int = 120) -> Path:
    try:
        import git
    except ImportError:
        raise IngestionError("GitPython is not installed. Install it with `pip install GitPython`.")

    target_dir = _project_dir(project)
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        git.Repo.clone_from(repo_url, target_dir, depth=1)
    except Exception as exc:  # noqa: BLE001 - surface any clone failure to the user
        raise IngestionError(f"Could not clone repository: {exc}")

    git_dir = target_dir / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir, ignore_errors=True)

    return target_dir


def _iter_python_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in PYTHON_EXTENSIONS:
            if any(part in {"venv", ".venv", "node_modules", "__pycache__", "site-packages"}
                   for part in path.parts):
                continue
            yield path


def run_ast_engine(project: ScanProject, root: Path) -> list[dict]:
    findings = []
    for path in _iter_python_files(root):
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel_path = str(path.relative_to(root))
        file_findings = scan_source(rel_path, source)
        findings.extend(file_findings)
    return findings


def _relativize(findings: list[dict], root: Path) -> list[dict]:
    root_str = str(root)
    for f in findings:
        fp = f.get("file_path", "")
        if fp.startswith(root_str):
            f["file_path"] = str(Path(fp).relative_to(root))
    return findings


def execute_scan(project: ScanProject) -> None:
    """Run all enabled engines against project.scan_path and persist findings."""
    root = Path(project.scan_path)
    project.status = "running"
    project.save(update_fields=["status"])

    start = time.monotonic()
    errors = []
    all_findings: list[dict] = []

    try:
        if project.run_bandit:
            findings, err = run_bandit(str(root), timeout=settings.ARGUS_SCAN_TIMEOUT)
            if err:
                errors.append(f"Bandit: {err}")
            all_findings.extend(_relativize(
                [dict(f, source="bandit") for f in findings], root
            ))

        if project.run_semgrep:
            findings, err = run_semgrep(str(root), timeout=settings.ARGUS_SCAN_TIMEOUT)
            if err:
                errors.append(f"Semgrep: {err}")
            all_findings.extend(_relativize(
                [dict(f, source="semgrep") for f in findings], root
            ))

        if project.run_ast_checks:
            ast_findings = run_ast_engine(project, root)
            all_findings.extend([dict(f, source="ast") for f in ast_findings])

        finding_objs = [
            Finding(
                project=project,
                source=f.get("source", "ast"),
                rule_id=f.get("rule_id", ""),
                title=f.get("title", "")[:500],
                description=f.get("description", ""),
                severity=f.get("severity", "medium"),
                confidence=f.get("confidence", "") or "",
                file_path=f.get("file_path", ""),
                line_number=f.get("line_number") or 0,
                end_line_number=f.get("end_line_number"),
                code_snippet=(f.get("code_snippet") or "")[:4000],
                cwe_id=f.get("cwe_id", "") or "",
                owasp_category=f.get("owasp_category", "") or "",
                remediation=f.get("remediation", "") or "",
            )
            for f in all_findings
        ]
        Finding.objects.bulk_create(finding_objs)

        project.files_scanned = sum(1 for _ in _iter_python_files(root))
        project.status = "failed" if (errors and not all_findings and not project.files_scanned) else "completed"
        project.error_message = "\n".join(errors)

    except Exception as exc:  # noqa: BLE001
        project.status = "failed"
        project.error_message = str(exc)

    project.duration_seconds = round(time.monotonic() - start, 2)
    project.completed_at = timezone.now()
    project.save(update_fields=[
        "status", "error_message", "files_scanned", "duration_seconds", "completed_at"
    ])


def run_demo_scan(project: ScanProject) -> None:
    """Run a fast demo scan with predefined findings for demonstration."""
    project.status = "running"
    project.save(update_fields=["status"])

    start = time.monotonic()

    # Predefined demo findings that simulate a real scan
    demo_findings = [
        {
            "source": "bandit",
            "rule_id": "B602",
            "title": "Subprocess with shell=True",
            "description": "Using shell=True with subprocess calls can lead to command injection vulnerabilities if user input is not properly sanitized.",
            "severity": "high",
            "confidence": "HIGH",
            "file_path": "demo_app/utils.py",
            "line_number": 42,
            "end_line_number": 42,
            "code_snippet": "result = subprocess.run(user_input, shell=True, capture_output=True)",
            "cwe_id": "CWE-78",
            "owasp_category": "A03:2021 - Injection",
            "remediation": "Avoid shell=True. Use subprocess.run() with a list of arguments instead."
        },
        {
            "source": "bandit",
            "rule_id": "B311",
            "title": "Use of weak cryptographic hash (MD5)",
            "description": "MD5 is cryptographically broken and should not be used for security-sensitive operations.",
            "severity": "medium",
            "confidence": "HIGH",
            "file_path": "demo_app/auth.py",
            "line_number": 18,
            "end_line_number": 18,
            "code_snippet": "password_hash = hashlib.md5(password.encode()).hexdigest()",
            "cwe_id": "CWE-327",
            "owasp_category": "A02:2021 - Cryptographic Failures",
            "remediation": "Use SHA-256 or stronger (e.g., hashlib.sha256) for password hashing. Consider using bcrypt or Argon2."
        },
        {
            "source": "semgrep",
            "rule_id": "django-raw-sql",
            "title": "Potential SQL Injection via raw()",
            "description": "Using raw SQL with string formatting can lead to SQL injection. Use parameterized queries instead.",
            "severity": "critical",
            "confidence": "MEDIUM",
            "file_path": "demo_app/views.py",
            "line_number": 56,
            "end_line_number": 56,
            "code_snippet": "User.objects.raw(f\"SELECT * FROM users WHERE name = '{username}'\")",
            "cwe_id": "CWE-89",
            "owasp_category": "A03:2021 - Injection",
            "remediation": "Use Django ORM or parameterized queries: User.objects.raw('SELECT * FROM users WHERE name = %s', [username])"
        },
        {
            "source": "semgrep",
            "rule_id": "django-xss-template",
            "title": "Potential XSS in template",
            "description": "Using safe filter or unescaped variables in templates can lead to cross-site scripting.",
            "severity": "high",
            "confidence": "MEDIUM",
            "file_path": "demo_app/templates/user_profile.html",
            "line_number": 23,
            "end_line_number": 23,
            "code_snippet": "<div>{{ user.bio|safe }}</div>",
            "cwe_id": "CWE-79",
            "owasp_category": "A03:2021 - Injection",
            "remediation": "Remove the |safe filter or ensure content is properly sanitized before rendering."
        },
        {
            "source": "ast",
            "rule_id": "hardcoded-secret",
            "title": "Hardcoded API key detected",
            "description": "An API key or secret appears to be hardcoded in source code.",
            "severity": "critical",
            "confidence": "HIGH",
            "file_path": "demo_app/config.py",
            "line_number": 7,
            "end_line_number": 7,
            "code_snippet": "API_KEY = \"sk_live_51H7x8J2K9LmN3oP4qR5sT6uV7wX8yZ9\"",
            "cwe_id": "CWE-798",
            "owasp_category": "A07:2021 - Identification and Authentication Failures",
            "remediation": "Move secrets to environment variables or a secure vault. Use django-environ or similar."
        },
        {
            "source": "ast",
            "rule_id": "sql-injection",
            "title": "SQL Injection via string formatting",
            "description": "SQL query built via string formatting with user input.",
            "severity": "high",
            "confidence": "HIGH",
            "file_path": "demo_app/reports.py",
            "line_number": 34,
            "end_line_number": 34,
            "code_snippet": "cursor.execute(f\"SELECT * FROM reports WHERE id = {report_id}\")",
            "cwe_id": "CWE-89",
            "owasp_category": "A03:2021 - Injection",
            "remediation": "Use parameterized queries: cursor.execute('SELECT * FROM reports WHERE id = %s', [report_id])"
        },
        {
            "source": "ast",
            "rule_id": "command-injection",
            "title": "Command injection in os.system",
            "description": "User input passed directly to os.system() without validation.",
            "severity": "critical",
            "confidence": "HIGH",
            "file_path": "demo_app/tools.py",
            "line_number": 12,
            "end_line_number": 12,
            "code_snippet": "os.system(f\"ping -c 4 {user_host}\")",
            "cwe_id": "CWE-78",
            "owasp_category": "A03:2021 - Injection",
            "remediation": "Use subprocess.run() with list arguments and validate/sanitize input."
        },
        {
            "source": "ast",
            "rule_id": "weak-crypto",
            "title": "Use of deprecated crypto algorithm (DES)",
            "description": "DES is cryptographically weak and should not be used.",
            "severity": "medium",
            "confidence": "HIGH",
            "file_path": "demo_app/crypto.py",
            "line_number": 8,
            "end_line_number": 8,
            "code_snippet": "cipher = DES.new(key, DES.MODE_ECB)",
            "cwe_id": "CWE-327",
            "owasp_category": "A02:2021 - Cryptographic Failures",
            "remediation": "Use AES with GCM mode or ChaCha20-Poly1305 instead."
        },
        {
            "source": "ast",
            "rule_id": "unsafe-deserialization",
            "title": "Unsafe deserialization with pickle",
            "description": "Pickle can execute arbitrary code during deserialization. Use JSON instead.",
            "severity": "high",
            "confidence": "MEDIUM",
            "file_path": "demo_app/cache.py",
            "line_number": 15,
            "end_line_number": 15,
            "code_snippet": "data = pickle.loads(user_supplied_data)",
            "cwe_id": "CWE-502",
            "owasp_category": "A08:2021 - Software and Data Integrity Failures",
            "remediation": "Use json.loads() or a safe serialization format. Never unpickle untrusted data."
        }
    ]

    # Create finding objects
    finding_objs = [
        Finding(
            project=project,
            source=f["source"],
            rule_id=f["rule_id"],
            title=f["title"][:500],
            description=f["description"],
            severity=f["severity"],
            confidence=f["confidence"],
            file_path=f["file_path"],
            line_number=f["line_number"],
            end_line_number=f["end_line_number"],
            code_snippet=f["code_snippet"][:4000],
            cwe_id=f["cwe_id"],
            owasp_category=f["owasp_category"],
            remediation=f["remediation"],
        )
        for f in demo_findings
    ]

    Finding.objects.bulk_create(finding_objs)

    project.files_scanned = 8
    project.status = "completed"
    project.error_message = ""
    project.duration_seconds = round(time.monotonic() - start, 2)
    project.completed_at = timezone.now()
    project.save(update_fields=[
        "status", "error_message", "files_scanned", "duration_seconds", "completed_at"
    ])
