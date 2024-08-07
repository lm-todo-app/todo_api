import json
from flask import Flask
from werkzeug.exceptions import HTTPException
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger
from werkzeug.exceptions import HTTPException
from settings import SECRET, JWT_SECRET, DB_URI, SALT
from database import db, ma, create_db
from resources import users, token, login
from scripts.users import users_cli
from cache import cache, resource_cache
import authz

# TODO: Add password_reset resource.

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# cli
app.cli.add_command(users_cli)

# apidocs
docs = Swagger(app)

v1 = "/api/v1"

app.config["SECRET_KEY"] = SECRET
app.config["JWT_SECRET_KEY"] = JWT_SECRET
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_REFRESH_COOKIE_PATH"] = f"{v1}/token/refresh"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECURITY_PASSWORD_SALT"] = SALT

with app.app_context():
    db.init_app(app)
    create_db(db.engine)
    ma.init_app(app)
    cache.init_app(app)
    resource_cache.init_app(app)
    db.create_all()

api.add_resource(users.UsersResource, f"{v1}/users")
api.add_resource(users.UserResource, f"{v1}/users/<int:user_id>")
api.add_resource(users.CurrentUserResource, f"{v1}/users/current")
api.add_resource(login.Login, f"{v1}/login")
api.add_resource(token.Auth, f"{v1}/token/auth")
api.add_resource(token.Refresh, f"{v1}/token/refresh")
api.add_resource(token.Remove, f"{v1}/token/remove")
api.add_resource(login.ConfirmEmail, f"{v1}/confirm/<conf_token>")

authz.init()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)