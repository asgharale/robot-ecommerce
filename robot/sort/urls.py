from django.urls import path, include
from .views import CategoryViewset, TagViewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('categories', CategoryViewset)
router.register('tags', TagViewset)

urlpatterns = [
    path("v1/", include(router.urls)),
]
