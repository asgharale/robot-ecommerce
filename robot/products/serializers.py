from rest_framework import serializers
from products.models import (
    Product
)


class ProductSerializer(serializers.ModelSerializer):
    """Serializers for Products."""

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'meta', 'org_price', 'sell_price',
                  'thumbnail', 'is_exist', 'purchases']
        read_only_fields = ['id']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product details."""

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'meta', 'org_price', 'sell_price',
                  'thumbnail', 'is_exist', 'purchases', 'description',
                  'updated_at']
