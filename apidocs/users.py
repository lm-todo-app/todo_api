"""
apispec is needed to use marshmallow schemas but it is not necessary to import
it.

Importing anyway to prevent removing the unused package by accident as the error
message is difficult to understand when it is removed.
"""
import apispec  # pylint: disable=unused-import
from models.user import UserSchema


users_get = {
    "responses": {
        200: {"schema": UserSchema},
        401: {"description": "Authorization cookies is missing or invalid"},
    }
}

users_post = {
    "responses": {
        200: {"schema": UserSchema},
        401: {"description": "Authorization cookies is missing or invalid"},
    }
}

user_get = {
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "int",
        }
    ],
    "responses": {
        200: {"schema": UserSchema},
        404: {"description": "User not found"},
        401: {"description": "Authorization cookies is missing or invalid"},
    },
}

user_put = {
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "int",
        }
    ],
    "responses": {
        200: {"schema": UserSchema},
        404: {"description": "User not found"},
        401: {"description": "Authorization cookies is missing or invalid"},
    },
}

user_delete = {
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "int",
        }
    ],
    "responses": {
        200: {"schema": UserSchema},
        404: {"description": "User not found"},
        401: {"description": "Authorization cookies is missing or invalid"},
    },
}
