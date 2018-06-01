from django.db import models, transaction
from django.utils import timezone

from drf_chunked_upload.models import ChunkedUpload


class TmpChunkedUpload(ChunkedUpload):
    """
    Model with chunked upload file data
    """
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={'parent': None},
        related_name='versions'
    )

    @transaction.atomic
    def completed(self, completed_at=timezone.now(), ext='.done'):
        """We want use real file extension instead of .done"""
        ext = '.{}'.format(self.filename.split('.')[-1])
        super().completed(completed_at=completed_at, ext=ext)


class Server(models.Model):
    """
    Model with servers connection data and general information
    """
    STATUS = (
        ('online', 'online'),
        ('offline', 'offline'),
    )
    public_domain = models.CharField(max_length=40, unique=True)
    public_port = models.SmallIntegerField()
    free_space = models.BigIntegerField(default=0, editable=False)
    status = models.CharField(
        choices=STATUS,
        max_length=7,
        default='offline',
        editable=False
    )
    ssh_host = models.CharField(max_length=20)
    ssh_user = models.CharField(max_length=20)
    ssh_password = models.CharField(max_length=20)
    ssh_port = models.SmallIntegerField(default=22)

    def __str__(self):
        return '{}:{}'.format(self.public_domain, self.public_port)


class Replica(models.Model):
    """
    Model with replicated servers on which was copy file
    """
    chunked = models.ForeignKey(TmpChunkedUpload, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('chunked', 'server')
