from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db, try_commit
from resources.helpers.user_auth import (login_success_response,
                                         invalid_form,
                                         user_exists)
from common.message import (error_validating_form,
                            crud_error,
                            user_exists_message)

class User(Resource):
    @jwt_required
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return 404
        user_schema = UserSchema(exclude=['password'])
        return user_schema.dump(user), 200

    @jwt_required
    def put(self, user_id):
        self.req = request.get_json()
        if invalid_form(self.req):
            return error_validating_form, 500
        self.user = UserModel.query.get(user_id)
        if not self.user:
            return 404
        self._set_updated_user_values()
        if try_commit():
            return 200
        return crud_error('updating', 'user'), 500

    def _set_updated_user_values(self):
        if 'username' in self.req:
            self.user.username = self.req['username']
        if 'email' in self.req:
            if not user_exists(req['email']):
                self.user.email = self.req['email']
        if 'password' in self.req:
            self.user.set_password(self.req['password'])

    @jwt_required
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return 404
        db.session.delete(user)
        if try_commit():
            return 200
        return crud_error('deleting', 'user'), 500


class Users(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        if not users:
            return 404
        user_schema = UserSchema(exclude=['password'])
        return user_schema.dump(users, many=True), 200

    def post(self):
        req = request.get_json()
        if invalid_form(req):
            return error_validating_form, 500
        if user_exists(req['email']):
            return user_exists_message, 500
        #TODO: Marshmallow might be able to do the following automatically
        user = UserModel(
            username=req['username'],
            email=req['email'],
        )
        user.set_password(req['password'])
        db.session.add(user)
        if try_commit():
            return login_success_response(user), 200
        return crud_error('creating', 'user'), 500
