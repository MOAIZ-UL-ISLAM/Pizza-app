from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import OTP, User


def send_otp_email(user_id, otp_code):
    """
    Send OTP code to user's email for password reset.

    Note: In a production environment, this would be an async task using Celery.
    For this implementation, we'll use it as a regular function.
    """
    try:
        user = User.objects.get(id=user_id)

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
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return True
    except User.DoesNotExist:
        return False
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return False


def cleanup_expired_otps():
    """
    Clean up expired OTP codes.
    In a production environment, this would be a scheduled task using Celery beat.
    """
    # OTPs that are older than 10 minutes or have been used
    expiry_time = timezone.now() - timezone.timedelta(minutes=10)

    # Delete all expired OTPs
    OTP.objects.filter(created_at__lt=expiry_time).delete()

    # Delete all used OTPs
    OTP.objects.filter(is_used=True).delete()
