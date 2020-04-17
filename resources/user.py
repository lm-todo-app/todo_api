from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db
from common.message import (error_validating_form,
                            crud_error,
                            user_exists_message)

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
            return error_validating_form, 500

        user = UserModel.query.get(user_id)

        if 'username' in req:
            user.username = req['username']
        if 'email' in req:
            user.email = req['email']
        if 'password' in req:
            user.set_password(req['password'])

        try:
            db.session.commit()
        except:
            return crud_error('updating', 'user'), 500
        return 200

    @jwt_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            return crud_error('deleting', 'user'), 500
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
            return user_exists_message, 500
        if errors:
            return error_validating_form, 500
        user = UserModel(
            username=req['username'],
            email=req['email'],
        )
        user.set_password(req['password'])
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return crud_error('creating', 'user'), 500
        access_token = create_access_token(identity=user.email)
        user_schema = UserSchema(exclude=['password'])
        user_json = user_schema.dump(user)
        return {'user': user_json, 'access_token': access_token}, 200
