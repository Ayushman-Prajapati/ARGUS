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
