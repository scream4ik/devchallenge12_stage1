"""devchallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from accounts.views import ObtainJSONWebTokenExtend

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path(
        'api-token-auth/',
        ObtainJSONWebTokenExtend.as_view(),
        name='api_token_auth'
    ),
    path('storage/', include('storage.urls')),
]

schema_view = get_schema_view(
    openapi.Info(title='Docs', default_version='v1'),
    permission_classes=(permissions.AllowAny,),
    public=True
)

urlpatterns += [
    re_path(
        '^docs/swagger(?P<format>.json|.yaml)$',
        schema_view.without_ui(cache_timeout=None),
        name='schema-json'
    ),
    path(
        'docs/swagger/',
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'
    ),
    path(
        'docs/redoc/',
        schema_view.with_ui('redoc', cache_timeout=None),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            'api/v1/api-auth/',
            include('rest_framework.urls', namespace='rest_framework')
        ),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
