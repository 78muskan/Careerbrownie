import reflex as rx

from services.api import api_client
from states.auth_state import AuthState


class ChatState(rx.State):
    message: str = ""
    messages: list[dict[str, str]] = [
        {
            "role": "assistant",
            "content": "Welcome to Career Brownie. Ask about careers, colleges, skills, or roadmaps.",
        }
    ]
    is_loading: bool = False

    async def send_message(self):
        if not self.message.strip():
            return

        user_message = self.message.strip()
        self.messages.append({"role": "student", "content": user_message})
        self.message = ""
        self.is_loading = True
        auth = await self.get_state(AuthState)
        try:
            data = await api_client.post(
                "/chatbot/message",
                token=auth.token,
                json={"message": user_message, "context": {}},
            )
            self.messages.append({"role": "assistant", "content": data.get("reply", "")})
        except Exception:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": "I could not reach the guidance API yet. Your message is saved in this session.",
                }
            )
        finally:
            self.is_loading = False
