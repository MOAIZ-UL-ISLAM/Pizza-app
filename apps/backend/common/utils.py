import re
import string
from django.utils import timezone
from django.utils.crypto import get_random_string


def generate_unique_username(email, model):
    """Generate a unique username based on the email."""
    # Extract the part before @ in the email
    username = re.sub(r'[^a-zA-Z0-9_.]', '', email.split('@')[0])

    # If the username is already taken, append random characters
    if model.objects.filter(username=username).exists():
        random_suffix = get_random_string(
            length=5, allowed_chars=string.ascii_lowercase + string.digits)
        username = f"{username}_{random_suffix}"

    return username


def is_password_expired(password_changed_date, days=90):
    """Check if the password has expired (default: 90 days)."""
    if not password_changed_date:
        return False

    expiry_date = password_changed_date + timezone.timedelta(days=days)
    return timezone.now() >= expiry_date
