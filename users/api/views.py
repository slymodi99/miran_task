from django.contrib.auth import authenticate

from utils.token import encode_token
from ..models import Customer, User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password


class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        user_phone = request.data.get('user_phone')
        password = request.data.get('password')
        username = request.data.get('username', )

        if not user_phone or not password or not username:
            return Response({'detail': 'Phone, Username, and Password are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(user_phone=user_phone).exists():
            return Response({'detail': 'User with this phone already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            user_phone=user_phone,
            username=username,
            password=make_password(password),
        )
        Customer.objects.get_or_create(user=user)

        return Response({'detail': 'User created successfully.'}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        phone = request.data.get('user_phone')
        password = request.data.get('password')

        user = authenticate(request, user_phone=phone, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token = encode_token({
            "user_id": user.id,
            "user_phone": user.user_phone
        })

        return Response({
            "token": token,
            "user_id": user.id,
            "user_phone": user.user_phone
        })
