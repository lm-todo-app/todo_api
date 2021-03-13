from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

# TODO: Unit tests.

class Auth(Resource):
    """
    Handle authentication for user.
    """
    @jwt_required()
    def post(self):
        """
        Check if JWT is valid.
        """
        user = get_jwt_identity()
        return jsonify(logged_in_as=user)


class Refresh(Resource):
    """
    Refresh an access token.
    """
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh access tokens without changing refresh tokens.
        """
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return resp


class Remove(Resource):
    """
    Handle logging out user.
    """
    def post(self):
        """
        Remove cookies.
        """
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp
