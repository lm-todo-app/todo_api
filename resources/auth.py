from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models.user import User as UserModel
from models.user import UserSchema
from common.message import error_message, incorrect_credentials

class Auth(Resource):
    def post(self):
        req = request.get_json()
        user_schema = UserSchema()
        errors = user_schema.validate(req)
        if errors:
            return error_message, 500
        user = UserModel.query.filter_by(email=req['email']).first()
        if user and user.check_password(req['password']):
            access_token = create_access_token(identity=req['email'])
            user_schema = UserSchema(exclude=['password'])
            user_json = user_schema.dump(user)
            return {'user': user_json, 'access_token': access_token}, 200
        return incorrect_credentials, 401
