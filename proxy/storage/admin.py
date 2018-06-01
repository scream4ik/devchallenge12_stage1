from django.contrib import admin

from .models import TmpChunkedUpload, Server


@admin.register(TmpChunkedUpload)
class TmpChunkedUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'user', 'status', 'created_at', 'parent')
    search_fields = ('filename',)
    list_filter = ('status',)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('public_domain', 'public_port', 'free_space', 'status')
    list_filter = ('status',)
