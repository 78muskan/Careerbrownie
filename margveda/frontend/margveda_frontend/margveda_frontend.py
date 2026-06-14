import reflex as rx

from components.theme import GLOBAL_STYLE
from pages.admin_dashboard import admin_dashboard_page
from pages.chatbot import chatbot_page
from pages.counsellor_dashboard import counsellor_dashboard_page
from pages.landing import landing_page
from pages.login import login_page
from pages.recommendations import recommendations_page
from pages.register import register_page
from pages.roadmap import roadmap_page
from pages.student_dashboard import student_dashboard_page
from states.admin_state import AdminState
from states.auth_state import AuthState
from states.counsellor_state import CounsellorState
from states.recommendation_state import RecommendationState
from states.student_state import StudentState


app = rx.App(style=GLOBAL_STYLE)

app.add_page(landing_page, route="/", title="MargVedA")
app.add_page(login_page, route="/login", title="Login | MargVedA", on_load=AuthState.load_me)
app.add_page(register_page, route="/register", title="Register | MargVedA")
app.add_page(
    student_dashboard_page,
    route="/student",
    title="Student Dashboard | MargVedA",
    on_load=StudentState.load_dashboard,
)
app.add_page(
    counsellor_dashboard_page,
    route="/counsellor",
    title="Counsellor Dashboard | MargVedA",
    on_load=CounsellorState.load_dashboard,
)
app.add_page(
    admin_dashboard_page,
    route="/admin",
    title="Admin Dashboard | MargVedA",
    on_load=AdminState.load_dashboard,
)
app.add_page(chatbot_page, route="/chatbot", title="AI Chatbot | MargVedA")
app.add_page(
    roadmap_page,
    route="/roadmap",
    title="Career Roadmap | MargVedA",
    on_load=RecommendationState.load_roadmaps,
)
app.add_page(recommendations_page, route="/recommendations", title="Recommendations | MargVedA")
