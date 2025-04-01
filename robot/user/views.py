from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import (
    RequestOTPSerializer,
    RequestOTPResponseSerializer,
    VerifyOtpRequestserializer,
    ObtainTokenSerializer
)
from rest_framework.response import Response
from rest_framework import status
from .models import (
	OTPRequest,
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class OTPView(APIView):
    def get(self, request):
        serializer = RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(status=status.HTTP_201_CREATED, data=RequestOTPResponseSerializer(otp).data)
            except Exception as e:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def post(self, request):
        serializer = VerifyOtpRequestserializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(receiver=data['receiver'],
                                           request_id=data['request_id'], 
                                           password=data['password']):
                return Response(self._handle_login(data))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=serializer.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, otp):
        User = get_user_model()
        query = User.objects.filter(username=otp['receiver'])
        if query.exists():
            create = False
            user = query.first()
        else:
            user = User.objects.create(
                username=otp['receiver'],
            )
            create = True
        refresh = RefreshToken.for_user(user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'created': create
        }).data