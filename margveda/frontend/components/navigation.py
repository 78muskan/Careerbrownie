import reflex as rx

from components.theme import ACCENT, BORDER, MUTED, TEXT


def nav_link(label: str, route: str) -> rx.Component:
    return rx.link(
        label,
        href=route,
        color=MUTED,
        font_weight="700",
        _hover={"color": ACCENT},
    )


def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.hstack(
                rx.box(
                    width="34px",
                    height="34px",
                    border_radius="8px",
                    background=f"linear-gradient(135deg, {ACCENT}, #8b5cf6)",
                ),
                rx.vstack(
                    rx.text("MargVedA", color=TEXT, font_weight="900", line_height="1"),
                    rx.text("AI Career Guidance", color=MUTED, font_size="12px"),
                    spacing="0",
                    align_items="start",
                ),
                spacing="3",
            ),
            href="/",
            text_decoration="none",
        ),
        rx.spacer(),
        rx.hstack(
            nav_link("Login", "/login"),
            nav_link("Register", "/register"),
            nav_link("Student", "/student"),
            nav_link("Counsellor", "/counsellor"),
            nav_link("Admin", "/admin"),
            nav_link("Chatbot", "/chatbot"),
            nav_link("Roadmap", "/roadmap"),
            nav_link("Recommendations", "/recommendations"),
            spacing="5",
            wrap="wrap",
        ),
        width="100%",
        padding="18px 24px",
        border_bottom=f"1px solid {BORDER}",
        position="sticky",
        top="0",
        z_index="10",
        backdrop_filter="blur(16px)",
        background="rgba(7, 11, 24, 0.86)",
    )
