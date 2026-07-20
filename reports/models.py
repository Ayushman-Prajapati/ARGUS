from django.db import models

from scanner.models import ScanProject


class GeneratedReport(models.Model):
    project = models.ForeignKey(ScanProject, on_delete=models.CASCADE, related_name="pdf_reports")
    file = models.FileField(upload_to="pdf_reports/")
    created_at = models.DateTimeField(auto_now_add=True)
    include_technical_appendix = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.project.name} ({self.created_at:%Y-%m-%d %H:%M})"
