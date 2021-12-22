""" Authn and Authz functions. """

from functools import wraps
from flask_jwt_extended import get_jwt_identity


def validate_caller(f):
    """
    If "me" is passed to the user_id field instead of the user ID and the
    jwt_required() is called before this decorator then this will set the
    user_id field as the current users ID.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if kwargs.get("user_id") == "me":
            kwargs["user_id"] = get_jwt_identity()
        return f(*args, **kwargs)

    return wrapper
