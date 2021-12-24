from flask import request, jsonify
from flasgger import swag_from
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from models.user import (
    User,
    UserSchema,
    create_user,
    delete_user,
    set_updated_user_values,
    validate_create_user_form,
    jsonify_users,
)
from database import commit_to_db
from common.confirm_email import send_confirmation_email
from common.response import success, error
from common.confirm_email import generate_confirmation_token
from common.auth import validate_caller, id_or_400
from apidocs import users as spec
from cache import cache, resource_cache

not_found = {"status": "fail", "data": {"Not Found": "User does not exist"}}


class UsersResource(Resource):
    """
    API methods that handle the users resource.
    """

    @jwt_required()
    @swag_from(spec.users_get)
    @cache.cached(timeout=50)
    def get(self):
        """
        Get all users.
        """
        users = User.query.all()
        return success(jsonify_users(users))

    @swag_from(spec.users_post)
    def post(self):
        """
        Check that the username and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this check. If this is successful then create the user.
        """
        form = UserSchema().validate_or_400(request.get_json())
        validate_create_user_form(form)
        user = create_user(form)
        if commit_to_db():
            token = generate_confirmation_token(user.email)
            send_confirmation_email(user.email, token)
            return success({"confirm": "Please confirm email address"})
        error(500, {"user": "Error creating user"})


class UserResource(Resource):
    """
    API methods that handle the user resource.
    """

    @jwt_required()
    @swag_from(spec.user_get)
    @id_or_400
    @validate_caller
    @resource_cache.memoize(timeout=50)
    def get(self, user_id):
        """
        If ID exists get a single user.
        """
        user = User.query.get_or_404(user_id, not_found)
        return success(user.json())

    @jwt_required()
    @swag_from(spec.user_put)
    @id_or_400
    @validate_caller
    def put(self, user_id):
        """
        Update user.
        """
        form = UserSchema().validate_or_400(request.get_json())
        user = User.query.get_or_404(user_id, not_found)
        user = set_updated_user_values(user, form)
        if commit_to_db():
            return success(user.json())
        error(500, {"user": "Error updating user"})

    @jwt_required()
    @swag_from(spec.user_delete)
    @id_or_400
    @validate_caller
    def delete(self, user_id):
        """
        Delete user.
        """
        user = User.query.get_or_404(user_id, not_found)
        caller_id = get_jwt_identity()
        delete_user(user)
        if commit_to_db():
            resp = jsonify(success())
            # If the user deletes their account then this removes the users
            # access tokens logging them out.
            if user.id == caller_id:
                unset_jwt_cookies(resp)
            return resp
        error(500, {"user": "Error deleting user"})
