from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from scanner.models import ScanProject

from .models import GeneratedReport
from .pdf_generator import generate_report_pdf


@require_http_methods(["POST", "GET"])
def generate_report(request, project_id):
    project = get_object_or_404(ScanProject, id=project_id)
    include_appendix = request.GET.get("appendix", "1") != "0"

    pdf_path = generate_report_pdf(project, include_technical_appendix=include_appendix)
    relative_path = f"pdf_reports/{pdf_path.name}"
    report = GeneratedReport.objects.create(
        project=project,
        file=relative_path,
        include_technical_appendix=include_appendix,
    )
    return redirect("reports:download_report", report_id=report.id)


def download_report(request, report_id):
    report = get_object_or_404(GeneratedReport, id=report_id)
    if not report.file or not report.file.storage.exists(report.file.name):
        raise Http404("Report file not found.")
    return FileResponse(
        report.file.open("rb"),
        as_attachment=True,
        filename=f"ARGUS_Report_{report.project.name}_{report.id}.pdf",
    )
