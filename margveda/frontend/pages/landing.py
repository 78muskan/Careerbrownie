import reflex as rx

from components.cards import feature_card, metric_card
from components.layout import page_header, page_shell
from components.theme import ACCENT, MUTED, panel_style


def landing_page() -> rx.Component:
    return page_shell(
        rx.grid(
            rx.vstack(
                page_header(
                    "AI-powered career counselling",
                    "Career Brownie guides students from confusion to a clear career path.",
                    "Students get recommendations, counsellors manage sessions, admins track the platform, and the AI service powers guidance workflows.",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Start as Student", size="3", background=ACCENT, color="#020617"),
                        href="/register",
                    ),
                    rx.link(
                        rx.button("Open Login", size="3", variant="outline", color=ACCENT),
                        href="/login",
                    ),
                    spacing="4",
                    wrap="wrap",
                ),
                align_items="start",
                spacing="5",
            ),
            rx.vstack(
                rx.text("Platform Flow", color=ACCENT, font_weight="900"),
                rx.text("Reflex frontend → FastAPI backend → Python AI service", color=MUTED),
                rx.divider(border_color="rgba(148, 163, 184, 0.22)"),
                rx.text("JWT auth, role-based dashboards, recommendations, chatbot, roadmaps, and session booking are wired for one product flow.", line_height="1.7"),
                align_items="start",
                padding="24px",
                **panel_style(),
            ),
            columns="2",
            spacing="6",
            width="100%",
        ),
        rx.grid(
            metric_card("Users", "3 Roles", "Students, counsellors, admins"),
            metric_card("AI APIs", "5 Flows", "Chatbot, careers, skill gap, colleges, roadmaps"),
            metric_card("Stack", "Python", "FastAPI, Reflex, SQLAlchemy"),
            columns="3",
            spacing="4",
            width="100%",
            margin_top="28px",
        ),
        rx.grid(
            feature_card("Student Dashboard", "Manage profile and get career direction.", "/student"),
            feature_card("AI Chatbot", "Ask career guidance questions in natural language.", "/chatbot"),
            feature_card("Roadmaps", "Generate practical step-by-step career plans.", "/roadmap"),
            feature_card("Recommendations", "Explore careers, colleges, and skill gaps.", "/recommendations"),
            columns="4",
            spacing="4",
            width="100%",
            margin_top="18px",
        ),
    )
