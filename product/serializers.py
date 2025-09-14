from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUploadSerializer(serializers.Serializer):
    file = serializers.FileField(use_url=True)