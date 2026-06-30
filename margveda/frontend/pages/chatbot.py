import reflex as rx

from components.chatbot import chatbot_panel
from components.layout import page_header, page_shell
from components.theme import DANGER
from states.chatbot_state import ChatbotState


def chatbot_page() -> rx.Component:
    return page_shell(
        page_header("AI chatbot", "Ask Career Brownie AI", "Career questions, roadmap ideas, college suggestions, and skill planning in one assistant."),
        chatbot_panel(),
        rx.cond(ChatbotState.error != "", rx.text(ChatbotState.error, color=DANGER)),
    )
