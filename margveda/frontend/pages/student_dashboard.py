import reflex as rx

from components.cards import metric_card
from components.forms import primary_button, text_area, text_input
from components.layout import page_header, page_shell
from components.theme import MUTED, panel_style
from states.auth_state import AuthState
from states.student_state import StudentState


def student_dashboard_page() -> rx.Component:
    return page_shell(
        page_header("Student workspace", "Your AI guidance dashboard", "Complete your profile, track roadmap progress, and prepare for counselling."),
        rx.hstack(
            rx.text("Signed in as: "),
            rx.text(AuthState.email, color="#27e0ff", font_weight="900"),
            rx.spacer(),
            rx.button("Logout", on_click=AuthState.logout, variant="outline"),
            width="100%",
            margin_bottom="18px",
        ),
        rx.grid(
            metric_card("Roadmaps", StudentState.roadmap_count, "Saved career plans"),
            metric_card("Sessions", StudentState.upcoming_sessions, "Requested or confirmed"),
            metric_card("Next Step", "Action", StudentState.next_step),
            columns="3",
            spacing="4",
            width="100%",
        ),
        rx.grid(
            rx.vstack(
                rx.heading("Student Profile", size="5"),
                rx.form(
                    rx.vstack(
                        text_input("grade", "Class / grade"),
                        text_input("stream", "Academic stream"),
                        text_area("interests", "Interests separated by commas"),
                        text_area("skills", "Skills separated by commas"),
                        text_input("career_goal", "Career goal"),
                        text_input("preferred_location", "Preferred location"),
                        text_input("budget", "Budget"),
                        primary_button("Save profile"),
                        rx.text(StudentState.message, color=MUTED),
                        spacing="3",
                    ),
                    on_submit=StudentState.update_profile,
                    width="100%",
                ),
                align_items="start",
                padding="20px",
                **panel_style(),
            ),
            rx.vstack(
                rx.heading("Recommended Workflow", size="5"),
                rx.text("1. Complete your profile.", color=MUTED),
                rx.text("2. Generate career recommendations.", color=MUTED),
                rx.text("3. Create a roadmap.", color=MUTED),
                rx.text("4. Book a counsellor session.", color=MUTED),
                rx.link(rx.button("Open Recommendations", width="100%"), href="/recommendations"),
                rx.link(rx.button("Open Roadmap", width="100%"), href="/roadmap"),
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
