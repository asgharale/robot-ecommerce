from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/sort/", include("sort.urls")),
    path("api/products/", include("products.urls")),
    path('admin/', admin.site.urls),
]
