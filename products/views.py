from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.request.user

        return context

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
    model = models.Product
    repos = repos.ProductRepos()
    permission_classes = [permissions.IsProductOwner]

    @swagger_auto_schema(responses={200: serializers.ProductSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            product = self.repos.get_user_products(user_id=request.user.id)
        except self.model.DoesNotExist:
            return Response({"detail": "У вас нет товаров."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ProductSerializer(product, many=True)

        return Response(serializer.data)


class FavoriteProductView(APIView):
    model = models.FavoriteProduct
    repos = repos.ProductRepos()
    permission_classes = [user_permissions.IsAuthorizedPermission]

    @swagger_auto_schema(responses={200: serializers.FavoriteProductSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            favorites = self.repos.get_favorite_products(user_id=request.user.id)
        except self.model.DoesNotExist:
            return Response({"detail": "У вас нет понравившихся товаров."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.FavoriteProductSerializer(favorites, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(method='POST', request_body=serializers.FavoriteProductSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request):
        context = {
            'user_id': request.user
        }
        serializer = serializers.FavoriteProductSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        product_id = request.data.get('product_id')
        product = self.model.objects.get(product_id=product_id)
        serializer = serializers.FavoriteProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

