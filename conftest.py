"""
Test settings and configuration.
"""
import pytest
from app import app
from database import db
from settings import TEST_DB_URI


@pytest.fixture
def client():
    """
    Create a test database and use the flask context to allow requests.
    """
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
