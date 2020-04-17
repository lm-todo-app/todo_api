from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def try_commit():
    try:
        db.session.commit()
    except:
        return False
    return True
