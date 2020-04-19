import os

ENVIRONMENT = os.environ['FLASK_ENV']

if ENVIRONMENT == 'development':
    # TODO: These can be environment variables like the production setup.
    SECRET = 'secret'
    JWT_SECRET = 'secret-key'
    DEV_DB_URI = 'sqlite:////tmp/todo_dev.db'

elif ENVIRONMENT == 'production':
    SECRET = os.environ['todo_api_secret']
    JWT_SECRET = os.environ['todo_api_jwt_secret']
    # MySQL connection required
    DEV_DB_URI = os.environ['todo_api_db_uri']

elif ENVIRONMENT == 'test':
    SECRET = 'secret'
    JWT_SECRET = 'secret-key'
    DEV_DB_URI = 'sqlite:////tmp/todo_test.db'

else:
    raise ValueError('Environment is not set properly, see settings file.')
