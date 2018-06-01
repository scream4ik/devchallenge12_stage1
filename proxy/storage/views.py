from rest_framework import generics, views, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.http.response import HttpResponseRedirect

from .serializers import TmpChunkedUploadSerializer, UserFilesSerializer
from .models import TmpChunkedUpload, Server, Replica
from .tasks import data_replicate
from .helpers import get_client_ip, ping

from drf_chunked_upload.views import ChunkedUploadView
from geoip2.errors import AddressNotFoundError

import base64


class TmpChunkedUploadView(ChunkedUploadView):
    """
    Endpoint for chunked upload files
    """
    model = TmpChunkedUpload
    serializer_class = TmpChunkedUploadSerializer

    def on_completion(self, chunked_upload, request):
        """
        After completion sync file to replicated servers
        """
        data_replicate.delay(chunked_upload.pk)

    def md5_check(self, chunked_upload, md5):
        print(chunked_upload.md5)
        super().md5_check(chunked_upload, md5)


class UserFilesListView(generics.ListAPIView):
    """
    Endpoint for user files list
    """
    serializer_class = UserFilesSerializer

    def get_queryset(self):
        return TmpChunkedUpload.objects.filter(
            user=self.request.user, parent__isnull=True
        )


class ChunkedDownloadView(views.APIView):
    """
    Endpoint for download file
    """

    def get(self, request, *args, **kwargs):
        chunked_upload = get_object_or_404(
            TmpChunkedUpload, pk=kwargs['pk'], user=request.user
        )
        g = GeoIP2()

        # get user geo position
        try:
            user_point = g.geos(get_client_ip(request))
        except AddressNotFoundError:
            user_point = Point(0, 0)
        nearest_server = None

        # get suitable servers
        replica_servers = Replica.objects.filter(chunked=chunked_upload)\
                                         .values_list('server', flat=True)
        ping_servers = ping(qs=Server.objects.filter(pk__in=replica_servers))

        # calculate nearest server
        for server_id, server_data in ping_servers.items():
            # get server geo position
            server_point = g.geos(server_data['public_ip'])
            distance = user_point.distance(server_point)

            if nearest_server is None or nearest_server['distance'] > distance:
                nearest_server = {'id': server_id, 'distance': distance}

        if nearest_server is None:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # encode media file path to base64
        key = base64.b64encode(chunked_upload.file.name.encode('utf-8'))
        key = key.decode('utf-8')
        nearest_server = Server.objects.get(pk=nearest_server['id'])

        # redirect to nearest server for download
        return HttpResponseRedirect(
            redirect_to='http://{}:{}/download?key={}'.format(
                nearest_server.public_domain, nearest_server.public_port, key
            )
        )
