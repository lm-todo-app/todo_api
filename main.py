from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models.db import db, ma
from resources.user import Users, User
from resources.auth import Auth

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SECRET_KEY'] = 'secret'
app.config['JWT_SECRET_KEY'] = 'super-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    db.create_all()

api.add_resource(Users, '/user')
api.add_resource(User, '/user/<user_id>')
api.add_resource(Auth, '/auth')

if __name__ == '__main__':
    app.run(debug=True)
