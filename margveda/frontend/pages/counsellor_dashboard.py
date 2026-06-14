import reflex as rx

from components.cards import metric_card
from components.forms import primary_button, text_area, text_input
from components.layout import page_header, page_shell
from components.theme import MUTED, panel_style
from states.counsellor_state import CounsellorState


def counsellor_dashboard_page() -> rx.Component:
    return page_shell(
        page_header("Counsellor dashboard", "Manage guidance sessions", "Maintain your profile and monitor student requests."),
        rx.grid(
            metric_card("Total Sessions", CounsellorState.total_sessions, "All assigned sessions"),
            metric_card("Requests", CounsellorState.requested_sessions, "Waiting for action"),
            metric_card("Availability", "Profile", CounsellorState.availability),
            columns="3",
            spacing="4",
            width="100%",
        ),
        rx.grid(
            rx.vstack(
                rx.heading("Counsellor Profile", size="5"),
                rx.form(
                    rx.vstack(
                        text_input("specialization", "Specialization"),
                        text_input("years_experience", "Years experience", "number"),
                        text_input("availability", "Availability"),
                        text_area("bio", "Short bio"),
                        primary_button("Save profile"),
                        rx.text(CounsellorState.message, color=MUTED),
                        spacing="3",
                    ),
                    on_submit=CounsellorState.update_profile,
                    width="100%",
                ),
                align_items="start",
                padding="20px",
                **panel_style(),
            ),
            rx.vstack(
                rx.heading("Upcoming Sessions", size="5"),
                rx.foreach(
                    CounsellorState.sessions,
                    lambda item: rx.text(item["topic"], color=MUTED),
                ),
                align_items="start",
                padding="20px",
                **panel_style(),
            ),
            columns="2",
            spacing="4",
            width="100%",
            margin_top="18px",
        ),
    )
