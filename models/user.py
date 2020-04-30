from werkzeug.security import generate_password_hash, check_password_hash
from database import db, ma
from marshmallow import fields, validate, pre_load

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def create_user(req):
        """
        Creating user to be saved here instead of using marshmallow so that we
        can set the hashed the password.
        """
        # TODO: Marshmallow may be able to replace this function.
        user = User(
            username=req['username'],
            email=req['email'],
        )
        user.set_password(req['password'])
        return user

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    email = fields.Email(required=True)
    username = fields.Str(
        validate=validate.Length(min=5, max=100),
        required=True
    )
    password = fields.Str(
        validate=validate.Length(min=8, max=100),
        required=True
    )

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get('email'):
            data["email"] = data["email"].lower().strip()
        if data.get('username'):
            data["username"] = data["username"].strip()
        if data.get('password'):
            data["password"] = data["password"].strip()
        return data
