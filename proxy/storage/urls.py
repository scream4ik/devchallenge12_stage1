from django.urls import path

from .views import TmpChunkedUploadView, UserFilesListView, ChunkedDownloadView


urlpatterns = [
    path('tmp-upload/', TmpChunkedUploadView.as_view(), name='tmp_upload'),
    path(
        'tmp-upload/<uuid:pk>/',
        TmpChunkedUploadView.as_view(),
        name='tmp_upload_detail'
    ),
    path('files/', UserFilesListView.as_view(), name='user_files_list'),
    path('download/<uuid:pk>/', ChunkedDownloadView.as_view(), name='download')
]
