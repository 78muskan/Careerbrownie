import reflex as rx

from components.forms import primary_button, text_input
from components.layout import page_header, page_shell
from components.theme import DANGER, SUCCESS, input_style, panel_style
from states.auth_state import AuthState


def register_page() -> rx.Component:
    return page_shell(
        rx.center(
            rx.vstack(
                page_header("Create account", "Join MargVedA", "Choose your role so the platform opens the correct dashboard."),
                rx.form(
                    rx.vstack(
                        text_input("full_name", "Full name"),
                        text_input("email", "Email", "email"),
                        text_input("password", "Password", "password"),
                        rx.select(
                            ["student", "counsellor", "admin"],
                            name="role",
                            default_value="student",
                            style=input_style(),
                        ),
                        primary_button("Create account"),
                        rx.cond(AuthState.error != "", rx.text(AuthState.error, color=DANGER)),
                        rx.cond(AuthState.success != "", rx.text(AuthState.success, color=SUCCESS)),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=AuthState.register,
                    width="100%",
                ),
                rx.link("Already registered? Login", href="/login", color="#27e0ff"),
                width="100%",
                max_width="500px",
                padding="24px",
                **panel_style(),
            ),
            width="100%",
        )
    )
