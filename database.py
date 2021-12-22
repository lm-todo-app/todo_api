"""
Initialise SQLAlchemy and Marshmallow here to avoid circular import issues.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_marshmallow import Marshmallow
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
ma = Marshmallow()


def commit_to_db():
    """
    Common commit action used after changes have been made to the database.
    """
    try:
        db.session.commit()
    except SQLAlchemyError:
        return False
    return True


def create_db(engine):
    """
    Create the database if it doesn't exist
    """
    if not database_exists(engine.url):
        create_database(engine.url)
