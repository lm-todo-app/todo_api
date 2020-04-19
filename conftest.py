from settings import TEST_DB_URI
from app import app
from database import db, ma
import pytest

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
    with app.test_client() as client:
        with app.app_context():
            #  db.init_app(app)
            #  ma.init_app(app)
            db.create_all()
            yield client
