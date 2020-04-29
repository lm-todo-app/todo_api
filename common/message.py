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

# functions below are the standard responses, this needs to be turned into a
# class and used for standard returns anywhere.

# the standard is called 'jsend' with the addition that a http status code will
# also be returned with the response.

# TODO: Add example comments for these.

def success(status_code, data=None):
    return {
        'status': 'success',
        'data': data
    }, status_code

def fail(status_code, data=None):
    return {
        'status': 'fail',
        'data': data
    }, status_code

def error(status_code, message, data=None):
    return {
        'status': 'error',
        'message': message,
        'data': data
    }, status_code
