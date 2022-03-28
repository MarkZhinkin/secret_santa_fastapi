from python_http_client.client import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.core.config import settings
from app.helpers.random_codes_generator import generate_random_hash, generate_confirmation_code


class SendgridPostOffice:
    def __init__(self):
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    def email_confirmation_send_message(self, send_to: str) -> tuple:
        confirmation_code = generate_confirmation_code()
        message_uid = generate_random_hash()

        # ToDo Add template manager

        message_response = self.send_message(
            send_to,
            confirmation_code
        )

        return message_response.status_code, confirmation_code, message_uid

    def send_message(self, send_to: str, html_content: str) -> Response:
        message_obj = Mail(
            from_email=self.from_email,
            to_emails=send_to,
            subject="Your email confirmation",
            html_content=html_content,
        )
        return self.client.send(message_obj)
