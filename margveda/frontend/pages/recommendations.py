import reflex as rx

from components.forms import primary_button, text_input
from components.layout import page_header, page_shell
from components.theme import ACCENT, MUTED, panel_style
from states.recommendation_state import RecommendationState


def recommendations_page() -> rx.Component:
    return page_shell(
        page_header("Recommendations", "Career, skill gap, and college prediction", "Use the backend API that delegates intelligence to the Python AI service."),
        rx.grid(
            rx.vstack(
                rx.heading("Career Recommendation", size="5"),
                rx.form(
                    rx.vstack(
                        text_input("interests", "Interests, comma separated"),
                        text_input("skills", "Skills, comma separated"),
                        text_input("academic_stream", "Academic stream"),
                        text_input("preferred_location", "Preferred location"),
                        primary_button("Recommend Careers"),
                        spacing="3",
                    ),
                    on_submit=RecommendationState.recommend,
                    width="100%",
                ),
                rx.foreach(
                    RecommendationState.recommendations,
                    lambda item: rx.vstack(
                        rx.text(item["title"], color=ACCENT, font_weight="900"),
                        rx.text(item["reason"], color=MUTED),
                        align_items="start",
                        padding="12px",
                        **panel_style(),
                    ),
                ),
                align_items="start",
                spacing="3",
                padding="20px",
                **panel_style(),
            ),
            rx.vstack(
                rx.heading("Skill Gap", size="5"),
                rx.form(
                    rx.vstack(
                        text_input("target_career", "Target career"),
                        text_input("current_skills", "Current skills, comma separated"),
                        primary_button("Analyze Skill Gap"),
                        spacing="3",
                    ),
                    on_submit=RecommendationState.analyze_skill_gap,
                    width="100%",
                ),
                rx.text(RecommendationState.skill_target, color=ACCENT),
                rx.foreach(
                    RecommendationState.missing_skills,
                    lambda item: rx.text("• ", item, color=MUTED),
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
        rx.vstack(
            rx.heading("College Prediction", size="5"),
            rx.form(
                rx.grid(
                    text_input("academic_stream", "Academic stream"),
                    text_input("score_percent", "Score percent", "number"),
                    text_input("preferred_location", "Preferred location"),
                    text_input("budget", "Budget"),
                    primary_button("Predict Colleges"),
                    columns="5",
                    spacing="3",
                    width="100%",
                ),
                on_submit=RecommendationState.predict_colleges,
                width="100%",
            ),
            rx.foreach(
                RecommendationState.colleges,
                lambda item: rx.vstack(
                    rx.text(item["name"], color=ACCENT, font_weight="900"),
                    rx.text(item["location"], color=MUTED),
                    rx.text(item["reason"], color=MUTED),
                    align_items="start",
                    padding="12px",
                    **panel_style(),
                ),
            ),
            align_items="start",
            spacing="3",
            padding="20px",
            margin_top="18px",
            **panel_style(),
        ),
    )
