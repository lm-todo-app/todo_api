from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from settings import SECRET, JWT_SECRET, DEV_DB_URI
from mail import mail
from database import db, ma
from resources.user import Users, User
from resources.auth import Auth, ConfirmEmail

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = SECRET
app.config['JWT_SECRET_KEY'] = JWT_SECRET

app.config['SQLALCHEMY_DATABASE_URI'] = DEV_DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    db.create_all()

api.add_resource(Users, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(Auth, '/auth')
api.add_resource(ConfirmEmail, '/confirm/<conf_token>')

if __name__ == '__main__':
    app.run(debug=True)
