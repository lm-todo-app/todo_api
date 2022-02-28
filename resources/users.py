from flask import request, jsonify
from flasgger import swag_from
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from models.user import User, UserSchema, jsonify_users
from database import commit_to_db
from authz import has_access, Objects, Actions, Roles
from common.response import success, error, fail
from common.pagination import get_pagination_args, get_sort_by
from apidocs import users as spec
from cache import cache, resource_cache


class UsersResource(Resource):
    """
    API methods that handle the users resource.
    """

    @jwt_required()
    @has_access(Objects.users, Actions.protected)
    @swag_from(spec.users_get)
    @cache.cached(timeout=50)
    def get(self):
        """
        Get all users.
        """
        page, size = get_pagination_args()
        sort = get_sort_by()
        users = User.get_many(sort, page, size)
        if not users:
            fail(404, {"status": "fail", "data": {"Not Found": "No users found."}})
        return success(jsonify_users(users))

    @swag_from(spec.users_post)
    def post(self):
        """
        Check that the username and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this check. If this is successful then create the user.
        """
        form = UserSchema().validate_or_400(request.get_json())
        user = User.create(form)
        user.set_role(Roles.user)
        if commit_to_db():
            user.send_confirmation_email()
            return success({"confirm": "Please confirm email address"})
        error(500, {"user": "Error creating user"})


class UserResource(Resource):
    """
    API methods that handle the user resource.
    """

    @jwt_required()
    @has_access(Objects.users, Actions.read)
    @swag_from(spec.user_get)
    @resource_cache.memoize(timeout=50)
    def get(self, user_id):
        """
        Get user.
        """
        return _get_user(user_id)

    @jwt_required()
    @has_access(Objects.users, Actions.write)
    @swag_from(spec.user_put)
    def put(self, user_id):
        """
        Update user.
        """
        return _update_user(user_id)

    @jwt_required()
    @has_access(Objects.users, Actions.write)
    @swag_from(spec.user_delete)
    def delete(self, user_id):
        """
        Delete user.
        """
        return _delete_user(user_id)


class CurrentUserResource(Resource):
    """
    API methods that handle the user resource for the currently logged in user.
    """

    @jwt_required()
    @swag_from(spec.user_get)
    @resource_cache.memoize(timeout=50)
    def get(self):
        """
        Get current user.
        """
        user_id = get_jwt_identity()
        return _get_user(user_id)

    @jwt_required()
    @swag_from(spec.user_put)
    def put(self):
        """
        Update current user.
        """
        user_id = get_jwt_identity()
        return _update_user(user_id)

    @jwt_required()
    @swag_from(spec.user_delete)
    def delete(self):
        """
        Delete current user.
        """
        user_id = get_jwt_identity()
        return _delete_user(user_id)


def _get_user(user_id):
    user = User.get(user_id)
    return success(user.json())


def _update_user(user_id):
    form = UserSchema().validate_or_400(request.get_json())
    user = User.get(user_id)
    user = user.update(form)
    if commit_to_db():
        return success(user.json())
    error(500, {"user": "Error updating user"})


def _delete_user(user_id):
    user = User.get(user_id)
    caller_id = get_jwt_identity()
    user.delete()
    if commit_to_db():
        resp = jsonify(success())
        # If the user deletes their account then this removes the users
        # access tokens logging them out.
        if user.id == caller_id:
            unset_jwt_cookies(resp)
        return resp
    error(500, {"user": "Error deleting user"})
