from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from models.db import db

class User(Resource):
    @jwt_required
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        user_schema = UserSchema(exclude=['password'])
        return user_schema.dump(user), 200

    @jwt_required
    def put(self, user_id):
        req = request.get_json()
        user_schema = UserSchema()
        errors = user_schema.validate(req)
        if errors:
            return {'msg': 'Error validating form'}, 500

        user = UserModel.query.get(user_id)

        if req['username']:
            user.username = req['username']
        if req['email']:
            user.email = req['email']
        if req['password']:
            user.set_password(req['password'])

        try:
            db.session.commit()
        except:
            return {'msg': 'Error updating user'}, 500
        return 200

    @jwt_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            return {'msg': 'Error deleting user'}, 500
        return 200


class Users(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        user_schema = UserSchema(exclude=['password'])
        return user_schema.dump(users, many=True), 200

    def post(self):
        req = request.get_json()
        user_schema = UserSchema()
        errors = user_schema.validate(req)
        user_exists = UserModel.query.filter_by(email=req['email']).first()
        if user_exists:
            return {'msg': 'User already exists with that email address'}, 500
        if errors:
            return {'msg': 'Error validating form'}, 500
        user = UserModel(
            username=req['username'],
            email=req['email'],
        )
        user.set_password(req['password'])
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return {'msg': 'Error creating user'}, 500
        access_token = create_access_token(identity=user.email)
        user_schema = UserSchema(exclude=['password'])
        user_json = user_schema.dump(user)
        return {'user': user_json, 'access_token': access_token}, 200
