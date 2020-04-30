from flask import request
from flask_restful import Resource
from models.user import User as UserModel
from common.response import fail
from resources.helpers.user_auth import (login_success_response,
                                         invalid_form_exclude_username)

class Auth(Resource):
    def post(self):
        req = request.get_json()
        if invalid_form_exclude_username(req):
            message = 'Incorrect email address or password'
            return fail(message), 401
        user = UserModel.query.filter_by(email=req['email']).first()
        if user and user.check_password(req['password']):
            return login_success_response(user), 200
        message = 'Incorrect email address or password'
        return fail(message), 401
