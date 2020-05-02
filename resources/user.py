from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.user import User as UserModel
from models.user import UserSchema
from database import db, try_commit
from common.response import success, error
from resources.helpers.user_auth import (
    login_success_response,
    validate_form,
    get_user,
    validate_password_strength,
    validate_unique_email,
    validate_unique_username
)

class User(Resource):
    def __init__(self):
        self.req = None
        self.user = None

    @jwt_required
    def get(self, user_id):
        user = get_user(user_id)
        user_schema = UserSchema(exclude=['password'])
        return success(user_schema.dump(user))

    @jwt_required
    def put(self, user_id):
        self.req = request.get_json()
        validate_form(self.req)
        self.user = get_user(user_id)
        self._set_updated_user_values()
        if try_commit():
            return success()
        message = {'user': 'Error updating user'}
        return error(message), 500

    def _set_updated_user_values(self):
        """
        check that each field is in the response, if they aren't then they don't
        need to be updated.

        Also check that the username and email that the user wants to update
        to are not already in use by another user and will throw an error if
        they are.
        """
        if 'username' in self.req:
            if not validate_unique_username(self.req['username']):
                self.user.username = self.req['username']
        if 'email' in self.req:
            if not validate_unique_email(self.req['email']):
                self.user.email = self.req['email']
        if 'password' in self.req:
            self.user.set_password(self.req['password'])

    @jwt_required
    def delete(self, user_id):
        user = get_user(user_id)
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
        """
        Check that the username, and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this feature. If this is successful then create the user.
        """
        req = request.get_json()
        validate_form(req)
        validate_unique_email(req['email'])
        validate_unique_username(req['username'])
        validate_password_strength(req['password'])
        user = UserModel.create_user(req)
        db.session.add(user)
        try_commit()
        if try_commit():
            return login_success_response(user), 200
        message = {'user': 'Error creating user'}
        return error(message), 500
