from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.protocols.basic import FileSender
from twisted.python.log import err

import os
import json
import base64


class DataPage(Resource):
    """
    Resource with server general information
    """

    def render_GET(self, request):
        s = os.statvfs('/')
        free = s.f_bsize * s.f_bavail

        data = {
            'free_space': free,
            'public_ip': os.environ.get('PUBLIC_IP')
        }

        return '{}'.format(json.dumps(data)).encode('utf-8')


class DownloadPage(Resource):
    """
    Resource for download media file by key
    """

    def render_GET(self, request):
        # key - path to media file in base64
        path = base64.b64decode(request.args[b'key'][0]).decode('utf-8')

        fp = open('/root/media/{}'.format(path), 'rb')
        d = FileSender().beginFileTransfer(fp, request)

        def cbFinished(ignored):
            fp.close()
            request.finish()

        d.addErrback(err).addCallback(cbFinished)
        return NOT_DONE_YET


root = Resource()
root.putChild(b'data', DataPage())
root.putChild(b'download', DownloadPage())

factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 9999)
endpoint.listen(factory)
reactor.run()
