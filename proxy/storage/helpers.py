from rest_framework.request import Request

from .models import Server

import requests


def get_client_ip(request: Request):
    """
    Get user real ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ping(qs: Server = None) -> dict:
    """
    Get available servers information
    """
    if qs is None:
        qs = Server.objects.all()

    servers = {}

    for server in qs:
        try:
            # using ssh_host instead of public_domain for
            # docker containers particular qualities
            r = requests.get(
                'http://{}:{}/data'.format(
                    server.ssh_host, server.public_port
                )
            )
            servers[server.pk] = r.json()
        except requests.ConnectionError:
            pass

    return servers
