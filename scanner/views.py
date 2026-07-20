import json

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from . import services
from .forms import FileUploadForm, GithubRepoForm, PasteCodeForm, ZipUploadForm
from .models import Finding, ScanProject


def home(request):
    recent_scans = ScanProject.objects.all()[:8]
    stats = {
        "total_scans": ScanProject.objects.count(),
        "total_findings": Finding.objects.count(),
        "critical_findings": Finding.objects.filter(severity="critical").count(),
    }
    return render(request, "scanner/home.html", {"recent_scans": recent_scans, "stats": stats})


def _run_and_redirect(request, project: ScanProject):
    try:
        services.execute_scan(project)
    except Exception as exc:  # noqa: BLE001
        project.status = "failed"
        project.error_message = str(exc)
        project.save(update_fields=["status", "error_message"])
        messages.error(request, f"Scan failed: {exc}")
    else:
        if project.status == "completed":
            messages.success(request, f"Scan complete: {project.total_findings} findings.")
        else:
            messages.warning(request, "Scan finished with issues. See details below.")
    return redirect("scanner:scan_detail", project_id=project.id)


@require_http_methods(["GET", "POST"])
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            project = ScanProject.objects.create(
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
def upload_zip(request):
    if request.method == "POST":
        form = ZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archive = form.cleaned_data["archive"]
            project = ScanProject.objects.create(
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
def paste_code(request):
    if request.method == "POST":
        form = PasteCodeForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data["filename"] or "snippet.py"
            project = ScanProject.objects.create(
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
def scan_github(request):
    if request.method == "POST":
        form = GithubRepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]
            name = repo_url.rstrip("/").split("/")[-1]
            project = ScanProject.objects.create(
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


def scan_list(request):
    projects = ScanProject.objects.all()
    return render(request, "scanner/scan_list.html", {"projects": projects})


def scan_detail(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id)
    findings = project.findings.all()

    severity_filter = request.GET.get("severity")
    source_filter = request.GET.get("source")
    if severity_filter:
        findings = findings.filter(severity=severity_filter)
    if source_filter:
        findings = findings.filter(source=source_filter)

    context = {
        "project": project,
        "findings": findings,
        "severity_counts": project.severity_counts(),
        "source_counts": project.source_counts(),
        "severity_counts_json": json.dumps(project.severity_counts()),
        "source_counts_json": json.dumps(project.source_counts()),
        "risk_score": project.risk_score(),
        "active_severity": severity_filter or "",
        "active_source": source_filter or "",
    }
    return render(request, "scanner/scan_detail.html", context)


def dashboard(request):
    projects = ScanProject.objects.filter(status="completed")
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


@require_http_methods(["POST"])
def rescan(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id)
    project.findings.all().delete()
    return _run_and_redirect(request, project)


@require_http_methods(["POST"])
def delete_scan(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id)
    project.delete()
    messages.info(request, "Scan deleted.")
    return redirect("scanner:scan_list")
