from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from database import db, commit_to_db
from models.user import User, UserSchema
from common.confirm_email import confirm_token
from common.response import fail, success, error


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
        user_schema = UserSchema(only=["email", "password"])
        form = user_schema.validate_or_400(request.get_json())
        user = User.query.filter_by(email=form["email"]).first()
        # Check the email and password are correct.
        if not user or not user.check_password(form["password"]):
            fail(401, {"form": "Incorrect email address or password"})

        # Check the user has confirmed their email.
        if not user.confirmed_on:
            fail(401, {"form": "Please confirm email"})
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
            fail(401, {"form": "Account with this email address does not exist"})
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed_on:
            fail(400, {"form": "Account already confirmed. Please login."})
        user.save_email_confirmation()
        if commit_to_db():
            return success({"confirm": "You have confirmed your account."})
        error(500, {"user": "Error confirming user account"})

    #  TODO: post should generate a new confirmation token and accept email
    # address as an argument.


def _login_success_response(user):
    """
    Generate tokens for the user and return the user info with cookies for
    auth, refresh and csrf.
    """
    additional_claims = {"email": user.email}
    access_token = create_access_token(
        identity=user.id, additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=user.id, additional_claims=additional_claims
    )
    resp = jsonify({"user": user.json()})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp
