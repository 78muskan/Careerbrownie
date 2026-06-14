import reflex as rx

from components.theme import ACCENT, MUTED, panel_style


def roadmap_stage_card(stage: dict) -> rx.Component:
    return rx.vstack(
        rx.text(stage["title"], color=ACCENT, font_weight="900"),
        rx.text(stage["description"], color="#e5f4ff", line_height="1.6"),
        rx.text(stage["duration"], color=MUTED),
        align_items="start",
        spacing="2",
        padding="18px",
        **panel_style(),
    )
