"""
Generates static PNG chart images for embedding in PDF reports.

The live web dashboard renders interactive charts client-side with Chart.js;
PDF reports need flattened raster images instead, so this module uses
matplotlib (headless 'Agg' backend) to produce equivalent severity and
source-breakdown charts.
"""
import uuid
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from django.conf import settings  # noqa: E402

SEVERITY_COLORS = {
    "critical": "#dc3545",
    "high": "#fd7e14",
    "medium": "#0dcaf0",
    "low": "#6c757d",
    "info": "#e9ecef",
}

SOURCE_COLORS = {
    "bandit": "#4c6ef5",
    "semgrep": "#37b24d",
    "ast": "#f59f00",
}


def _chart_dir() -> Path:
    d = Path(settings.ARGUS_CHART_DIR)
    d.mkdir(parents=True, exist_ok=True)
    return d


def severity_bar_chart(severity_counts: dict) -> Path:
    labels = [k.capitalize() for k in severity_counts.keys()]
    values = list(severity_counts.values())
    colors = [SEVERITY_COLORS.get(k, "#999999") for k in severity_counts.keys()]

    fig, ax = plt.subplots(figsize=(6, 3.2), dpi=150)
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Findings by Severity", fontsize=12, fontweight="bold")
    ax.set_ylabel("Count")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(val),
                    ha="center", va="bottom", fontsize=9)
    fig.tight_layout()

    out_path = _chart_dir() / f"severity_{uuid.uuid4().hex}.png"
    fig.savefig(out_path, transparent=False, facecolor="white")
    plt.close(fig)
    return out_path


def source_pie_chart(source_counts: dict) -> Path:
    if not source_counts or sum(source_counts.values()) == 0:
        source_counts = {"none": 1}
    labels = [k.capitalize() for k in source_counts.keys()]
    values = list(source_counts.values())
    colors = [SOURCE_COLORS.get(k, "#adb5bd") for k in source_counts.keys()]

    fig, ax = plt.subplots(figsize=(4.5, 3.2), dpi=150)
    ax.pie(values, labels=labels, colors=colors, autopct="%1.0f%%", startangle=90,
           textprops={"fontsize": 9})
    ax.set_title("Findings by Scan Engine", fontsize=12, fontweight="bold")
    fig.tight_layout()

    out_path = _chart_dir() / f"source_{uuid.uuid4().hex}.png"
    fig.savefig(out_path, transparent=False, facecolor="white")
    plt.close(fig)
    return out_path


def risk_gauge_chart(risk_score: int) -> Path:
    fig, ax = plt.subplots(figsize=(4.5, 2.6), dpi=150, subplot_kw={"aspect": "equal"})
    color = "#dc3545" if risk_score >= 70 else "#fd7e14" if risk_score >= 40 else "#37b24d"

    ax.pie(
        [risk_score, 100 - risk_score],
        colors=[color, "#e9ecef"],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35},
    )
    ax.text(0, 0, f"{risk_score}", ha="center", va="center", fontsize=22, fontweight="bold")
    ax.set_title("Overall Risk Score", fontsize=12, fontweight="bold", y=1.05)

    out_path = _chart_dir() / f"risk_{uuid.uuid4().hex}.png"
    fig.savefig(out_path, transparent=False, facecolor="white")
    plt.close(fig)
    return out_path
