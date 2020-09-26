"""
Initialise SQLAlchemy and Marshmallow here to avoid circular import issues.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def try_commit():
    """
    Common commit action used after changes have been made to the database.
    """
    try:
        db.session.commit()
    except SQLAlchemyError:
        return False
    return True
