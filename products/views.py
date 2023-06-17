from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from utils import mixins
from . import serializers, models

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer,
    }

    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()

    @swagger_auto_schema(
        operation_description="Get products",
        responses={200: serializers.ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        wrapped_data = {'products': serializer.data}

        return Response(wrapped_data)
