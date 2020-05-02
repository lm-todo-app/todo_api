import string
from flask_jwt_extended import create_access_token
from models.user import User as UserModel
from models.user import UserSchema
from common.response import fail, error

def login_success_response(user):
    email = user.email
    access_token = create_access_token(identity=email)
    user_schema = UserSchema(exclude=['password'])
    user_json = user_schema.dump(user)
    return {'user': user_json, 'accessToken': access_token}

def validate_form_exclude_username(req):
    """
    For auth we only need either the email or username to identify a user.
    Using this method we only need to pass the email on authentication and we
    can ignore the username.
    """
    user_schema = UserSchema(exclude=['username'])
    _validate_schema(req, user_schema)

def validate_form(req):
    user_schema = UserSchema()
    _validate_schema(req, user_schema)

def _validate_schema(req, schema):
    errors = schema.validate(req)
    if errors:
        message = {'form': 'Error validating form'}
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

def validate_password_strength(password):
    """
    Check if the password the user supplies when signing up contains:
        no whitespace
        8 characters or greater
        at least 1 uppercase character
        at least 1 digit
        at least 1 special character
    """
    message = {}
    if ' ' in password:
        message['whitespace'] = 'whitespace is not allowed'
    if len(password) < 8:
        message['length'] = 'must be 8 characters in length'
    if not any(char.isupper() for char in password):
        message['uppercase'] = 'must contain at least one uppercase letter'
    if not any(char.isdigit() for char in password):
        message['number'] = 'must contain at least one number'
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        message['symbol'] = 'must contain at least one symbol'
    if message:
        fail(400, data={'password': message})
