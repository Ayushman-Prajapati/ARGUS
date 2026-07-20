import uuid

from django.db import models
from django.urls import reverse


class ScanProject(models.Model):
    """A single scan session: one upload/paste/clone, scanned as a unit."""

    SOURCE_CHOICES = [
        ("file", "Single File Upload"),
        ("zip", "Project Archive (.zip)"),
        ("paste", "Pasted Code Snippet"),
        ("github", "GitHub Repository"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Scanning"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    source_reference = models.CharField(
        max_length=500, blank=True,
        help_text="Original filename, repo URL, or 'pasted snippet'"
    )
    scan_path = models.CharField(
        max_length=1000, blank=True,
        help_text="Absolute path on disk to the scanned code root"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)

    run_bandit = models.BooleanField(default=True)
    run_semgrep = models.BooleanField(default=True)
    run_ast_checks = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(null=True, blank=True)

    files_scanned = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse("scanner:scan_detail", args=[str(self.id)])

    @property
    def total_findings(self):
        return self.findings.count()

    def severity_counts(self):
        qs = self.findings.values("severity").annotate(count=models.Count("id"))
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for row in qs:
            counts[row["severity"]] = row["count"]
        return counts

    def source_counts(self):
        qs = self.findings.values("source").annotate(count=models.Count("id"))
        return {row["source"]: row["count"] for row in qs}

    def risk_score(self):
        """Weighted 0-100 risk score derived from severity distribution."""
        weights = {"critical": 10, "high": 6, "medium": 3, "low": 1, "info": 0}
        counts = self.severity_counts()
        raw = sum(weights[k] * v for k, v in counts.items())
        return min(100, raw)


class Finding(models.Model):
    """A single security finding, normalized across Bandit/Semgrep/AST engines."""

    SEVERITY_CHOICES = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
        ("info", "Informational"),
    ]

    SOURCE_CHOICES = [
        ("bandit", "Bandit"),
        ("semgrep", "Semgrep"),
        ("ast", "ARGUS AST Engine"),
    ]

    project = models.ForeignKey(ScanProject, on_delete=models.CASCADE, related_name="findings")
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    rule_id = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default="medium")
    confidence = models.CharField(max_length=20, blank=True)

    file_path = models.CharField(max_length=1000)
    line_number = models.PositiveIntegerField(default=0)
    end_line_number = models.PositiveIntegerField(null=True, blank=True)
    code_snippet = models.TextField(blank=True)

    cwe_id = models.CharField(max_length=50, blank=True)
    owasp_category = models.CharField(max_length=100, blank=True)
    remediation = models.TextField(blank=True)

    class Meta:
        ordering = ["severity", "file_path", "line_number"]
        indexes = [
            models.Index(fields=["project", "severity"]),
            models.Index(fields=["project", "source"]),
        ]

    def __str__(self):
        return f"[{self.severity.upper()}] {self.title} ({self.file_path}:{self.line_number})"

    SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

    @property
    def severity_rank(self):
        return self.SEVERITY_ORDER.get(self.severity, 5)

    @property
    def severity_badge_class(self):
        return {
            "critical": "bg-danger",
            "high": "bg-warning text-dark",
            "medium": "bg-info text-dark",
            "low": "bg-secondary",
            "info": "bg-light text-dark",
        }.get(self.severity, "bg-secondary")
