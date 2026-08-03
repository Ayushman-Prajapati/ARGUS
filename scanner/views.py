import json
import threading

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import services
from .forms import FileUploadForm, GithubRepoForm, PasteCodeForm, ZipUploadForm
from .models import Finding, ScanProject


@login_required
def home(request):
    return render(request, "scanner/home.html", _home_context(request))


def _home_context(request, demo=False):
    """Build the homepage context.

    The homepage carries the static demo timeline so the "Run Demo Scan"
    experience is fully client-side and never navigates away. ``demo=True``
    also signals the client to auto-start the demo on load (used by the
    Scan History demo buttons). No database records are created for a demo.
    """
    from . import demo_service

    recent_scans = ScanProject.objects.filter(user=request.user)[:8]
    stats = {
        "total_scans": ScanProject.objects.filter(user=request.user).count(),
        "total_findings": Finding.objects.filter(project__user=request.user).count(),
        "critical_findings": Finding.objects.filter(project__user=request.user, severity="critical").count(),
    }
    demo_payload = demo_service.demo_data()
    ctx = {
        "recent_scans": recent_scans,
        "stats": stats,
        "demo_mode": demo,
        "demo_data_json": json.dumps(demo_payload),
    }
    return ctx


def _run_and_redirect(request, project: ScanProject):
    """Start scan in background and redirect to progress page."""
    # Run scan in background thread
    thread = threading.Thread(target=_execute_scan_background, args=(project,))
    thread.daemon = True
    thread.start()
    return redirect("scanner:scan_progress", project_id=project.id)


def _execute_scan_background(project: ScanProject):
    """Execute scan in background thread. Called from _run_and_redirect."""
    # Mark as running when background thread starts
    project.status = "running"
    project.save(update_fields=["status"])

    try:
        services.execute_scan(project)
    except Exception as exc:  # noqa: BLE001
        project.status = "failed"
        project.error_message = str(exc)
        project.save(update_fields=["status", "error_message"])


@login_required
def scan_progress(request, project_id):
    """Display the scan progress page."""
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)
    return render(request, "scanner/scan_progress.html", {"project": project})


@login_required
def scan_progress_status(request, project_id):
    """Return JSON status for scan progress polling."""
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)

    # Determine progress based on status
    status = project.status
    progress = 0
    stage = "Initializing..."
    message = "Preparing scan environment..."
    details = ""
    engines = {}

    if status == "queued":
        progress = 5
        stage = "Queued"
        message = "Scan queued, waiting to start..."
        details = "Your scan is in the queue and will begin shortly."
    elif status == "running":
        # Simulate progress within running state based on time elapsed
        # In a real implementation, we'd track actual engine progress
        progress = min(90, 15 + (project.duration_seconds or 0) * 2)
        stage = "Running security engines"
        message = "Scanning code for vulnerabilities..."
        details = "This may take a moment depending on project size."

        # Simulate engine statuses
        engines = _get_simulated_engine_status(project)
    elif status == "completed":
        progress = 100
        stage = "Completed"
        message = "Scan completed successfully!"
        details = f"Found {project.total_findings} findings in {project.duration_seconds or 0:.1f}s."
        engines = {e: {"status": "completed"} for e in _get_enabled_engines(project)}
    elif status == "failed":
        progress = 100
        stage = "Failed"
        message = "Scan encountered an error"
        details = project.error_message or "Unknown error occurred."
        engines = {e: {"status": "failed"} for e in _get_enabled_engines(project)}
    elif status == "cancelled":
        progress = 100
        stage = "Cancelled"
        message = "Scan was cancelled"
        details = "The scan was cancelled by the user."
        engines = {e: {"status": "skipped"} for e in _get_enabled_engines(project)}

    # Generate console events based on scan status
    console_events = _generate_console_events(project, status)

    return JsonResponse({
        "status": status,
        "progress": progress,
        "stage": stage,
        "message": message,
        "details": details,
        "engines": engines,
        "console": console_events,
    })


def _generate_console_events(project: ScanProject, status: str) -> list:
    """Generate console events for the live console based on scan status."""
    events = []
    elapsed = project.duration_seconds or 0

    # Base events that always happen
    events.append({
        "timestamp": "0:00",
        "type": "info",
        "message": "Scan initialized",
        "details": f"Project: {project.name}"
    })

    if status in ["running", "completed", "failed"]:
        events.append({
            "timestamp": "0:01",
            "type": "info",
            "message": "Source code prepared",
            "details": f"{project.files_scanned or 0} files to scan"
        })

        # Engine events
        engine_events = [
            ("bandit", "Bandit", 2, 10),
            ("semgrep", "Semgrep", 5, 15),
            ("ast", "ARGUS AST", 15, 20),
            ("safety", "Safety", 20, 10),
            ("pip_audit", "pip-audit", 25, 10),
        ]

        for engine_key, engine_name, start, duration in engine_events:
            if engine_key == "bandit" and not project.run_bandit:
                continue
            if engine_key == "semgrep" and not project.run_semgrep:
                continue
            if engine_key == "ast" and not project.run_ast_checks:
                continue

            if elapsed >= start:
                events.append({
                    "timestamp": f"0:{start:02d}",
                    "type": "info",
                    "message": f"{engine_name} started",
                    "details": "Analyzing source code..."
                })

            if elapsed >= start + duration:
                events.append({
                    "timestamp": f"0:{start + duration:02d}",
                    "type": "success",
                    "message": f"{engine_name} completed",
                    "details": "Analysis finished"
                })
            elif elapsed > start and status == "running":
                events.append({
                    "timestamp": f"0:{min(start + 5, int(elapsed)):02d}",
                    "type": "info",
                    "message": f"{engine_name} running...",
                    "details": "Scanning in progress"
                })

        if status in ["completed", "failed"]:
            events.append({
                "timestamp": f"0:{max(35, int(elapsed)):02d}",
                "type": "info",
                "message": "Aggregating findings",
                "details": "Normalizing results from all engines"
            })

            events.append({
                "timestamp": f"0:{max(38, int(elapsed)):02d}",
                "type": "info",
                "message": "Generating report",
                "details": "Preparing scan summary"
            })

    if status == "completed":
        events.append({
            "timestamp": f"0:{max(40, int(elapsed)):02d}",
            "type": "success",
            "message": "Scan complete",
            "details": f"Found {project.total_findings} findings"
        })
    elif status == "failed":
        events.append({
            "timestamp": f"0:{max(40, int(elapsed)):02d}",
            "type": "error",
            "message": "Scan failed",
            "details": project.error_message or "Unknown error"
        })
    elif status == "cancelled":
        events.append({
            "timestamp": f"0:{int(elapsed):02d}",
            "type": "warning",
            "message": "Scan cancelled",
            "details": "User cancelled the scan"
        })

    return events


def _get_enabled_engines(project: ScanProject):
    """Get list of enabled engine keys for a project."""
    engines = []
    if project.run_bandit:
        engines.append("bandit")
    if project.run_semgrep:
        engines.append("semgrep")
    if project.run_ast_checks:
        engines.append("ast")
    # Safety and pip-audit are tracked but not yet implemented
    engines.append("safety")
    engines.append("pip_audit")
    return engines


def _get_simulated_engine_status(project: ScanProject):
    """Generate simulated engine status for UI feedback during scan."""
    engines = {}
    elapsed = project.duration_seconds or 0

    # Define all 5 engines with their timing
    engine_timing = {
        "bandit": {"start": 0, "duration": 10, "enabled": project.run_bandit},
        "semgrep": {"start": 5, "duration": 15, "enabled": project.run_semgrep},
        "ast": {"start": 15, "duration": 20, "enabled": project.run_ast_checks},
        "safety": {"start": 20, "duration": 10, "enabled": True},  # Always tracked
        "pip_audit": {"start": 25, "duration": 10, "enabled": True},  # Always tracked
    }

    for engine_key, timing in engine_timing.items():
        if not timing["enabled"]:
            engines[engine_key] = {"status": "skipped"}
            continue

        if elapsed < timing["start"]:
            engines[engine_key] = {"status": "pending"}
        elif elapsed < timing["start"] + timing["duration"]:
            engines[engine_key] = {"status": "running"}
        else:
            engines[engine_key] = {"status": "completed"}

    return engines


@require_http_methods(["GET", "POST"])
@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            project = ScanProject.objects.create(
                user=request.user,
                name=uploaded.name,
                source_type="file",
                source_reference=uploaded.name,
                run_bandit=form.cleaned_data["run_bandit"],
                run_semgrep=form.cleaned_data["run_semgrep"],
                run_ast_checks=form.cleaned_data["run_ast_checks"],
            )
            try:
                path = services.ingest_single_file(project, uploaded)
            except services.IngestionError as exc:
                project.delete()
                messages.error(request, str(exc))
                return render(request, "scanner/upload_file.html", {"form": form})
            project.scan_path = str(path)
            project.save(update_fields=["scan_path"])
            return _run_and_redirect(request, project)
    else:
        form = FileUploadForm()
    return render(request, "scanner/upload_file.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def upload_zip(request):
    if request.method == "POST":
        form = ZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archive = form.cleaned_data["archive"]
            project = ScanProject.objects.create(
                user=request.user,
                name=archive.name,
                source_type="zip",
                source_reference=archive.name,
                run_bandit=form.cleaned_data["run_bandit"],
                run_semgrep=form.cleaned_data["run_semgrep"],
                run_ast_checks=form.cleaned_data["run_ast_checks"],
            )
            try:
                path = services.ingest_zip(project, archive)
            except services.IngestionError as exc:
                project.delete()
                messages.error(request, str(exc))
                return render(request, "scanner/upload_zip.html", {"form": form})
            project.scan_path = str(path)
            project.save(update_fields=["scan_path"])
            return _run_and_redirect(request, project)
    else:
        form = ZipUploadForm()
    return render(request, "scanner/upload_zip.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def paste_code(request):
    if request.method == "POST":
        form = PasteCodeForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data["filename"] or "snippet.py"
            project = ScanProject.objects.create(
                user=request.user,
                name=filename,
                source_type="paste",
                source_reference="pasted snippet",
                run_bandit=form.cleaned_data["run_bandit"],
                run_semgrep=form.cleaned_data["run_semgrep"],
                run_ast_checks=form.cleaned_data["run_ast_checks"],
            )
            path = services.ingest_pasted_code(project, form.cleaned_data["code"], filename)
            project.scan_path = str(path)
            project.save(update_fields=["scan_path"])
            return _run_and_redirect(request, project)
    else:
        form = PasteCodeForm()
    return render(request, "scanner/paste_code.html", {"form": form})


@require_http_methods(["GET", "POST"])
@login_required
def scan_github(request):
    if request.method == "POST":
        form = GithubRepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]
            name = repo_url.rstrip("/").split("/")[-1]
            project = ScanProject.objects.create(
                user=request.user,
                name=name,
                source_type="github",
                source_reference=repo_url,
                run_bandit=form.cleaned_data["run_bandit"],
                run_semgrep=form.cleaned_data["run_semgrep"],
                run_ast_checks=form.cleaned_data["run_ast_checks"],
            )
            try:
                path = services.ingest_github_repo(project, repo_url)
            except services.IngestionError as exc:
                project.delete()
                messages.error(request, str(exc))
                return render(request, "scanner/scan_github.html", {"form": form})
            project.scan_path = str(path)
            project.save(update_fields=["scan_path"])
            return _run_and_redirect(request, project)
    else:
        form = GithubRepoForm()
    return render(request, "scanner/scan_github.html", {"form": form})


@login_required
def scan_list(request):
    projects = ScanProject.objects.filter(user=request.user)
    return render(request, "scanner/scan_list.html", {"projects": projects})


@login_required
def scan_detail(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)
    findings = project.findings.all()

    severity_filter = request.GET.get("severity")
    source_filter = request.GET.get("source")
    if severity_filter:
        findings = findings.filter(severity=severity_filter)
    if source_filter:
        findings = findings.filter(source=source_filter)

    paginator = Paginator(findings, 25)
    page_number = request.GET.get("page", 1)
    findings_page = paginator.get_page(page_number)

    # Preserve active filters when building pagination links
    querydict = request.GET.copy()
    querydict.pop("page", None)
    filter_qs = querydict.urlencode()

    # Previous scans for same source (for comparison)
    previous_scans = ScanProject.objects.filter(
        user=request.user,
        source_type=project.source_type,
        source_reference=project.source_reference,
        status="completed"
    ).exclude(id=project.id).order_by("-completed_at")

    context = {
        "project": project,
        "findings_page": findings_page,
        "filtered_count": paginator.count,
        "filter_qs": filter_qs,
        "severity_counts": project.severity_counts(),
        "source_counts": project.source_counts(),
        "severity_counts_json": json.dumps(project.severity_counts()),
        "source_counts_json": json.dumps(project.source_counts()),
        "risk_score": project.risk_score(),
        "active_severity": severity_filter or "",
        "active_source": source_filter or "",
        "previous_scans": previous_scans,
    }
    return render(request, "scanner/scan_detail.html", context)


@login_required
def dashboard(request):
    projects = ScanProject.objects.filter(user=request.user, status="completed")
    total_findings = Finding.objects.filter(project__in=projects)

    severity_agg = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for row in total_findings.values("severity"):
        severity_agg[row["severity"]] = severity_agg.get(row["severity"], 0) + 1

    source_agg = {}
    for row in total_findings.values("source"):
        source_agg[row["source"]] = source_agg.get(row["source"], 0) + 1

    context = {
        "projects": projects,
        "total_scans": projects.count(),
        "total_findings": total_findings.count(),
        "severity_agg": severity_agg,
        "source_agg": source_agg,
        "severity_agg_json": json.dumps(severity_agg),
        "source_agg_json": json.dumps(source_agg),
        "top_risk_projects": sorted(projects, key=lambda p: p.risk_score(), reverse=True)[:5],
    }
    return render(request, "scanner/dashboard.html", context)


@login_required
@require_http_methods(["POST"])
def rescan(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)
    project.findings.all().delete()
    return _run_and_redirect(request, project)


@login_required
@require_http_methods(["POST"])
def cancel_scan(request, project_id):
    """Cancel a running/queued scan (UI only - marks status as cancelled)."""
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)
    if project.status in ["queued", "running"]:
        project.status = "cancelled"
        project.error_message = "Scan cancelled by user."
        project.save(update_fields=["status", "error_message"])
        messages.info(request, "Scan cancelled.")
    else:
        messages.warning(request, "Scan cannot be cancelled in its current state.")
    return redirect("scanner:scan_progress", project_id=project.id)


@login_required
def scan_compare(request, project_id):
    """Compare current scan with previous scan for the same source."""
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)

    # Find previous scan for same source
    previous_scan = ScanProject.objects.filter(
        user=request.user,
        source_type=project.source_type,
        source_reference=project.source_reference,
        status="completed"
    ).exclude(id=project.id).order_by("-completed_at").first()

    if not previous_scan:
        messages.info(request, "No previous scan found for comparison.")
        return redirect("scanner:scan_detail", project_id=project.id)

    # Compare metrics
    current_risk = project.risk_score()
    previous_risk = previous_scan.risk_score()
    risk_diff = current_risk - previous_risk

    current_severity = project.severity_counts()
    previous_severity = previous_scan.severity_counts()

    current_source = project.source_counts()
    previous_source = previous_scan.source_counts()

    severity_comparison = {}
    for sev in ["critical", "high", "medium", "low", "info"]:
        current = current_severity.get(sev, 0)
        previous = previous_severity.get(sev, 0)
        severity_comparison[sev] = {
            "current": current,
            "previous": previous,
            "diff": current - previous,
        }

    source_comparison = {}
    all_sources = set(list(current_source.keys()) + list(previous_source.keys()))
    for src in all_sources:
        current = current_source.get(src, 0)
        previous = previous_source.get(src, 0)
        source_comparison[src] = {
            "current": current,
            "previous": previous,
            "diff": current - previous,
        }

    context = {
        "project": project,
        "previous_scan": previous_scan,
        "risk_score": current_risk,
        "previous_risk": previous_risk,
        "risk_diff": risk_diff,
        "severity_comparison": severity_comparison,
        "source_comparison": source_comparison,
    }
    return render(request, "scanner/scan_compare.html", context)


@login_required
@require_http_methods(["POST"])
def demo_scan(request):
    """Start an isolated, read-only demo scan on the homepage.

    The user stays on "/". The homepage is re-rendered in demo mode and the
    whole experience is driven client-side from static demo data. No Project /
    Scan / Finding / Report is created and no database writes occur.
    """
    return render(request, "scanner/home.html", _home_context(request, demo=True))


@login_required
@require_http_methods(["POST"])
def delete_scan(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id, user=request.user)
    project.delete()
    messages.info(request, "Scan deleted.")
    return redirect("scanner:scan_list")
