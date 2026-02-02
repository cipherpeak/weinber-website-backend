from rest_framework import serializers
from dashboard.models import Product, ProductImage, ProductFeature

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ['id', 'feature']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'description', 'created_at', 'images', 'features']
