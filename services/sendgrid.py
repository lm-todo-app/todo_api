import os
from settings import SENDGRID_SENDER, SENDGRID_API_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Message():
    sender = SENDGRID_SENDER

    def __init__(self, contact, template_id, template_data=None):
        self.contact = contact
        self.template_id = template_id
        self.template_data = template_data

    def create(self):
        message = Mail(
            from_email=Message.sender,
            to_emails=self.contact,
        )
        message.dynamic_template_data = self.template_data
        message.template_id = self.template_id
        return message


class SendgridService():
    key = SENDGRID_API_KEY
    def __init__(self):
        self.client = SendGridAPIClient(SendgridService.key)

    def send(self, message):
        try:
            response = self.client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
