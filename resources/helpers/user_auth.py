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

def invalid_form(req):
    user_schema = UserSchema()
    errors = user_schema.validate(req)
    return bool(errors)

def user_exists_email(email):
    user = UserModel.query.filter_by(email=email).first()
    return bool(user)

def user_exists_username(username):
    user = UserModel.query.filter_by(username=username).first()
    return bool(user)
