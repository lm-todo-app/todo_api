from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user import User
from models.user import UserSchema
from database import db, try_commit
from mail import send_email
from common.response import success, error, fail
from common.confirm_email import generate_confirmation_token
from common.user import (
    validate_form,
    get_user,
    validate_password_strength,
    validate_unique_email,
    validate_unique_username
)


class Users(Resource):
    """
    API methods that handle the users resource.
    """
    def __init__(self):
        self.form = None
        self.user = None
        self.user_schema = UserSchema()

    @jwt_required()
    def get(self, user_id=None):
        """
        If ID exists get a single user else get all users.
        """
        if user_id is None:
            return self._get_users()
        return self._get_user(user_id)

    @jwt_required()
    def put(self, user_id):
        """
        Update user.
        """
        self.form = request.get_json()
        validate_form(self.form, self.user_schema)
        self.user = get_user(user_id)
        self._set_updated_user_values()
        if try_commit():
            return success()
        message = {'user': 'Error updating user'}
        error(500, message)

    @jwt_required()
    def delete(self, user_id):
        """
        Delete user.
        """
        # TODO: Need to remove token if user is logged in.
        user = get_user(user_id)
        db.session.delete(user)
        if try_commit():
            return success()
        message = {'user': 'Error deleting user'}
        error(500, message)

    def post(self):
        """
        Check that the username, and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this check. If this is successful then create the user.
        """
        self.form = request.get_json()
        validate_form(self.form, self.user_schema)

        # TODO: Might be able to move this check to pre_load
        # Password is required here but is not required by marshmallow because
        # it is load only so we need to check the field exists here instead.
        if not self.form.get('password'):
            fail(400, {'form':{'password': 'password field is required'}})

        validate_unique_email(self.form['email'])
        validate_unique_username(self.form['username'])
        validate_password_strength(self.form['password'])
        self._create_user()
        if try_commit():
            # TODO: Move this url to settings.
            url = f'{request.url_root}api/v1/confirm/'
            self._send_confirmation_email(url)
            return success({'confirm': 'Please confirm email address'})
        message = {'user': 'Error creating user'}
        error(500, message)

    def _set_updated_user_values(self):
        """
        check that each field is in the response, if they aren't then they don't
        need to be updated.

        Also check that the username and email that the user wants to update
        to are not already in use by another user and will throw an error if
        they are.
        """
        if 'username' in self.form:
            if not validate_unique_username(self.form['username']):
                self.user.username = self.form['username']
        if 'email' in self.form:
            if not validate_unique_email(self.form['email']):
                self.user.email = self.form['email']
        if 'password' in self.form:
            self.user.set_password(self.form['password'])

    def _get_user(self, user_id):
        """
        Get a single user.
        """
        user = get_user(user_id)
        json_user = self.user_schema.dump(user)
        return success(json_user)

    def _get_users(self):
        """
        Get all users.
        """
        users = User.query.all()
        json_users = self.user_schema.dump(users, many=True)
        return success(json_users)

    def _create_user(self):
        """
        We need to exclude the password from the request as it needs to be
        hashed before being saved to the database. We exclude it from the
        marshmallow loads which creates the user model object and then add the
        hashed password to the user object.
        """
        password = self.form.pop('password')
        self.user = self.user_schema.load(self.form, session=db.session)
        self.user.set_password(password)
        db.session.add(self.user)

    # TODO: This should be moved to the common confirm email and used by
    # resource confirm post method.
    # Needs url and email params
    def _send_confirmation_email(self, url):
        """
        Sends a confirmation email to the user.

        Prints the confirmation link to the console for development so we don't
        need an smtp server setup. The send_email function only sends an email
        in production.
        """
        token = generate_confirmation_token(self.user.email)
        confirm_url = url + token
        print('\nConfirm URL:')
        print(confirm_url + '\n')
        send_email(self.user.email, 'confirm email', 'confirmation_email.html')
