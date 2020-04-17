from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User as UserModel
from models.user import UserSchema
from common.message import error_message, incorrect_credentials
from resources.helpers.user_auth import login_success_response, invalid_form

class Auth(Resource):
    def post(self):
        req = request.get_json()
        if invalid_form(req):
            return incorrect_credentials, 500
        user = UserModel.query.filter_by(email=req['email']).first()
        if user and user.check_password(req['password']):
            return login_success_response(user)
        return incorrect_credentials, 401
