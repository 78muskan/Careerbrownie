import reflex as rx

from components.theme import button_style, input_style


def text_input(name: str, placeholder: str, input_type: str = "text") -> rx.Component:
    return rx.input(
        name=name,
        placeholder=placeholder,
        type=input_type,
        style=input_style(),
    )


def text_area(name: str, placeholder: str) -> rx.Component:
    return rx.text_area(
        name=name,
        placeholder=placeholder,
        background="#0f172a",
        border="1px solid rgba(148, 163, 184, 0.22)",
        border_radius="8px",
        color="#e5f4ff",
        min_height="110px",
        width="100%",
    )


def primary_button(label: str) -> rx.Component:
    return rx.button(label, type="submit", style=button_style())
