from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User as UserModel, UserSchema
from common.response import fail
from resources.helpers.user import validate_request

class Login(Resource):
    """
    Returns a login token if the user is valid.
    """
    def post(self):
        """
        Check if the user exists and if their email has been confirmed.
        Check the password and if correct returns an auth token.
        """
        req = request.get_json()
        self.validate_form_authn(req)
        user = UserModel.query.filter_by(email=req['email']).first()
        if not user:
            message = {'user':'User not found'}
            fail(404, message)
        if not user.confirmed_on:
            message = {'form':'Please confirm email'}
            fail(401, message)
        if user and user.check_password(req['password']):
            return self._login_success_response(user), 200
        message = {'form':'Incorrect email address or password'}
        fail(401, message)

    def _login_success_response(self, user):
        """
        Generate a token for the user and return the user info and token.
        """
        email = user.email
        access_token = create_access_token(identity=email)
        user_schema = UserSchema()
        user = user_schema.dump(user)
        return {'user': user, 'accessToken': access_token}

    def validate_form_authn(self, req):
        """
        For auth we only need the email and password to identify a user.
        """
        user_schema = UserSchema(only=['email', 'password'])
        validate_request(req, user_schema)
