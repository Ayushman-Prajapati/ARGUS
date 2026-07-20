from django.contrib import admin

from .models import Finding, ScanProject


class FindingInline(admin.TabularInline):
    model = Finding
    extra = 0
    fields = ("source", "severity", "title", "file_path", "line_number")
    readonly_fields = fields
    can_delete = False


@admin.register(ScanProject)
class ScanProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "source_type", "status", "total_findings", "created_at")
    list_filter = ("source_type", "status")
    search_fields = ("name", "source_reference")
    inlines = [FindingInline]


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "source", "severity", "file_path", "line_number")
    list_filter = ("source", "severity")
    search_fields = ("title", "file_path", "rule_id")
