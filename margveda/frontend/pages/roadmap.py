import reflex as rx

from components.forms import primary_button, text_input
from components.layout import page_header, page_shell
from components.roadmap import roadmap_stage_card
from components.theme import MUTED, panel_style
from states.recommendation_state import RecommendationState


def roadmap_page() -> rx.Component:
    return page_shell(
        page_header("Career roadmap", "Generate a step-by-step plan", "The backend saves the roadmap and uses the AI service to generate the plan."),
        rx.grid(
            rx.vstack(
                rx.heading("Create Roadmap", size="5"),
                rx.form(
                    rx.vstack(
                        text_input("career_goal", "Target career"),
                        text_input("current_level", "Current level"),
                        text_input("timeline_months", "Timeline months", "number"),
                        primary_button("Generate Roadmap"),
                        rx.text(RecommendationState.message, color=MUTED),
                        spacing="3",
                    ),
                    on_submit=RecommendationState.generate_roadmap,
                    width="100%",
                ),
                align_items="start",
                padding="20px",
                **panel_style(),
            ),
            rx.vstack(
                rx.heading(RecommendationState.roadmap_title, size="5"),
                rx.foreach(
                    RecommendationState.roadmap_stages,
                    roadmap_stage_card,
                ),
                align_items="start",
                spacing="3",
                padding="20px",
                **panel_style(),
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
    )
