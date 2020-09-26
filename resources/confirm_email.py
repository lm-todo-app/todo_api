from datetime import datetime
from flask_restful import Resource
from models.user import User as UserModel
from common.response import fail, success
from database import db
from resources.helpers.confirm_email import confirm_token

class ConfirmEmail(Resource):
    """
    Check if the user has confirmed their email address.
    A user who has not confrimed their email address is not able to login.
    """
    def get(self, conf_token):
        """
        Check the token and if the user still exists or has not previously
        confirmed their token.
        """
        email = confirm_token(conf_token)
        if email is None:
            message = {'form':'Account with this email address does not exist'}
            fail(401, message)
        user = UserModel.query.filter_by(email=email).first_or_404()
        if not user:
            message = {'user':'User not found'}
            fail(404, message)
        if user.confirmed_on:
            message = {'form':'Account already confirmed. Please login.'}
            fail(400, message)
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        return success({'confirm': 'You have confirmed your account.'})

    #  TODO: post should generate a new confirmation token and accept email
    # address as a value.
