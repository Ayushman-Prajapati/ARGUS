from django.contrib import admin

from .models import GeneratedReport


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ("project", "created_at", "include_technical_appendix")
    list_filter = ("include_technical_appendix",)
