from django.core.exceptions import ValidationError

# Checks email for ending in .org, ensuring individual is a medical personnel
def validate_org_email(value):
    if not value.endswith('.org'):
        raise ValidationError("Email must end with .org.")