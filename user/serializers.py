from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.exceptions import (
    VerificationCodeExpiredOrInvalid,
    VerificationCodeInvalid,
    InvalidPhoneOrEmail,
    WrongPassword,
    UserNotVerified,
    PhoneAlreadyVerified,
    InvalidPhoneEntry,
    EmailAlreadyVerified,
    InvalidEmailEntry,
)
from user.tasks import send_verification_code
from user.utils import get_tokens_for_user

user_model = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=11, required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user_model
        fields = ['phone', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = user_model(**validated_data)
        user.set_password(password)
        user.save()
        send_verification_code.apply_async((validated_data.get('phone'), validated_data.get('email')))
        return user


class VerifyUserPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, write_only=True)
    code = serializers.CharField(write_only=True)
    phone_verified = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        phone = validated_data.get('phone')
        valid_code = cache.get(phone)
        if not valid_code:
            raise VerificationCodeExpiredOrInvalid
        if validated_data.get('code') != valid_code:
            raise VerificationCodeInvalid
        user_model.objects.filter(phone=phone).update(phone_verified=True)
        return {'phone_verified': True}


class VerifyUserEmailSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    email_verified = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        email = validated_data.get('email')
        valid_code = cache.get(email)
        if not valid_code:
            raise VerificationCodeExpiredOrInvalid
        if validated_data.get('code') != valid_code:
            raise VerificationCodeInvalid
        user_model.objects.filter(email=email).update(email_verified=True)
        return {'email_verified': True}


class SigninUserSerializer(serializers.ModelSerializer):
    phone_or_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    # access_token = serializers.CharField(read_only=True)
    # refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = user_model
        fields = ['phone_or_email', 'password', 'token']
        # 'access_token', 'refresh_token']

    def create(self, validated_data):
        password = validated_data.get('password')
        phone_or_email = validated_data.get('phone_or_email')
        try:
            user = user_model.objects.get(Q(phone=phone_or_email) | Q(email=phone_or_email))
        except user_model.DoesNotExist:
            raise InvalidPhoneOrEmail
        else:
            if not user.check_password(password):
                raise WrongPassword
            if not user.email_verified and not user.phone_verified:
                raise UserNotVerified
        return get_tokens_for_user(user)


class ResendPhoneCodeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    code_sent = serializers.BooleanField(read_only=True)

    class Meta:
        model = user_model
        fields = ['phone', 'code_sent']

    def create(self, validated_data):
        phone = validated_data.get('phone')
        try:
            user = user_model.objects.get(phone=phone)
        except user_model.DoesNotExist:
            raise InvalidPhoneEntry
        else:
            if user.phone_verified:
                raise PhoneAlreadyVerified
            send_verification_code.apply_async((validated_data.get('phone'), None))
            return {'code_sent': True}


class ResendEmailCodeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    code_sent = serializers.BooleanField(read_only=True)

    class Meta:
        model = user_model
        fields = ['email', 'code_sent']

    def create(self, validated_data):
        email = validated_data.get('email')
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            raise InvalidEmailEntry
        else:
            if user.phone_verified:
                raise EmailAlreadyVerified
            send_verification_code.apply_async((None, validated_data.get('email')))
            return {'code_sent': True}


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['id', 'first_name', 'last_name', 'phone', 'phone_verified', 'email', 'email_verified']
        read_only_fields = ['id', 'phone_verified', 'email_verified']

    def update(self, instance, validated_data):
        if 'phone' in validated_data:
            instance.phone_verified = False
            send_verification_code.apply_async((validated_data.get('phone'), None))
        if 'email' in validated_data:
            instance.email_verified = False
            send_verification_code.apply_async((None, validated_data.get('email')))
        return super().update(instance, validated_data)


class UserPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    # access_token = serializers.CharField(read_only=True)
    # refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = user_model
        fields = ['password', 'token']
        # 'access_token', 'refresh_token']
        read_only_fields = ['access_token', 'refresh_token']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        tokens = OutstandingToken.objects.filter(user=instance)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        instance.save()
        return get_tokens_for_user(instance)
