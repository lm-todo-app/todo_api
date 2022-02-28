"""
Generates and checks a hashed string to determine if the user has confirmed
their email.
"""
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired, BadSignature
from services.sendgrid import Message
from settings import APP_URL, API_URL, SALT, SECRET


def generate_confirmation_token(email):
    """
    Create a unqiue token for the user to use for email validation.
    """
    serializer = URLSafeTimedSerializer(SECRET)
    return serializer.dumps(email, salt=SALT)


def confirm_token(token, expiration=3600):
    """
    Check the unique token is correct.
    Expiration is set to an hour.
    """
    serializer = URLSafeTimedSerializer(SECRET)
    try:
        email = serializer.loads(token, salt=SALT, max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email


def print_confirmation_url(confirmation_token):
    """
    Print the confirmation URL in dev.
    """
    confirm_url = f"{API_URL}/v1/confirm/{confirmation_token}"
    print("\nConfirm URL:")
    print(confirm_url + "\n")


def create_email_confirmation_message(contact, confirmation_token):
    """
    Confirmation template and data for the dynamic template stored in sendgrid.
    """
    # TODO: Add to a sendgrid message class:
    # self.confirmation_template = 'd-c337569b20124d6b8ba0504c7e54d481'
    # self.template_data = {
    #     'subject': 'Please confirm your email address',
    #     'confirmation_url': f'{APP_URL}/verify/{confirmation_token}'
    # }

    confirmation_template = "d-c337569b20124d6b8ba0504c7e54d481"
    template_data = {
        "subject": "Please confirm your email address",
        "confirmation_url": f"{APP_URL}/verify/{confirmation_token}",
    }
    message = Message(contact, confirmation_template, template_data)
    return message.create()
