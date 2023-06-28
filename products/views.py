from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from utils import mixins
from . import serializers, models, permissions, repos
from users import permissions as user_permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer,
    }

    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [user_permissions.IsAuthorizedPermission]

    @swagger_auto_schema(
        operation_description="Get products",
        responses={200: serializers.ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        wrapped_data = {'products': serializer.data}

        return Response(wrapped_data)


class UserProductView(APIView):
    repos = repos.ProductRepos()
    permission_classes = [permissions.IsProductOwner]

    @swagger_auto_schema(responses={200: serializers.ProductSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            product = self.repos.get_user_products(user_id=request.user.id)
        except self.model.DoesNotExist:
            return Response({"detail": "У вас нет товара."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ProductSerializer(product, many=True)

        return Response(serializer.data)
