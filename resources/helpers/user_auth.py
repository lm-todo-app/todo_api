from flask import abort
from flask_jwt_extended import create_access_token
from models.user import User as UserModel
from models.user import UserSchema

def login_success_response(user):
    email = user.email
    access_token = create_access_token(identity=email)
    user_schema = UserSchema(exclude=['password'])
    user_json = user_schema.dump(user)
    return {'user': user_json, 'access_token': access_token}

def invalid_form_exclude_username(req):
    user_schema = UserSchema(exclude=['username'])
    errors = user_schema.validate(req)
    return bool(errors)

def validate_form(req):
    user_schema = UserSchema()
    errors = user_schema.validate(req)
    if errors:
        message = {'form': 'Error validating form'}
        abort(400, message)

def validate_unique_email(email):
    user = UserModel.query.filter_by(email=email).first()
    if user:
        message = {'user': 'User already exists with this email'}
        abort(409, message)

def validate_unique_username(username):
    user = UserModel.query.filter_by(username=username).first()
    if user:
        message = {'user': 'User already exists with this username'}
        abort(409, message)

def get_user(user_id):
    """
    Leaving this here instead of moving this to the model because it uses flask
    abort and we don't want the model methods to use that.
    """
    user = UserModel.query.get(user_id)
    if not user:
        message = {'user': 'User does not exist'}
        abort(404, message)
    return user

def validate_password_strength(password):
    if ' ' in password:
        message = {'form': 'Spaces are not allowed in password'}
        abort(400, message)
