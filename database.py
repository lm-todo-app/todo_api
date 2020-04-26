from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def try_commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        return False
    return True
