from django.urls import path
from .views import UploadFileView,UploadDashboardView,UploadStatusView,ClearDashboardView


urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="upload-file"),
    path("dashboard/",UploadDashboardView.as_view(),name="upload-dashboard"),
    path("upload-status/<int:pk>/",UploadStatusView.as_view(),name="upload-status"),
    path("clear-dashboard/",ClearDashboardView.as_view(),name="clear-dashboard"),

]

