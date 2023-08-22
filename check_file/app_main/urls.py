from django.urls import path

from .views import IndexView, UploadFileView, DeleteFile

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload-file', UploadFileView.as_view(), name='upload_file'),
    path('delete-file/<int:pk>/', DeleteFile.as_view(), name='delete_file'),
]