from flask_mail import Mail, Message
from settings import ENVIRONMENT

mail = Mail()

# move to settings
SENDER = 'hello@world.com'

def send_email(to, subject, template):
    if ENVIRONMENT == 'production':
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            #  sender=app.config['MAIL_DEFAULT_SENDER']
            sender=SENDER
        )
        print(msg)
        mail.send(msg)
