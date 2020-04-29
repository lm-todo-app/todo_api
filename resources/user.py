from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db, try_commit
from resources.helpers.user_auth import (login_success_response,
                                         invalid_form,
                                         user_exists_email,
                                         user_exists_username)
from common.message import (error_validating_form,
                            crud_error,
                            email_exists_message,
                            username_exists_message,
                            success, fail, error)

class User(Resource):
    def __init__(self):
        self.req = None
        self.user = None

    @jwt_required
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return fail(404)
        user_schema = UserSchema(exclude=['password'])
        return success(200, user_schema.dump(user))

    @jwt_required
    def put(self, user_id):
        self.req = request.get_json()
        if invalid_form(self.req):
            return error(400, error_validating_form)
        self.user = UserModel.query.get(user_id)
        if not self.user:
            return fail(404)
        self._set_updated_user_values()
        if try_commit():
            return success(200)
        return error(500, crud_error('updating', 'user'))

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
            return fail(404)
        db.session.delete(user)
        if try_commit():
            return success(200)
        return error(500, crud_error('deleting', 'user'))


class Users(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        user_schema = UserSchema(exclude=['password'])
        return success(200, user_schema.dump(users, many=True))

    def post(self):
        req = request.get_json()
        if invalid_form(req):
            return error(400, error_validating_form)
        if user_exists_email(req['email']):
            return fail(409, email_exists_message)
        if user_exists_username(req['username']):
            return fail(409, username_exists_message)
        if ' ' in req['password']:
            return fail(400, {'message': 'spaces are not allowed in password'})
        #TODO: Marshmallow might be able to do the following automatically
        user = UserModel(
            username=req['username'],
            email=req['email'],
        )
        user.set_password(req['password'])
        db.session.add(user)
        if try_commit():
            return login_success_response(user), 200
        return error(500, crud_error('creating', 'user'))
