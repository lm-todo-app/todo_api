"""
Constants for app.
"""
import os


ENVIRONMENT = os.environ["FLASK_ENV"]

SECRET = os.environ["todo_api_secret"]

JWT_SECRET = os.environ["todo_api_jwt_secret"]

SENDGRID_SENDER = os.environ["SENDGRID_SENDER"]

SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

TEST_DB_URI = "sqlite:////tmp/todo_test.db"

APP_URL = os.environ["TODO_APP_URL"]

API_URL = "http://localhost:5000/api"  # TODO Find a better way to do this


USE_CACHE = False
if ENVIRONMENT == "production":
    USE_CACHE = True


SALT = "salt"
if ENVIRONMENT == "production":
    SALT = os.environ["SECURITY_PASSWORD_SALT"]


if ENVIRONMENT == "development":
    # DB_URI = "sqlite:////tmp/todo_dev.db"
    DB_URI = "postgresql://docker:docker@localhost:5433/todo"

elif ENVIRONMENT == "production":
    DB_URI = os.environ["todo_api_db_uri"]

else:
    raise ValueError("Environment is not set properly, see settings file.")
