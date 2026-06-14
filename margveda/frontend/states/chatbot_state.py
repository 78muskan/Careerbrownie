import reflex as rx

from services.api_client import api_request


class ChatbotState(rx.State):
    token: str = rx.LocalStorage("", name="margveda_token")
    reply: str = ""
    suggested_actions: list[str] = []
    error: str = ""

    def send_message(self, form_data: dict):
        try:
            data = api_request(
                "POST",
                "/chatbot/message",
                {"message": form_data.get("message", "")},
                token=self.token,
            )
            self.reply = data.get("reply", "")
            self.suggested_actions = data.get("suggested_actions", [])
            self.error = ""
        except ValueError as exc:
            self.error = str(exc)
