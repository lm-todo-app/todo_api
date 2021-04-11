import string
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from marshmallow import fields
from marshmallow import validate
from marshmallow import pre_load
from database import db
from models.base import BaseSchema
from common.response import fail


class User(db.Model):
    """
    User model, currently has username and email as unique fields.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(200), unique=False, nullable=True)
    last_name = db.Column(db.String(200), unique=False, nullable=True)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        """
        Generates a password hash using werkzeug security ready to save to the
        database.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the password in the database matches the supplied password.
        """
        return check_password_hash(self.password, password)


class UserSchema(BaseSchema):
    """
    Schema for user validation with API.
    """
    class Meta:
        model = User
        load_instance = True

    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    username = fields.Str(
        validate=validate.Length(min=5, max=100),
        required=True
    )

    @pre_load
    def process_input(self, data, **kwargs): # pylint: disable=unused-argument
        """
        Before checking for validation strip whitespace from email and username.
        """
        if not data:
            return data
        if data.get('email'):
            data['email'] = data['email'].lower().strip()
        if data.get('username'):
            data['username'] = data['username'].strip()
        return data


def delete_user(user):
    db.session.delete(user)

def create_user(form):
    """
    We need to exclude the password from the request as it needs to be
    hashed before being saved to the database. We exclude it from the
    marshmallow loads which creates the user model object and then add the
    hashed password to the user object.
    """
    schema = UserSchema()
    password = form.pop('password')
    user = schema.load(form, session=db.session)
    user.set_password(password)
    db.session.add(user)
    return user

def validate_create_user_form(form):
    """
    Password is required here but is not required by marshmallow because
    it is load only so we need to check the field exists here instead.

    Also check unique username, email and that the user has used a strong
    password.
    """
    if not form.get('password'):
        fail(400, {'form':{'password': 'Missing data for required field.'}})
    _unique_email_or_409(form['email'])
    _unique_username_or_409(form['username'])
    _strong_password_or_400(form['password'])

def set_updated_user_values(user, form):
    """
    check that each field is in the response, if they aren't then they don't
    need to be updated.

    Also check that the username and email that the user wants to update
    to are not already in use by another user and will throw an error if
    they are.
    """
    username = form.get('username')
    if username and user.username != username:
        _unique_username_or_409(username)
        user.username = username
    email = form.get('email')
    if email and user.email != email:
        _unique_email_or_409(email)
        user.email = email
    password = form.get('password')
    if password:
        _strong_password_or_400(password)
        user.set_password(password)
    return user

def _unique_email_or_409(email):
    if User.query.filter_by(email=email).first():
        message = {'user': 'User already exists with this email'}
        fail(409, data=message)

def _unique_username_or_409(username):
    if User.query.filter_by(username=username).first():
        message = {'user': 'User already exists with this username'}
        fail(409, data=message)

def _strong_password_or_400(password):
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
    return None

def _check_length(password):
    """
    Check password string is 8 characters or greater.
    """
    if len(password) < 8:
        return 'must be 8 characters in length'
    return None

def _check_uppercase(password):
    """
    Check password string contains at least one uppercase character.
    """
    if not any(char.isupper() for char in password):
        return 'must contain at least one uppercase letter'
    return None

def _check_number(password):
    """
    Check password string contains at least one number.
    """
    if not any(char.isdigit() for char in password):
        return 'must contain at least one number'
    return None

def _check_special_char(password):
    """
    Check password string contains at least one special character.
    """
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        return 'must contain at least one symbol'
    return None
