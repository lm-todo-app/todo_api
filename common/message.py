# This can be a class that generates the CRUD errors for a resource
# TODO: Check if marshmallow handles this automatically

def message(msg, *args):
    if args:
        msg = msg.format(*args)
    return {'message': msg}

def crud_error(action, resource):
    actions = ['creating', 'updating', 'deleting', 'reading']
    if action in actions:
        msg = 'Error ' + action + ' {}'
        return message(msg, resource)
    return message('Error')

error_message = message('Error')
error_validating_form = message('Error validating form')
email_exists_message = message('User already exists with that email address')
username_exists_message = message('User already exists with that username')
incorrect_credentials = message('Incorrect email address or password')
