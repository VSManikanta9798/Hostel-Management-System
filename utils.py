def validate_email(email):
    # Simple email validation
    return '@' in email and '.' in email

def validate_phone(phone):
    # Simple phone number validation
    return phone.isdigit() and len(phone) == 10