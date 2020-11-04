from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from settings import SECRET, JWT_SECRET, DEV_DB_URI
from mail import mail
from database import db, ma
from resources.user import Users
from resources.token import Auth
from resources.token import Refresh
from resources.token import Remove
from resources.login import Login
from resources.confirm_email import ConfirmEmail
# TODO: Add password_reset resource.

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = SECRET
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    db.create_all()

api.add_resource(Users, '/users', endpoint='users')
api.add_resource(Users, '/users/<user_id>', endpoint='user')
api.add_resource(Login, '/login')
api.add_resource(Auth, '/token/auth')
api.add_resource(Refresh, '/token/refresh')
api.add_resource(Remove, '/token/remove')
api.add_resource(ConfirmEmail, '/confirm/<conf_token>')

if __name__ == '__main__':
    app.run(debug=True)
