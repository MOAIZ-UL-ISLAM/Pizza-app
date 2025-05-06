from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send a welcome email when a new user is created."""
    if created and settings.EMAIL_HOST_USER:  # Only send if email settings are configured
        subject = 'Welcome to Our App!'
        html_message = f"""
        <html>
        <body>
            <h2>Welcome to Our App, {instance.username}!</h2>
            <p>Thank you for registering. Your account has been created successfully.</p>
            <p>You can now login using your email address: {instance.email}</p>
            <p>If you have any questions, please feel free to contact us.</p>
            <p>Best regards,</p>
            <p>The Team</p>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            html_message=html_message,
            fail_silently=True,  # Set to True to prevent registration errors if email fails
        )
