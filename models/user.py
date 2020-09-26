from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import fields, validate, pre_load
from database import db
from models.helpers.case import CamelCaseSchema

class User(db.Model):
    """
    User model, currently has username and email as unique fields.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(200), unique=False, nullable=True)
    last_name = db.Column(db.String(200), unique=False, nullable=True)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        """
        Generates a password hash using werkzeug security ready to save to the
        database.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the password in the database matches the supplied password.
        """
        return check_password_hash(self.password, password)


class UserSchema(CamelCaseSchema):
    """
    Schema for user validation with API.

    """
    class Meta:
        model = User
        load_instance = True

    email = fields.Email(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    username = fields.Str(
        validate=validate.Length(min=5, max=100),
        required=True
    )

    @pre_load
    def process_input(self, data, **kwargs):
        """
        Before checking for validation strip whitespace from email and username.

        """
        if data.get('email'):
            data["email"] = data["email"].lower().strip()
        if data.get('username'):
            data["username"] = data["username"].strip()
        return data
