"""
Constants for app.
"""
import os


ENVIRONMENT = os.environ["FLASK_ENV"]

SECRET = os.environ["TODO_API_SECRET"]

JWT_SECRET = os.environ["TODO_API_JWT_SECRET"]

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
    DB_URI = "postgresql://docker:docker@localhost:5434/todo"

elif ENVIRONMENT == "production":
    DB_URI = os.environ["TODO_API_DB_URI"]

else:
    raise ValueError("Environment is not set properly, see settings file.")
