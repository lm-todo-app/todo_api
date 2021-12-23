"""
Test settings and configuration.
"""

# Change the dev db to the test db so that when app is imported it doesn't try
# and create a dev or prod db.
import settings

settings.DB_URI = settings.TEST_DB_URI
settings.USE_CACHE = False

import pytest
from app import app
from database import db


@pytest.fixture
def client():
    """
    Create a test database and use the flask context to allow requests.
    """
    app.config["TESTING"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.TEST_DB_URI
    with app.test_client() as client:  # pylint: disable=redefined-outer-name
        with app.app_context():
            db.create_all()
            yield client
