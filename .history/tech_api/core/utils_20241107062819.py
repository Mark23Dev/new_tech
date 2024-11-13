# core/utils.py

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_email(email):
    """
    Validates the provided email address.
    Raises ValidationError if the email is not valid.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValidationError(_('Invalid email address'))

def calculate_age(birth_date):
    """
    Calculates the age of a person based on their birth date.
    """
    from datetime import date

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def format_date(date_obj, format_string="%Y-%m-%d"):
    """
    Formats a given date object into a string based on the provided format.
    """
    return date_obj.strftime(format_string)

def generate_random_string(length=10):
    """
    Generates a random string of fixed length.
    """
    import random
    import string

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def send_welcome_email(user):
    """
    Sends a welcome email to the newly registered user.
    """
    subject = 'Welcome to STEM Platform'
    message = f'Hi {user.first_name},\n\nThank you for joining our STEM community!'
    from django.core.mail import send_mail
    send_mail(
        subject,
        message,
        'noreply@yourdomain.com',  # Use your domain email
        [user.email],
        fail_silently=False,
    )
