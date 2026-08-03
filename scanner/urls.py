from django.urls import path

from . import views

app_name = "scanner"

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("scans/", views.scan_list, name="scan_list"),
    path("scans/<uuid:project_id>/", views.scan_detail, name="scan_detail"),
    path("scans/<uuid:project_id>/rescan/", views.rescan, name="rescan"),
    path("scans/<uuid:project_id>/cancel/", views.cancel_scan, name="cancel_scan"),
    path("scans/<uuid:project_id>/delete/", views.delete_scan, name="delete_scan"),
    path("scans/<uuid:project_id>/progress/", views.scan_progress, name="scan_progress"),
    path("scans/<uuid:project_id>/progress/status/", views.scan_progress_status, name="scan_progress_status"),
    path("scans/<uuid:project_id>/compare/", views.scan_compare, name="scan_compare"),
    path("upload/file/", views.upload_file, name="upload_file"),
    path("upload/zip/", views.upload_zip, name="upload_zip"),
    path("upload/paste/", views.paste_code, name="paste_code"),
    path("upload/github/", views.scan_github, name="scan_github"),
]
