import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, validate, pre_load
from database import db
from models.base import BaseSchema
from common.response import fail
from common.confirm_email import (
    generate_confirmation_token,
    print_confirmation_url,
    create_email_confirmation_message,
)
from services.sendgrid import SendgridService
from authz import e
from settings import ENVIRONMENT


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

    def send_confirmation_email(self):
        """
        Sends the confirmation email if in production and prints the confirmation
        URL to the terminal in dev.
        """
        token = generate_confirmation_token(self.email)
        print_confirmation_url(token)
        if ENVIRONMENT != "production":
            return
        message = create_email_confirmation_message(self.email, token)
        SendgridService().send(message)

    def json(self):
        return UserSchema().dump(self)

    def set_role(self, role):
        e.add_role_for_user(self.email, role)

    def has_permission(self, obj, act):
        return e.enforce(self.email, obj, act)

    def save_email_confirmation(self):
        self.confirmed_on = datetime.now()
        db.session.add(self)

    def delete(self):
        # TODO: Remove from authz table
        db.session.delete(self)

    def update(self, form):
        """
        check that each field is in the response, if they aren't then they don't
        need to be updated.

        Also check that the username and email that the user wants to update
        to are not already in use by another user and will throw an error if
        they are.
        """
        username = form.get("username")
        if username and self.username != username:
            _unique_username_or_409(username)
            self.username = username
        email = form.get("email")
        if email and self.email != email:
            _unique_email_or_409(email)
            self.email = email
            # TODO: If email has changed update role table
        password = form.get("password")
        if password:
            _strong_password_or_400(password)
            self.set_password(password)
        return self

    @staticmethod
    def create(form, autoconfirm=False):
        """
        We need to exclude the password from the request as it needs to be
        hashed before being saved to the database. We exclude it from the
        marshmallow loads which creates the user model object and then add the
        hashed password to the user object.

        Autoconfirm True allows users created from the cli to skip confirmation
        email.
        """
        _validate_create_user_form(form)
        password = form.pop("password")
        user = UserSchema().load(form, session=db.session)
        user.set_password(password)
        if autoconfirm:
            user.confirmed_on = datetime.now()
        db.session.add(user)
        return user

    @classmethod
    def get_many(cls, sort, page, size):
        return cls.query.order_by(sort).paginate(page=page, per_page=size).items

    @classmethod
    def get(cls, user_id):
        msg = {"status": "fail", "data": {"Not Found": "User does not exist"}}
        return cls.query.get_or_404(user_id, msg)


class UserSchema(BaseSchema):
    """
    Schema for user validation with API.
    """

    class Meta:
        model = User
        load_instance = True

    email = fields.Email(required=True)
    password = fields.Str(load_only=True)
    username = fields.Str(validate=validate.Length(min=5, max=100), required=True)

    @pre_load
    def process_input(self, data, **kwargs):  # pylint: disable=unused-argument
        """
        Before checking for validation strip whitespace from email and username.
        """
        if not data:
            return data
        if data.get("email"):
            data["email"] = data["email"].lower().strip()
        if data.get("username"):
            data["username"] = data["username"].strip()
        return data


def jsonify_users(users):
    return [user.json() for user in users]


def _validate_create_user_form(form):
    """
    Password is required here but is not required by marshmallow because
    it is load only so we need to check the field exists here instead.

    Also check unique username, email and that the user has used a strong
    password.
    """
    if not form.get("password"):
        fail(400, {"form": {"password": "Missing data for required field."}})
    _unique_email_or_409(form["email"])
    _unique_username_or_409(form["username"])
    _strong_password_or_400(form["password"])


def _unique_email_or_409(email):
    if User.query.filter_by(email=email).first():
        message = {"user": "User already exists with this email"}
        fail(409, data=message)


def _unique_username_or_409(username):
    if User.query.filter_by(username=username).first():
        message = {"user": "User already exists with this username"}
        fail(409, data=message)


def _strong_password_or_400(password):
    """
    Check if the password the user supplies when signing up contains:
        no whitespace
        8 characters or greater
        at least 1 uppercase character
        at least 1 number
        at least 1 special character

    Return the error messages found in the password in response.
    """
    message = {}

    if " " in password:
        message["whitespace"] = "whitespace is not allowed"

    if len(password) < 8:
        message["length"] = "must be 8 characters in length"

    if not any(char.isupper() for char in password):
        message["uppercase"] = "must contain at least one uppercase letter"

    if not any(char.isdigit() for char in password):
        message["number"] = "must contain at least one number"

    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        message["symbol"] = "must contain at least one symbol"

    if any(message.values()):
        fail(400, data={"password": message})
