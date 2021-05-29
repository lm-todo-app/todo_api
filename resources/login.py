from datetime import datetime
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import set_refresh_cookies
from database import db
from models.user import User
from models.user import UserSchema
from common.confirm_email import confirm_token
# from common.user import validate_form
from common.response import fail
from common.response import success


class Login(Resource):
    """
    Handle login for user.
    """
    def post(self):
        """
        Check if the user exists and if their email has been confirmed.
        Check the password and if correct returns an auth cookie.

        For auth we only need the email and password to identify a user.
        """
        user_schema = UserSchema(only=['email', 'password'])
        form = user_schema.validate_or_400(request.get_json())
        email = form['email']
        password = form['password']
        user = User.query.filter_by(email=email).first()
        # Check the email and password are correct.
        if not user or not user.check_password(password):
            message = {'form':'Incorrect email address or password'}
            fail(401, message)
        # Check the user has confirmed their email.
        if not user.confirmed_on:
            message = {'form':'Please confirm email'}
            fail(401, message)
        return _login_success_response(user)


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


def _login_success_response(user):
    """
    Generate tokens for the user and return the user info with cookies for
    auth, refresh and csrf.
    """
    additional_claims = {"email": user.email}
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        additional_claims=additional_claims
    )
    user_schema = UserSchema()
    resp = jsonify({'user': user_schema.dump(user)})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp
