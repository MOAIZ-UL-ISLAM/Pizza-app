from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RequestPasswordResetView,
    VerifyOTPView,
    ResetPasswordView,
    UserDetailsView,
    hello_world,
)

urlpatterns = [
    # Djoser endpoints
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    # test
    path('hello/', hello_world),

    # Custom password reset with OTP
    path('password/reset/', RequestPasswordResetView.as_view(),
         name='password-reset'),
    path('password/reset/verify-otp/',
         VerifyOTPView.as_view(), name='verify-otp'),
    path('password/reset/confirm/', ResetPasswordView.as_view(),
         name='password-reset-confirm'),

    # User details
    path('me/', UserDetailsView.as_view(), name='user-details'),

    # JWT token refresh
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
