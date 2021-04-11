from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import unset_jwt_cookies
from flasgger import swag_from
from models.user import User
from models.user import UserSchema
from models.user import create_user
from models.user import delete_user
from models.user import set_updated_user_values
from models.user import validate_create_user_form
from database import try_commit
from common.confirm_email import send_confirmation_email
from common.response import success
from common.response import error
from common.confirm_email import generate_confirmation_token


class UsersResouce(Resource):
    """
    API methods that handle the users resource.
    """
    apidoc_dir = '../apidocs/users'

    @swag_from(f'{apidoc_dir}/get.yml')
    def get(self):
        user_schema = UserSchema()
        users = User.query.all()
        json_users = user_schema.dump(users, many=True)
        return success(json_users)

    @swag_from(f'{apidoc_dir}/post.yml')
    def post(self):
        """
        Check that the username, and email are not already in use by another
        user and check the password strength is sufficient as the average user
        will need this check. If this is successful then create the user.
        """
        user_schema = UserSchema()
        form = user_schema.validate_or_400(request.get_json())
        validate_create_user_form(form)
        user = create_user(form)
        if try_commit():
            token = generate_confirmation_token(user.email)
            send_confirmation_email(user.email, token)
            return success({'confirm': 'Please confirm email address'})
        message = {'user': 'Error creating user'}
        error(500, message)


class UserResource(Resource):
    """
    API methods that handle the user resource.
    """
    apidoc_dir = '../apidocs/user'

    @jwt_required()
    @swag_from(f'{apidoc_dir}/get.yml')
    def get(self, user_id):
        """
        If ID exists get a single user else get all users.
        """
        user_schema = UserSchema()
        # TODO: Error message just says url not found. Might want to say missing user.
        user = User.query.get_or_404(user_id)
        json_user = user_schema.dump(user)
        return success(json_user)

    # TODO: Write tests for updating fields
    # TODO: Check what fields are optional
    @jwt_required()
    @swag_from(f'{apidoc_dir}/put.yml')
    def put(self, user_id):
        """
        Update user.
        """
        user_schema = UserSchema()
        form = user_schema.validate_or_400(request.get_json())
        user = User.query.get_or_404(user_id)
        set_updated_user_values(user, form)
        if try_commit():
            return success()
        message = {'user': 'Error updating user'}
        error(500, message)

    @jwt_required()
    @swag_from(f'{apidoc_dir}/delete.yml')
    def delete(self, user_id):
        """
        Delete user.
        """
        user = User.query.get_or_404(user_id)
        caller_email = get_jwt_identity()
        delete_user(user)
        if try_commit():
            return _logout_user_if_caller_account(caller_email, user)
        message = {'user': 'Error deleting user'}
        error(500, message)


# TODO: Write a test for this scenario - user deleting their own account
def _logout_user_if_caller_account(caller_email, user):
    """
    If the user deletes their account then this removes the users access
    tokens logging them out. Always returns a normal success response.
    """
    resp = jsonify(success())
    if user.email == caller_email:
        unset_jwt_cookies(resp)
    return resp
