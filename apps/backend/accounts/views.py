from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import User, OTP
from .serializers import (
    RequestPasswordResetSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
)


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"})


def generate_otp():
    """Generate a 6-digit OTP code."""
    return ''.join(random.choices(string.digits, k=6))


class RequestPasswordResetView(APIView):
    """
    Request a password reset and send OTP code to the user's email.
    """
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)

                # Generate the OTP code
                otp_code = generate_otp()

                # Save the OTP to the database
                OTP.objects.create(user=user, code=otp_code)

                # Send the OTP to the user's email
                subject = 'Password Reset OTP'
                html_message = render_to_string('password_reset.html', {
                    'user': user,
                    'otp_code': otp_code,
                })
                plain_message = strip_tags(html_message)

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html_message,
                    fail_silently=False,
                )

                return Response(
                    {"detail": "OTP has been sent to your email address."},
                    status=status.HTTP_200_OK
                )

            except User.DoesNotExist:
                # We still return a 200 to prevent user enumeration
                return Response(
                    {"detail": "If your email is registered, you will receive an OTP code."},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """
    Verify the OTP code sent to the user's email.
    """
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Mark the OTP as used
            otp = serializer.validated_data['otp']
            otp.is_used = True
            otp.save()

            return Response(
                {"detail": "OTP verified successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Reset the user's password after verifying the OTP.
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp = serializer.validated_data['otp']

            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Mark the OTP as used
            otp.is_used = True
            otp.save()

            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's details.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        from .serializers import UserSerializer
        return UserSerializer
