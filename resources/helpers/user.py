import string
from models.user import User as UserModel
from common.response import fail

def validate_request(req, schema):
    errors = schema.validate(req)
    if errors:
        message = {'form': errors}
        fail(400, data=message)

def validate_unique_email(email):
    user = UserModel.query.filter_by(email=email).first()
    if user:
        message = {'user': 'User already exists with this email'}
        fail(409, data=message)

def validate_unique_username(username):
    user = UserModel.query.filter_by(username=username).first()
    if user:
        message = {'user': 'User already exists with this username'}
        fail(409, data=message)

def get_user(user_id):
    """
    Leaving this here instead of moving this to the model because it uses flask
    abort and we don't want the model methods to use that.
    """
    user = UserModel.query.get(user_id)
    if not user:
        message = {'user': 'User does not exist'}
        fail(404, data=message)
    return user

# TODO The code below should be part of schema
def validate_password_strength(password):
    """
    Check if the password the user supplies when signing up contains:
        no whitespace
        8 characters or greater
        at least 1 uppercase character
        at least 1 number
        at least 1 special character
    """
    message = {}
    message['whitespace'] = _check_whitespace(password)
    message['length'] = _check_length(password)
    message['uppercase'] = _check_uppercase(password)
    message['number'] = _check_number(password)
    message['symbol'] = _check_special_char(password)
    if any(message.values()):
        fail(400, data={'password': message})

def _check_whitespace(password):
    """
    Check for whitespace in password string.
    """
    if ' ' in password:
        return 'whitespace is not allowed'

def _check_length(password):
    """
    Check password string is 8 characters or greater.
    """
    if len(password) < 8:
        return 'must be 8 characters in length'

def _check_uppercase(password):
    """
    Check password string contains at least one uppercase character.
    """
    if not any(char.isupper() for char in password):
        return 'must contain at least one uppercase letter'

def _check_number(password):
    """
    Check password string contains at least one number.
    """
    if not any(char.isdigit() for char in password):
        return 'must contain at least one number'

def _check_special_char(password):
    """
    Check password string contains at least one special character.
    """
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        return 'must contain at least one symbol'
