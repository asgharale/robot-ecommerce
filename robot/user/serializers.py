from rest_framework import serializers
from .models import (
    OTPRequest,
    CUser,
    Address
)
from phonenumber_field.serializerfields import PhoneNumberField


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['request_id']


class VerifyOtpRequestserializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = PhoneNumberField(region='IR', allow_null=False)


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    created = serializers.BooleanField()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'description']


class AddressDetailSerailizer(serializers.ModelSerializer):
    class MEta:
        model = Address
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CUser
        fields = ['id', 'username','email', 'first_name', 'last_name',
                  'birthdate', 'phone_verified', 'email_verified',
                  'created_at', 'favorates', 'addresses']