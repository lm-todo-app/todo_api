"""
Generates and checks a hashed string to determine if the user has confirmed
their email.
"""
from settings import SECRET
from itsdangerous import URLSafeTimedSerializer

SALT = 'salt'
#  SALT = app.config['SECURITY_PASSWORD_SALT']

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
