"""
Generates and checks a hashed string to determine if the user has confirmed
their email.
"""
from itsdangerous import URLSafeTimedSerializer
from services.sendgrid import SendgridService, Message
from settings import ENVIRONMENT, APP_URL, API_URL, SALT, SECRET


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
    except:
        return None
    return email

def send_confirmation_email(contact, confirmation_token):
    """
    Sends the confirmation email if in production and prints the confirmation
    URL to the terminal in dev.
    """
    _print_confirmation_url(confirmation_token)
    if ENVIRONMENT != 'production':
        return
    service = SendgridService()
    message = _create_email_confirmation_message(contact, confirmation_token)
    service.send(message)

def _print_confirmation_url(confirmation_token):
    """
    Print the confirmation URL in dev.
    """
    confirm_url = f'{API_URL}/v1/confirm/{confirmation_token}'
    print('\nConfirm URL:')
    print(confirm_url + '\n')

def _create_email_confirmation_message(contact, confirmation_token):
    """
    Confirmation template and data for the dynamic template stored in sendgrid.
    """
    confirmation_template = 'd-c337569b20124d6b8ba0504c7e54d481'
    template_data = {
        'subject': "Please confirm your email address",
        'confirmation_url': f'{APP_URL}/verify/{confirmation_token}'
    }
    message = Message(contact, confirmation_template, template_data)
    return message.create()
