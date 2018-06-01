from celery import task

from .models import Server, TmpChunkedUpload, Replica
from .helpers import ping

import os


@task
def check_servers():
    """
    Periodic task update server status and general information
    """
    ping_servers = ping()

    for server_id, server_data in ping_servers.items():
        s = Server.objects.get(pk=server_id)
        s.free_space = server_data['free_space']
        s.status = 'online'
        s.save(update_fields=['free_space', 'status'])

    Server.objects.exclude(pk__in=ping_servers.keys()).update(status='offline')


@task
def data_replicate(chunked_upload_id: int):
    """
    Task check free space on replicated servers for sync file
    """
    chunked_upload = TmpChunkedUpload.objects.get(pk=chunked_upload_id)
    ping_servers = ping()

    for server_id, server_data in ping_servers.items():
        if server_data['free_space'] > chunked_upload.file.size:
            # sync file
            rsync.delay(server_id, chunked_upload_id)

    # TODO: if we haven't any available servers
    pass


@task
def rsync(server_id: int, chunked_upload_id: int):
    """
    Async task for sync file to replicated server using rsync
    """
    server = Server.objects.get(pk=server_id)
    chunked_upload = TmpChunkedUpload.objects.get(pk=chunked_upload_id)

    os.system(
        'sshpass -p {} rsync -az --rsync-path="mkdir -p /root/media/{} && rsync" -e "ssh -o StrictHostKeyChecking=no -p {}" {} {}@{}:/root/media/{}'.format(
            server.ssh_password,
            '/'.join(chunked_upload.file.name.split('/')[:-1]),
            server.ssh_port,
            chunked_upload.file.path,
            server.ssh_user,
            server.ssh_host,
            '/'.join(chunked_upload.file.name.split('/')[:-1])
        )
    )

    Replica.objects.get_or_create(chunked=chunked_upload, server=server)
