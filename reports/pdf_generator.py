"""
ARGUS PDF Report Generator (ReportLab)

Builds a two-part report:
  1. Executive summary - risk score, severity/engine charts, top findings table.
  2. Technical appendix  - every finding with description, code snippet, and
     remediation guidance, grouped by file.

Usage:
    from reports.pdf_generator import generate_report_pdf
    report_path = generate_report_pdf(project, include_technical_appendix=True)
"""
import uuid
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .chart_generator import risk_gauge_chart, severity_bar_chart, source_pie_chart

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]

SEVERITY_COLOR_HEX = {
    "critical": colors.HexColor("#dc3545"),
    "high": colors.HexColor("#fd7e14"),
    "medium": colors.HexColor("#0dcaf0"),
    "low": colors.HexColor("#6c757d"),
    "info": colors.HexColor("#adb5bd"),
}

BRAND_NAVY = colors.HexColor("#0b1f3a")
BRAND_ACCENT = colors.HexColor("#2563eb")


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(
        name="ArgusTitle", fontSize=26, leading=30, textColor=BRAND_NAVY,
        fontName="Helvetica-Bold", spaceAfter=6,
    ))
    ss.add(ParagraphStyle(
        name="ArgusSubtitle", fontSize=13, leading=16, textColor=colors.HexColor("#495057"),
        fontName="Helvetica", spaceAfter=20,
    ))
    ss.add(ParagraphStyle(
        name="ArgusH2", fontSize=15, leading=18, textColor=BRAND_NAVY,
        fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=8,
    ))
    ss.add(ParagraphStyle(
        name="ArgusH3", fontSize=11.5, leading=14, textColor=BRAND_ACCENT,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4,
    ))
    ss.add(ParagraphStyle(
        name="ArgusBody", fontSize=9.5, leading=13.5, textColor=colors.HexColor("#212529"),
    ))
    ss.add(ParagraphStyle(
        name="ArgusMono", fontName="Courier", fontSize=8, leading=10.5,
        backColor=colors.HexColor("#f1f3f5"), textColor=colors.HexColor("#212529"),
        borderPadding=6,
    ))
    ss.add(ParagraphStyle(
        name="ArgusCenter", parent=ss["ArgusBody"], alignment=TA_CENTER,
    ))
    return ss


def _cover_page(story, project, styles):
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("ARGUS", ParagraphStyle(
        name="Logo", fontSize=42, fontName="Helvetica-Bold", textColor=BRAND_NAVY,
        alignment=TA_CENTER,
    )))
    story.append(Paragraph("SECURE CODE REVIEW PLATFORM", ParagraphStyle(
        name="LogoSub", fontSize=12, fontName="Helvetica", textColor=BRAND_ACCENT,
        alignment=TA_CENTER, spaceAfter=40, characterSpacing=2,
    )))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("Security Scan Report", styles["ArgusTitle"]))
    story.append(Paragraph(project.name, ParagraphStyle(
        name="ProjName", fontSize=16, textColor=colors.HexColor("#212529"),
        fontName="Helvetica-Bold", spaceAfter=4,
    )))
    story.append(Paragraph(
        f"Source: {project.get_source_type_display()} &middot; "
        f"Generated: {timezone.now():%B %d, %Y at %H:%M UTC}",
        styles["ArgusSubtitle"],
    ))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#dee2e6"), thickness=1))
    story.append(PageBreak())


def _executive_summary(story, project, styles):
    story.append(Paragraph("Executive Summary", styles["ArgusH2"]))

    severity_counts = project.severity_counts()
    source_counts = project.source_counts()
    risk_score = project.risk_score()
    total = project.total_findings

    risk_label = "Critical Risk" if risk_score >= 70 else "Elevated Risk" if risk_score >= 40 else \
        "Moderate Risk" if risk_score >= 15 else "Low Risk"

    summary_text = (
        f"This report covers a static security analysis of <b>{project.name}</b> "
        f"performed by ARGUS using Bandit, Semgrep, and the ARGUS AST engine. "
        f"The scan analyzed {project.files_scanned} file(s) and identified "
        f"<b>{total} finding(s)</b> in {project.duration_seconds or 0:.1f} seconds. "
        f"The overall risk posture is assessed as <b>{risk_label}</b> "
        f"(score {risk_score}/100)."
    )
    story.append(Paragraph(summary_text, styles["ArgusBody"]))
    story.append(Spacer(1, 12))

    # Charts row: risk gauge + severity bar
    risk_img_path = risk_gauge_chart(risk_score)
    severity_img_path = severity_bar_chart(severity_counts)
    source_img_path = source_pie_chart(source_counts)

    chart_table = Table(
        [[Image(str(risk_img_path), width=2.3 * inch, height=1.35 * inch),
          Image(str(severity_img_path), width=3.1 * inch, height=1.6 * inch)]],
        colWidths=[2.4 * inch, 3.3 * inch],
    )
    chart_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(chart_table)
    story.append(Spacer(1, 6))
    story.append(Image(str(source_img_path), width=3.2 * inch, height=2.3 * inch))
    story.append(Spacer(1, 12))

    # Severity summary table
    story.append(Paragraph("Findings by Severity", styles["ArgusH3"]))
    table_data = [["Severity", "Count"]]
    for sev in SEVERITY_ORDER:
        table_data.append([sev.capitalize(), str(severity_counts.get(sev, 0))])

    sev_table = Table(table_data, colWidths=[3 * inch, 1.5 * inch])
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i, sev in enumerate(SEVERITY_ORDER, start=1):
        style_cmds.append(("TEXTCOLOR", (0, i), (0, i), SEVERITY_COLOR_HEX[sev]))
        style_cmds.append(("FONTNAME", (0, i), (0, i), "Helvetica-Bold"))
    sev_table.setStyle(TableStyle(style_cmds))
    story.append(sev_table)

    if project.error_message:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Scan Notes", styles["ArgusH3"]))
        story.append(Paragraph(project.error_message.replace("\n", "<br/>"), styles["ArgusBody"]))

    story.append(PageBreak())


def _top_findings_table(story, project, styles):
    story.append(Paragraph("Top Findings", styles["ArgusH2"]))
    findings = project.findings.all().order_by("severity", "-id")[:15]
    if not findings:
        story.append(Paragraph("No findings were identified in this scan.", styles["ArgusBody"]))
        story.append(PageBreak())
        return

    table_data = [["Severity", "Title", "File", "Line", "Engine"]]
    for f in findings:
        table_data.append([
            f.get_severity_display(),
            Paragraph(f.title[:70], styles["ArgusBody"]),
            Paragraph(f.file_path[-40:], styles["ArgusBody"]),
            str(f.line_number),
            f.get_source_display(),
        ])

    t = Table(table_data, colWidths=[0.75 * inch, 2.5 * inch, 1.75 * inch, 0.5 * inch, 0.9 * inch], repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dee2e6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i, f in enumerate(findings, start=1):
        style_cmds.append(("TEXTCOLOR", (0, i), (0, i), SEVERITY_COLOR_HEX.get(f.severity, colors.black)))
        style_cmds.append(("FONTNAME", (0, i), (0, i), "Helvetica-Bold"))
    t.setStyle(TableStyle(style_cmds))
    story.append(t)
    story.append(PageBreak())


MAX_APPENDIX_FINDINGS = 400


def _technical_appendix(story, project, styles):
    story.append(Paragraph("Technical Appendix", styles["ArgusH2"]))
    story.append(Paragraph(
        "Full detail for every finding identified during this scan, grouped by file.",
        styles["ArgusBody"],
    ))

    total = project.total_findings
    all_findings = list(project.findings.all().order_by("severity", "file_path", "line_number"))
    truncated = total > MAX_APPENDIX_FINDINGS
    if truncated:
        all_findings = all_findings[:MAX_APPENDIX_FINDINGS]
        story.append(Paragraph(
            f"<b>Note:</b> this scan produced {total} findings. To keep the report a "
            f"manageable size, this appendix lists the {MAX_APPENDIX_FINDINGS} highest-severity "
            f"findings. Use the web dashboard's filters to review the remaining "
            f"{total - MAX_APPENDIX_FINDINGS}.",
            styles["ArgusBody"],
        ))
    story.append(Spacer(1, 8))

    findings_by_file = {}
    for f in all_findings:
        findings_by_file.setdefault(f.file_path, []).append(f)

    for file_path, findings in sorted(findings_by_file.items()):
        story.append(Paragraph(file_path or "(unknown file)", styles["ArgusH3"]))
        for f in sorted(findings, key=lambda x: x.severity_rank):
            header = (
                f'<font color="{SEVERITY_COLOR_HEX.get(f.severity, colors.black).hexval()}">'
                f'<b>[{f.get_severity_display().upper()}]</b></font> '
                f'{f.title}  &mdash;  line {f.line_number} &middot; {f.get_source_display()}'
                + (f" &middot; {f.cwe_id}" if f.cwe_id else "")
            )
            story.append(Paragraph(header, styles["ArgusBody"]))
            if f.description:
                story.append(Paragraph(f.description[:600], styles["ArgusBody"]))
            if f.code_snippet:
                snippet = (f.code_snippet[:1200]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(snippet.replace("\n", "<br/>"), styles["ArgusMono"]))
            if f.remediation:
                story.append(Paragraph(f"<b>Remediation:</b> {f.remediation[:500]}", styles["ArgusBody"]))
            story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", color=colors.HexColor("#dee2e6"), thickness=0.5))
        story.append(Spacer(1, 8))


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#868e96"))
    canvas.drawString(0.75 * inch, 0.5 * inch, "ARGUS Secure Code Review Platform")
    canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def generate_report_pdf(project, include_technical_appendix: bool = True) -> Path:
    out_dir = Path(settings.ARGUS_REPORT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"argus_report_{project.id}_{uuid.uuid4().hex[:8]}.pdf"

    doc = SimpleDocTemplate(
        str(out_path), pagesize=letter,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        title=f"ARGUS Report - {project.name}",
    )
    styles = _styles()
    story = []

    _cover_page(story, project, styles)
    _executive_summary(story, project, styles)
    _top_findings_table(story, project, styles)
    if include_technical_appendix:
        _technical_appendix(story, project, styles)

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return out_path
