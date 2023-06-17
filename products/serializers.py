from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('product_images')
        product = models.Product.objects.create(**validated_data)
        for image_data in images_data:
            models.ProductImage.objects.create(product=product, **image_data)
        return product
