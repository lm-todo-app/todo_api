from settings import SECRET
from itsdangerous import URLSafeTimedSerializer

SALT = 'salt'

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET)
    return serializer.dumps(email, salt=SALT)
    #  return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET)
    try:
        email = serializer.loads(
            token,
            salt=SALT,
            max_age=expiration
        )
    except:
        return False
    return email
