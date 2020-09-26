"""
Constants for app.
"""
import os

ENVIRONMENT = os.environ['FLASK_ENV']

SECRET = os.environ['todo_api_secret']
JWT_SECRET = os.environ['todo_api_jwt_secret']

if ENVIRONMENT == 'development':
    DEV_DB_URI = 'sqlite:////tmp/todo_dev.db'
elif ENVIRONMENT == 'production':
    # MySQL connection required
    DEV_DB_URI = os.environ['todo_api_db_uri']
else:
    raise ValueError('Environment is not set properly, see settings file.')

TEST_DB_URI = 'sqlite:////tmp/todo_test.db'
