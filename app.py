from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from settings import SECRET
from settings import JWT_SECRET
from settings import DEV_DB_URI
from database import db
from database import ma
from resources.users import Users
from resources.token import Auth
from resources.token import Refresh
from resources.token import Remove
from resources.login import Login
from resources.login import ConfirmEmail
from scripts.users import users_script_bp

# TODO: Add password_reset resource.

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(users_script_bp)

v1 = '/api/v1'

app.config['SECRET_KEY'] = SECRET
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_REFRESH_COOKIE_PATH'] = f'{v1}/token/refresh'

app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    db.create_all()

api.add_resource(Users, f'{v1}/users', f'{v1}/users/<user_id>')
api.add_resource(Login, f'{v1}/login')
api.add_resource(Auth, f'{v1}/token/auth')
api.add_resource(Refresh, f'{v1}/token/refresh')
api.add_resource(Remove, f'{v1}/token/remove')
api.add_resource(ConfirmEmail, f'{v1}/confirm/<conf_token>')

if __name__ == '__main__':
    app.run(debug=True)
