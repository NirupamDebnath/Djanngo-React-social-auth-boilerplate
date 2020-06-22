from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

def validate_password(password, user=None, password_validators=None):
    try:
        password_validation.validate_password(password, user=None, password_validators=None)
    except ValidationError as e:
        error_string_list = [e.message for e in e.error_list]
        return error_string_list
    return None
