from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from models.db import db, ma
from resources.user import Users, User

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    ma.init_app(app)
    db.create_all()

api.add_resource(Users, '/user')
api.add_resource(User, '/user/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
