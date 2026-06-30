from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Career Brownie AI Service v%s starting (env=%s)", settings.VERSION, settings.ENVIRONMENT)
    log.info("LLM: %s @ %s", settings.OLLAMA_MODEL, settings.OLLAMA_URL)
    log.info("Vector DB: %s", settings.QDRANT_URL)
    log.info("Embeddings: %s (%s)", settings.EMBED_MODEL, settings.EMBED_DEVICE)
    yield
    log.info("Career Brownie AI Service shutting down")


app = FastAPI(
    title="Career Brownie AI Service",
    version=settings.VERSION,
    description="Enterprise AI platform: RAG + Agents (Qwen2.5 / bge-m3 / Qdrant)",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.is_production else ["https://careerbrownie.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ──────────────────────────────────────────────────────────────────

@app.get("/health", tags=["health"])
async def health():
    from app.llm.ollama import OllamaLLM
    ollama_ok = await OllamaLLM().is_available()
    return {
        "status": "ok",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "llm": settings.OLLAMA_MODEL,
        "ollama_available": ollama_ok,
        "fallback_available": bool(settings.ANTHROPIC_API_KEY),
    }


# ── New API routes (v2) ──────────────────────────────────────────────────────

from app.api.chat import router as chat_router
from app.api.ingest import router as ingest_router

app.include_router(chat_router, prefix="/api/v2")
app.include_router(ingest_router, prefix="/api/v2")


# ── Legacy routes (v1 — backward compat) ────────────────────────────────────

from app.chatbot.bot import chat as legacy_chat
from app.models.schemas import (
    CareerRecommendationRequest, CareerRecommendationResponse,
    ChatMessageRequest, ChatMessageResponse,
    CollegePredictionRequest, CollegePredictionResponse,
    RoadmapRequest, RoadmapResponse,
    SkillGapRequest, SkillGapResponse,
)
from app.pipelines.college_prediction import predict_colleges
from app.pipelines.skill_gap import analyze_skill_gap
from app.recommender.engine import recommend_careers
from app.roadmap.generator import generate_roadmap


@app.post("/chatbot/chat", response_model=ChatMessageResponse, tags=["legacy"])
def chatbot_chat(payload: ChatMessageRequest):
    return legacy_chat(payload)


@app.post("/recommendations/careers", response_model=CareerRecommendationResponse, tags=["legacy"])
def career_recommendations(payload: CareerRecommendationRequest):
    return recommend_careers(payload)


@app.post("/recommendations/skill-gap", response_model=SkillGapResponse, tags=["legacy"])
def skill_gap(payload: SkillGapRequest):
    return analyze_skill_gap(payload)


@app.post("/recommendations/colleges", response_model=CollegePredictionResponse, tags=["legacy"])
def colleges(payload: CollegePredictionRequest):
    return predict_colleges(payload)


@app.post("/roadmaps/generate", response_model=RoadmapResponse, tags=["legacy"])
def roadmaps(payload: RoadmapRequest):
    return generate_roadmap(payload)
