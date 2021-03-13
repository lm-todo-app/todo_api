from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from flasgger import swag_from
from models.user import User
from models.user import UserSchema
from database import db
from database import try_commit
from common.confirm_email import send_confirmation_email
from common.response import success
from common.response import error
from common.response import fail
from common.confirm_email import generate_confirmation_token
from common.user import validate_form
from common.user import get_user
from common.user import validate_password_strength
from common.user import validate_unique_email
from common.user import validate_unique_username


apidoc_dir = '../apidocs/users'

class Users(Resource):
    """
    API methods that handle the users resource.
    """
    def __init__(self):
        self.form = None
        self.user = None
        self.user_schema = UserSchema()

    @jwt_required()
    @swag_from(f'{apidoc_dir}/get.yml')
    def get(self, user_id=None):
        """
        If ID exists get a single user else get all users.
        """
        if user_id is None:
            return self._get_users()
        return self._get_user(user_id)

    # TODO: Write tests for updating fields
    @jwt_required()
    @swag_from(f'{apidoc_dir}/put.yml', endpoint='user')
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
    @swag_from(f'{apidoc_dir}/delete.yml', endpoint='user')
    def delete(self, user_id):
        """
        Delete user.
        """
        self.user = get_user(user_id)
        caller_email = get_jwt_identity()
        db.session.delete(self.user)
        if try_commit():
            return self._logout_user_if_caller_account(caller_email)
        message = {'user': 'Error deleting user'}
        error(500, message)

    # TODO: Write a test for this scenario - user deleting their own account
    def _logout_user_if_caller_account(self, caller_email):
        """
        If the user deletes their account then this removes the users access
        tokens logging them out. Always returns a normal success response.
        """
        resp = jsonify(success())
        if self.user.email == caller_email:
            unset_jwt_cookies(resp)
        return resp


    @swag_from(f'{apidoc_dir}/post.yml', endpoint='users')
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
            token = generate_confirmation_token(self.user.email)
            send_confirmation_email(self.user.email, token)
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
        username = self.form.get('username')
        if username and self.user.username != username:
            if not validate_unique_username(username):
                self.user.username = username

        email = self.form.get('email')
        if email and self.user.email != email:
            if not validate_unique_email(email):
                self.user.email = email

        password = self.form.get('password')
        if password:
            validate_password_strength(password)
            self.user.set_password(password)

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
