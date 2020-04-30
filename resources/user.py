from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db, try_commit
from common.response import success, fail, error
from resources.helpers.user_auth import (login_success_response,
                                         invalid_form,
                                         user_exists_email,
                                         user_exists_username)

class User(Resource):
    def __init__(self):
        self.req = None
        self.user = None

    @jwt_required
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            message = {'user': 'User does not exist'}
            return fail(message), 404
        user_schema = UserSchema(exclude=['password'])
        return success(user_schema.dump(user))

    @jwt_required
    def put(self, user_id):
        self.req = request.get_json()
        if invalid_form(self.req):
            message = {'form': 'Error validating form'}
            return fail(message), 400
        self.user = UserModel.query.get(user_id)
        if not self.user:
            message = {'user': 'User does not exist'}
            return fail(message), 404
        self._set_updated_user_values()
        if try_commit():
            return success()
        message = {'user': 'Error updating user'}
        return error(message), 500

    def _set_updated_user_values(self):
        if 'username' in self.req:
            if not user_exists_username(self.req['username']):
                self.user.username = self.req['username']
        if 'email' in self.req:
            if not user_exists_email(self.req['email']):
                self.user.email = self.req['email']
        if 'password' in self.req:
            self.user.set_password(self.req['password'])

    @jwt_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            message = {'user': 'User does not exist'}
            return fail(message), 404
        db.session.delete(user)
        if try_commit():
            return success()
        message = {'user': 'Error deleting user'}
        return error(message), 500


class Users(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        user_schema = UserSchema(exclude=['password'])
        return success(user_schema.dump(users, many=True))

    def post(self):
        req = request.get_json()
        if invalid_form(req):
            message = {'form': 'Error validating form'}
            return error(message), 400
        if user_exists_email(req['email']):
            message = {'user': 'User already exists with this email'}
            return fail(message), 409
        if user_exists_username(req['username']):
            message = {'user': 'User already exists with this username'}
            return fail(message), 409
        if ' ' in req['password']:
            message = {'form': 'Spaces are not allowed in password'}
            return fail(message), 400
        user = UserModel.create_user(req)
        db.session.add(user)
        if try_commit():
            return login_success_response(user), 200
        message = {'user': 'Error creating user'}
        return error(message), 500
