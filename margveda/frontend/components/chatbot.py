import reflex as rx

from components.forms import primary_button, text_area
from components.theme import MUTED, panel_style
from states.chatbot_state import ChatbotState


def chatbot_panel() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                text_area("message", "Ask about careers, colleges, skills, or roadmaps..."),
                primary_button("Send message"),
                spacing="3",
            ),
            on_submit=ChatbotState.send_message,
            width="100%",
        ),
        rx.cond(
            ChatbotState.reply != "",
            rx.vstack(
                rx.text("MargVedA AI", color="#27e0ff", font_weight="900"),
                rx.text(ChatbotState.reply, color="#e5f4ff", line_height="1.7"),
                rx.foreach(
                    ChatbotState.suggested_actions,
                    lambda action: rx.text("• ", action, color=MUTED),
                ),
                align_items="start",
                spacing="2",
                padding="18px",
                **panel_style(),
            ),
        ),
        spacing="4",
        width="100%",
    )
