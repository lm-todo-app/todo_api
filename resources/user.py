from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db, try_commit
from common.response import success, error
from resources.helpers.confirm import generate_confirmation_token
from mail import send_email
from resources.helpers.user_auth import (
    login_success_response,
    validate_form,
    get_user,
    validate_password_strength,
    validate_unique_email,
    validate_unique_username
)

class User(Resource):
    def __init__(self):
        self.req = None
        self.user = None

    @jwt_required
    def get(self, user_id):
        user = get_user(user_id)
        user_schema = UserSchema(exclude=['password'])
        return success(user_schema.dump(user))

    @jwt_required
    def put(self, user_id):
        self.req = request.get_json()
        validate_form(self.req)
        self.user = get_user(user_id)
        self._set_updated_user_values()
        if try_commit():
            return success()
        message = {'user': 'Error updating user'}
        error(500, message)

    def _set_updated_user_values(self):
        """
        check that each field is in the response, if they aren't then they don't
        need to be updated.

        Also check that the username and email that the user wants to update
        to are not already in use by another user and will throw an error if
        they are.
        """
        if 'username' in self.req:
            if not validate_unique_username(self.req['username']):
                self.user.username = self.req['username']
        if 'email' in self.req:
            if not validate_unique_email(self.req['email']):
                self.user.email = self.req['email']
        if 'password' in self.req:
            self.user.set_password(self.req['password'])

    @jwt_required
    def delete(self, user_id):
        user = get_user(user_id)
        db.session.delete(user)
        if try_commit():
            return success()
        message = {'user': 'Error deleting user'}
        error(500, message)


class Users(Resource):
    def __init__(self):
        self.request = None
        self.req = None
        self.user = None

    @jwt_required
    def get(self):
        users = UserModel.query.all()
        user_schema = UserSchema(exclude=['password'])
        return success(user_schema.dump(users, many=True))

    def post(self):
        """
        Check that the username, and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this check. If this is successful then create the user.
        """
        self.req = request.get_json()
        self.request = request
        validate_form(self.req)
        validate_unique_email(self.req['email'])
        validate_unique_username(self.req['username'])
        validate_password_strength(self.req['password'])
        self._create_user()
        if try_commit():
            self._send_confirmation_email()
            return success({'confirm': 'Please confirm email address'})
        message = {'user': 'Error creating user'}
        error(500, message)

    def _create_user(self):
        """
        We need to exclude the password from the request as it needs to be
        hashed before being saved to the database. We exclude it from the
        marshmallow loads which creates the user model object and then add the
        hashed password to the user object.
        """
        user_schema = UserSchema(exclude=['password'])
        password = self.req['password']
        self.req.pop('password')
        self.user = user_schema.load(self.req, session=db.session)
        self.user.set_password(password)
        db.session.add(self.user)

    def _send_confirmation_email(self):
        """
        Prints the confirmation link to the console for development so we don't
        need an smtp server setup. The send_email function only sends an email
        in production.
        """
        token = generate_confirmation_token(self.user.email)
        confirm_url = self.request.url_root + 'confirm/' + token
        print('\nConfirm URL:')
        print(confirm_url + '\n')
        send_email(self.user.email, 'confirm email', 'confirmation_email.html')
