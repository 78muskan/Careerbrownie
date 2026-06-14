import reflex as rx

from components.cards import metric_card
from components.layout import page_header, page_shell
from components.theme import MUTED, panel_style
from states.admin_state import AdminState


def admin_dashboard_page() -> rx.Component:
    return page_shell(
        page_header("Admin command center", "Platform analytics", "Track users, counsellors, sessions, and roadmap generation."),
        rx.button("Refresh Admin Data", on_click=AdminState.load_dashboard, margin_bottom="18px"),
        rx.grid(
            metric_card("Users", AdminState.total_users, "Registered accounts"),
            metric_card("Students", AdminState.students, "Student profiles"),
            metric_card("Counsellors", AdminState.counsellors, "Counsellor profiles"),
            metric_card("Sessions", AdminState.sessions, "Guidance sessions"),
            columns="4",
            spacing="4",
            width="100%",
        ),
        rx.vstack(
            rx.heading("Users", size="5"),
            rx.foreach(
                AdminState.users,
                lambda user: rx.hstack(
                    rx.text(user["full_name"], color="#e5f4ff"),
                    rx.text(user["email"], color=MUTED),
                    rx.text(user["role"], color="#27e0ff"),
                    width="100%",
                    justify_content="space-between",
                    padding="12px",
                    border_bottom="1px solid rgba(148, 163, 184, 0.18)",
                ),
            ),
            rx.text(AdminState.message, color=MUTED),
            align_items="start",
            padding="20px",
            margin_top="18px",
            **panel_style(),
        ),
    )
