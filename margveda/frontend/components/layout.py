import reflex as rx

from components.navigation import navbar
from components.theme import ACCENT, BG, TEXT


def page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            *children,
            width="100%",
            max_width="1180px",
            margin="0 auto",
            padding="34px 20px 56px",
        ),
        min_height="100vh",
        background=(
            f"radial-gradient(circle at 18% 12%, rgba(39,224,255,0.18), transparent 28%),"
            f"radial-gradient(circle at 82% 4%, rgba(139,92,246,0.18), transparent 24%), {BG}"
        ),
        color=TEXT,
    )


def page_header(kicker: str, title: str, subtitle: str) -> rx.Component:
    return rx.vstack(
        rx.text(kicker, color=ACCENT, font_weight="900", font_size="13px"),
        rx.heading(title, size="8", line_height="1.05", max_width="760px"),
        rx.text(subtitle, color="#94a3b8", max_width="760px", line_height="1.7"),
        spacing="3",
        align_items="start",
        margin_bottom="24px",
    )
