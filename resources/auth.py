from datetime import datetime
from flask import request
from flask_restful import Resource
from models.user import User as UserModel
from common.response import fail, success
from database import db
from resources.helpers.confirm import confirm_token
from resources.helpers.user_auth import (
    login_success_response,
    validate_form_exclude_username
)

class Auth(Resource):
    def post(self):
        req = request.get_json()
        validate_form_exclude_username(req)
        user = UserModel.query.filter_by(email=req['email']).first()
        if not user:
            message = {'user':'User not found'}
            fail(404, message)
        if not user.confirmed_on:
            message = {'form':'Please confirm email'}
            fail(401, message)
        if user and user.check_password(req['password']):
            return login_success_response(user), 200
        message = {'form':'Incorrect email address or password'}
        fail(401, message)


class ConfirmEmail(Resource):
    def get(self, conf_token):
        try:
            email = confirm_token(conf_token)
        except:
            message = {'form':'Incorrect email address or password'}
            fail(401, message)
        user = UserModel.query.filter_by(email=email).first_or_404()
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
