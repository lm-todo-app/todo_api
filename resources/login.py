from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from models.user import User, UserSchema
from common.response import fail, success
from database import db
from common.user import validate_form
from common.confirm_email import confirm_token
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)


class Login(Resource):
    """
    Handle login for user.
    """
    def __init__(self):
        self.form = None
        self.user = None

    def post(self):
        """
        Check if the user exists and if their email has been confirmed.
        Check the password and if correct returns an auth cookie.
        """
        self.form = request.get_json()
        self._validate_form_authn()
        email = self.form['email']
        password = self.form['password']
        self.user = User.query.filter_by(email=email).first()
        # check the email and password are correct
        if not self.user or not self.user.check_password(password):
            message = {'form':'Incorrect email address or password'}
            fail(401, message)
        self._validate_user_email_confirmation()
        return self._login_success_response()

    def _login_success_response(self):
        """
        Generate tokens for the user and return the user info with cookies for
        auth, refresh and csrf.
        """
        email = self.user.email
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        user_schema = UserSchema()
        user = user_schema.dump(self.user)
        resp = jsonify({'user': user})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    def _validate_form_authn(self):
        """
        For auth we only need the email and password to identify a user.
        """
        user_schema = UserSchema(only=['email', 'password'])
        validate_form(self.form, user_schema)

    def _validate_user_email_confirmation(self):
        """
        Check if the user has confirmed their email address.
        """
        if not self.user.confirmed_on:
            message = {'form':'Please confirm email'}
            fail(401, message)


class ConfirmEmail(Resource):
    """
    Check if the user has confirmed their email address.
    A user who has not confrimed their email address is not able to login.
    """
    def get(self, conf_token):
        """
        Check the token and if the user still exists or has not previously
        confirmed their token.
        """
        email = confirm_token(conf_token)
        if email is None:
            message = {'form':'Account with this email address does not exist'}
            fail(401, message)
        user = User.query.filter_by(email=email).first_or_404()
        if not user:
            message = {'user':'User not found'}
            fail(404, message)
        if user.confirmed_on:
            message = {'form':'Account already confirmed. Please login.'}
            fail(400, message)
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        return success({'confirm': 'You have confirmed your account.'})

    #  TODO: post should generate a new confirmation token and accept email
    # address as an argument.
