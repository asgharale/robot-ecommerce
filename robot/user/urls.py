from django.urls import path
from .views import (
    OTPView
)


urlpatterns = [
    path('v1/otp/', OTPView.as_view()),
]
