from settings import TEST_DB_URI
from app import app
from database import db
import pytest

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
