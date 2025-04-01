from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)
from .settings import DEBUG

urlpatterns = [
    path("api/user/", include("user.urls")),
    path("api/sort/", include("sort.urls")),
    path("api/products/", include("products.urls")),
    path('admin/', admin.site.urls)
]


if DEBUG:
    urlpatterns += [
        path("api/schema/v1/", SpectacularAPIView.as_view(), name='schema'),
        path("api/schema/v1/docs/", SpectacularSwaggerView.as_view(url_name='schema'))
    ]