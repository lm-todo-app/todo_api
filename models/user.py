from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, validate, pre_load
from database import db
from models.helpers.case import CamelCaseSchema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(200), unique=False, nullable=True)
    last_name = db.Column(db.String(200), unique=False, nullable=True)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(CamelCaseSchema):
    class Meta:
        model = User
        load_instance = True

    email = fields.Email(required=True)
    username = fields.Str(
        validate=validate.Length(min=5, max=100),
        required=True
    )
    first_name = fields.Str()
    last_name = fields.Str()

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get('email'):
            data["email"] = data["email"].lower().strip()
        if data.get('username'):
            data["username"] = data["username"].strip()
        return data
