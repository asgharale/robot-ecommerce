from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/user/", include("user.urls")),
    path("api/sort/", include("sort.urls")),
    path("api/products/", include("products.urls")),
    path('admin/', admin.site.urls),
]
