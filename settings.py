import os

ENVIRONMENT = os.environ['FLASK_ENV']

# For dev set to 'secret'
SECRET = os.environ['todo_api_secret']

# For dev set to 'secret-key'
JWT_SECRET = os.environ['todo_api_jwt_secret']

if ENVIRONMENT == 'development':
    DEV_DB_URI = 'sqlite:////tmp/todo_dev.db'
elif ENVIRONMENT == 'production':
    # MySQL connection required
    DEV_DB_URI = os.environ['todo_api_db_uri']
else:
    raise ValueError('Environment is not set properly, see settings file.')

TEST_DB_URI = 'sqlite:////tmp/todo_test.db'
