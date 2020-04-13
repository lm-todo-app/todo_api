from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User as UserModel
from models.user import UserSchema
from models.db import db

class User(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    def get(self, user_id):
        user = UserModel.query.get(user_id)
        return self.user_schema.dump(user), 200

    def put(self, user_id):
        req = request.get_json()
        errors = self.user_schema.validate(req)
        if errors:
            return 500

        user = UserModel.query.get(user_id)
        user.username = req['username']
        user.email = req['email']
        user.password = req['password']

        try:
            db.session.commit()
        except:
            return {'msg': 'Error updating'}, 500
        return 200

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        db.session.delete(user)

        try:
            db.session.commit()
        except:
            return {'msg': 'Error deleting'}, 500
        return 200


class Users(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    def get(self):
        users = UserModel.query.all()
        return self.user_schema.dump(users, many=True), 200

    def post(self):
        req = request.get_json()
        errors = self.user_schema.validate(req)
        if errors:
            return 500

        password_hash = generate_password_hash(req['password'])

        user = UserModel(
            username=req['username'],
            email=req['email'],
            password=password_hash,
        )
        db.session.add(user)

        try:
            db.session.commit()
        except:
            return {'msg': 'Error saving'}, 500
        return 200
