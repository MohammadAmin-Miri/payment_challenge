from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .exceptions import PhoneOrEmailNotEntered
from .serializers import (
    CustomUserSerializer,
    VerifyUserPhoneSerializer,
    VerifyUserEmailSerializer,
    SigninUserSerializer,
    ResendPhoneCodeSerializer,
    ResendEmailCodeSerializer,
    UserDetailSerializer,
    UserPasswordSerializer,
    UserAddressSerializer,
)


class SignupUser(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        data = serializer.validated_data
        if 'phone' not in data and 'email' not in data:
            raise PhoneOrEmailNotEntered
        serializer.save()


class VerifyUserPhone(generics.CreateAPIView):
    serializer_class = VerifyUserPhoneSerializer
    permission_classes = [AllowAny]


class VerifyUserEmail(generics.CreateAPIView):
    serializer_class = VerifyUserEmailSerializer
    permission_classes = [AllowAny]


class SigninUser(generics.CreateAPIView):
    serializer_class = SigninUserSerializer
    permission_classes = [AllowAny]


class ResendPhoneCode(generics.CreateAPIView):
    serializer_class = ResendPhoneCodeSerializer
    permission_classes = [AllowAny]


class ResendEmailCode(generics.CreateAPIView):
    serializer_class = ResendEmailCodeSerializer
    permission_classes = [AllowAny]


class UserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPassword(generics.UpdateAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class UserAddress(generics.CreateAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
