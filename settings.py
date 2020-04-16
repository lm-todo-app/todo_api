import os

# Global variable for settings that can't be kept in this file. Use sparingly.
ENVIRONMENT = 'development'

if ENVIRONMENT == 'development':
    # TODO: These can be environment variables like the production setup.
    SECRET =  'secret'
    JWT_SECRET =  'secret-key'
    DEV_DB_URI = 'sqlite:////tmp/todo_dev.db'
    TEST_DB_URI = 'sqlite:////tmp/todo_test.db'

elif ENVIRONMENT == 'production':
    SECRET =  os.environ['todo_api_secret']
    JWT_SECRET =  os.environ['todo_api_jwt_secret']
    DEV_DB_URI = os.environ['todo_api_db_uri']
    TEST_DB_URI = os.environ['todo_api_test_db_uri']

else:
    raise ValueError('Environment is not set properly, see settings file.')
