import requests

from django.conf import settings


class BrevoEmailService:
    URL = "https://api.brevo.com/v3/smtp/email"

    @classmethod
    def send_email(
        cls,
        subject,
        html_content,
        recipients,
    ):
        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        }

        payload = {
            "sender": {
                "email": settings.DEFAULT_FROM_EMAIL,
            },
            "to": [
                {"email": email}
                for email in recipients
            ],
            "subject": subject,
            "htmlContent": html_content,
        }

        response = requests.post(
            cls.URL,
            json=payload,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()