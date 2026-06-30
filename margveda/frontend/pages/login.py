import reflex as rx

from components.forms import primary_button, text_input
from components.layout import page_header, page_shell
from components.theme import DANGER, SUCCESS, panel_style
from states.auth_state import AuthState


def login_page() -> rx.Component:
    return page_shell(
        rx.center(
            rx.vstack(
                page_header("Secure access", "Login to Career Brownie", "Use the account created through the backend JWT authentication system."),
                rx.form(
                    rx.vstack(
                        text_input("email", "Email", "email"),
                        text_input("password", "Password", "password"),
                        primary_button("Login"),
                        rx.cond(AuthState.error != "", rx.text(AuthState.error, color=DANGER)),
                        rx.cond(AuthState.success != "", rx.text(AuthState.success, color=SUCCESS)),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=AuthState.login,
                    width="100%",
                ),
                rx.link("Need an account? Register", href="/register", color="#27e0ff"),
                width="100%",
                max_width="460px",
                padding="24px",
                **panel_style(),
            ),
            width="100%",
        )
    )
