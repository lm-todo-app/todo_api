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

SALT = "salt"
#  SALT = app.config['SECURITY_PASSWORD_SALT']

if ENVIRONMENT == "development":
    DEV_DB_URI = "sqlite:////tmp/todo_dev.db"

elif ENVIRONMENT == "production":
    DEV_DB_URI = os.environ["todo_api_db_uri"]

else:
    raise ValueError("Environment is not set properly, see settings file.")
