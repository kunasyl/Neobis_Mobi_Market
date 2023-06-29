from rest_framework import serializers

from . import models


class ProductLikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_likes_count(self, obj):
        return models.FavoriteProduct.objects.filter(product_id=obj).count()


class ProductSerializer(serializers.ModelSerializer):
    # likes_count = ProductLikeSerializer()

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('image', )


# Serializer for product details
class RetrieveProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    # likes_count = ProductLikeSerializer()

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('product_images')
        product = models.Product.objects.create(**validated_data)
        for image_data in images_data:
            models.ProductImage.objects.create(product=product, **image_data)
        return product


class FavoriteProductSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())
    # likes_count = ProductLikeSerializer()

    class Meta:
        model = models.FavoriteProduct
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_data = ProductSerializer(instance.product_id).data
        representation['product'] = product_data
        return representation

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        product_id = validated_data.get('product_id')
        favorite = models.FavoriteProduct.objects.create(user_id=user_id, product_id=product_id)
        return favorite
