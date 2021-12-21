from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger
from settings import SECRET, JWT_SECRET, DEV_DB_URI
from database import db, ma, create_db
from resources import users, token, login
from scripts.users import users_cli


# TODO: Add password_reset resource.

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# cli
app.cli.add_command(users_cli)

# apidocs
docs = Swagger(app)

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
    create_db(db.engine)
    ma.init_app(app)
    db.create_all()

api.add_resource(users.UsersResource, f'{v1}/users')
api.add_resource(users.UserResource, f'{v1}/users/<user_id>')
api.add_resource(login.Login, f'{v1}/login')
api.add_resource(token.Auth, f'{v1}/token/auth')
api.add_resource(token.Refresh, f'{v1}/token/refresh')
api.add_resource(token.Remove, f'{v1}/token/remove')
api.add_resource(login.ConfirmEmail, f'{v1}/confirm/<conf_token>')

if __name__ == '__main__':
    app.run(debug=True)
