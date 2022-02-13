from functools import wraps
import casbin
import casbin_sqlalchemy_adapter
from flask_jwt_extended import get_jwt
from common.response import fail
from settings import DB_URI

adapter = casbin_sqlalchemy_adapter.Adapter(DB_URI)
e = casbin.Enforcer("model.conf", adapter)


class Roles:
    superadmin = "superadmin"
    user = "user"


class Objects:
    users = "users"


class Actions:
    read = "read"
    write = "write"


POLICIES = [
    # We Need to include one policy for superadmin to allow them to have access
    # to all policies by default.
    [Roles.superadmin, Objects.users, Actions.read],
    [Roles.superadmin, Objects.users, Actions.write],

    [Roles.user, Objects.users, Actions.read],
    # [Roles.user, Objects.users, Actions.write],
]


def init():
    e.add_named_policies("p", POLICIES)


def has_access(obj, act):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            email = get_jwt()["email"]
            # __import__('pdb').set_trace()
            if not e.enforce(email, obj, act):
                fail(403, {"Forbidden": f"Permission denied for {obj}:{act}"})
            return f(*args, **kwargs)

        return wrapper

    return decorator
