"""
Sender for email. Used for sending email confirmations.
"""
from flask_mail import Mail, Message
from settings import ENVIRONMENT


mail = Mail()

# move to settings
SENDER = 'hello@world.com'
#  SENDER = app.config['MAIL_DEFAULT_SENDER']

def send_email(to, subject, template):
    """
    Check if production environment and send an email.
    """
    if ENVIRONMENT == 'production':
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=SENDER
        )
        print(msg)
        mail.send(msg)
