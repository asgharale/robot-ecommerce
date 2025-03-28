from rest_framework import (
    viewsets,
    status,
)
from rest_framework.response import Response
from sort.models import Category, Tag
from sort.serializers import CategorySerializer, TagSerializer
from rest_framework.permissions import AllowAny


class CategoryViewset(viewsets.GenericViewSet):
    """Category Viewset"""

    authentication_classes = [AllowAny,]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'address'

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        instance = self.get_object()
        serializer = CategorySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewset(viewsets.GenericViewSet):
    """Tag Viewset"""

    authentication_classes = [AllowAny,]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = 'address'

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
