import httpx
from app.config import settings


class WhatsAppClient:
    def __init__(self):
        self.api_url = settings.WA_API_URL
        self.api_key = settings.API_KEY
        self.headers = {
            "D360-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }

    def send_message(self, to: str, text: str) -> None:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {"body": text},
        }
        with httpx.Client() as client:
            response = client.post(self.api_url, json=payload, headers=self.headers)
            if response.status_code >= 400:
                print(f"Error sending message: {response.text}")
