from rest_framework import serializers
from sort.models import (
    Category,
    Tag
)


class CategorySerializer(serializers.ModelSerializer):
    """model serialzer for category model."""

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """model serializer for category model."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id']
