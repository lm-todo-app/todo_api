from flask_jwt_extended import create_access_token
from models.user import User as UserModel
from models.user import UserSchema

def login_success_response(user):
    email = user.email
    access_token = create_access_token(identity=email)
    user_schema = UserSchema(exclude=['password'])
    user_json = user_schema.dump(user)
    return {'user': user_json, 'access_token': access_token}, 200

def invalid_form(req):
    user_schema = UserSchema()
    errors = user_schema.validate(req)
    return True if errors else False

def user_exists(email):
    user = UserModel.query.filter_by(email=email).first()
    return True if user else False
