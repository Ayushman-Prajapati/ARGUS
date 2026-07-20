from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("generate/<uuid:project_id>/", views.generate_report, name="generate_report"),
    path("download/<int:report_id>/", views.download_report, name="download_report"),
]
