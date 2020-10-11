from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User as UserModel, UserSchema
from common.response import fail
from resources.helpers.user import validate_request

class Login(Resource):
    """
    Handle authentication for user.
    """
    def __init__(self):
        self.user = None
        self.request = None

    def post(self):
        """
        Check if the user exists and if their email has been confirmed.
        Check the password and if correct returns an auth token.
        """
        self.request = request.get_json()
        self.validate_form_authn()
        email = self.request['email']
        password = self.request['password']
        self.user = UserModel.query.filter_by(email=email).first()
        # check the email and password are correct
        if not self.user or not self.user.check_password(password):
            message = {'form':'Incorrect email address or password'}
            fail(401, message)
        self.validate_user_email_confirmation()
        return self._login_success_response(), 200

    def _login_success_response(self):
        """
        Generate a token for the user and return the user info and token.
        """
        email = self.user.email
        access_token = create_access_token(identity=email)
        user_schema = UserSchema()
        user = user_schema.dump(self.user)
        return {'user': user, 'accessToken': access_token}

    def validate_form_authn(self):
        """
        For auth we only need the email and password to identify a user.
        """
        user_schema = UserSchema(only=['email', 'password'])
        validate_request(self.request, user_schema)

    def validate_user_email_confirmation(self):
        """
        Check if the user has confirmed their email address.
        """
        if not self.user.confirmed_on:
            message = {'form':'Please confirm email'}
            fail(401, message)

