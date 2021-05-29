""" Authn and Authz functions. """

from functools import wraps
from flask_jwt_extended import get_jwt_identity

def validate_caller(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.get('user_id') == 'me':
            kwargs['user_id'] = get_jwt_identity()
        return f(*args, **kwargs)
    return wrapper
