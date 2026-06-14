import reflex as rx

from components.theme import ACCENT, MUTED, TEXT, panel_style


def metric_card(label: str, value, detail) -> rx.Component:
    return rx.vstack(
        rx.text(label, color=MUTED, font_size="12px", font_weight="800"),
        rx.heading(value, size="6", color=TEXT),
        rx.text(detail, color=MUTED, font_size="13px"),
        align_items="start",
        spacing="2",
        padding="18px",
        min_height="130px",
        **panel_style(),
    )


def feature_card(title: str, body: str, route: str) -> rx.Component:
    return rx.link(
        rx.vstack(
            rx.text("●", color=ACCENT),
            rx.heading(title, size="5"),
            rx.text(body, color=MUTED, line_height="1.6"),
            align_items="start",
            spacing="3",
            padding="20px",
            min_height="190px",
            **panel_style(),
        ),
        href=route,
        text_decoration="none",
        color=TEXT,
    )
