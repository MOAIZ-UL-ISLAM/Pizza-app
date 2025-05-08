import re
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import OTP

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer for creating user instances."""

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username', 'password',
                  'confirm_password', ]
        extra_kwargs = {
            'password': {'write_only': True},

        }

    def validate_password(self, value):

        try:
            validate_password(value)  # Uses Django's built-in validators
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return attrs


class UserSerializer(BaseUserSerializer):
    """Serializer for user instances."""

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username',
                  'date_joined']
        read_only_fields = ['id', 'email', 'date_joined']


class RequestPasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset."""

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate the email exists."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No user with this email address exists.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for verifying the OTP code."""

    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)

    def validate(self, attrs):
        """Validate the OTP code."""
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No user with this email address exists."})

        # Get the latest non-used OTP for the user
        latest_otp = OTP.objects.filter(
            user=user, is_used=False).order_by('-created_at').first()

        if not latest_otp:
            raise serializers.ValidationError(
                {"otp_code": "No active OTP found. Please request a new one."})

        if latest_otp.is_expired:
            raise serializers.ValidationError(
                {"otp_code": "OTP has expired. Please request a new one."})

        if latest_otp.code != otp_code:
            raise serializers.ValidationError(
                {"otp_code": "Invalid OTP code."})

        attrs['user'] = user
        attrs['otp'] = latest_otp

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting the password."""

    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        """Validate the new password meets requirements."""
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))

        # Check if password is exactly 8 digits
        if not re.match(r'^\d{8}$', value):
            raise serializers.ValidationError(
                "Password must be exactly 8 digits.")

        return value

    def validate(self, attrs):
        """Validate OTP and that passwords match."""
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "No user with this email address exists."})

        # Get the latest non-used OTP for the user
        latest_otp = OTP.objects.filter(
            user=user, is_used=False).order_by('-created_at').first()

        if not latest_otp:
            raise serializers.ValidationError(
                {"otp_code": "No active OTP found. Please request a new one."})

        if latest_otp.is_expired:
            raise serializers.ValidationError(
                {"otp_code": "OTP has expired. Please request a new one."})

        if latest_otp.code != otp_code:
            raise serializers.ValidationError(
                {"otp_code": "Invalid OTP code."})

        attrs['user'] = user
        attrs['otp'] = latest_otp

        return attrs
