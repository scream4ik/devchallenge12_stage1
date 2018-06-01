from rest_framework_jwt.views import ObtainJSONWebToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ObtainJSONWebTokenExtend(ObtainJSONWebToken):
    """
    Modify response data for swagger
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'token': openapi.Schema(type=openapi.TYPE_STRING)}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
