from .models import TmpChunkedUpload

from rest_framework import serializers
from rest_framework.reverse import reverse

from drf_chunked_upload.serializers import ChunkedUploadSerializer


class TmpChunkedUploadSerializer(ChunkedUploadSerializer):
    """
    Serializer for chunked upload file
    """

    class Meta:
        model = TmpChunkedUpload
        fields = '__all__'
        read_only_fields = ('status', 'competed_at')

    def get_url(self, obj):
        return reverse(
            'tmp_upload_detail', args=[obj.id], request=self.context['request']
        )


class UserFilesVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for user version files list
    """
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = TmpChunkedUpload
        fields = ('id', 'filename', 'created_at', 'download_url')

    def get_download_url(self, obj):
        return reverse(
            'download', args=[obj.id], request=self.context['request']
        )


class UserFilesSerializer(serializers.ModelSerializer):
    """
    Serializer for user parent files list
    """
    download_url = serializers.SerializerMethodField()
    versions = UserFilesVersionSerializer(many=True)

    class Meta:
        model = TmpChunkedUpload
        fields = ('id', 'filename', 'created_at', 'download_url', 'versions')

    def get_download_url(self, obj):
        return reverse(
            'download', args=[obj.id], request=self.context['request']
        )
