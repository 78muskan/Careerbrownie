FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_RETRIES=5

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# ── Stage 1: PyTorch CPU (large file from PyTorch CDN) ──────────────────────
RUN pip install --no-cache-dir --timeout 180 --retries 5 \
    --index-url https://download.pytorch.org/whl/cpu \
    "torch>=2.4,<3"

# ── Stage 2: Web framework + HTTP ───────────────────────────────────────────
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    python-multipart==0.0.12 \
    pydantic==2.9.2 \
    httpx==0.27.2

# ── Stage 3: LLM clients ────────────────────────────────────────────────────
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    ollama==0.3.3 \
    "anthropic>=0.40.0"

# ── Stage 4: HuggingFace / NLP stack ────────────────────────────────────────
RUN pip install --no-cache-dir --timeout 180 --retries 5 \
    transformers==4.44.2

RUN pip install --no-cache-dir --timeout 180 --retries 5 \
    sentence-transformers==3.2.1

RUN pip install --no-cache-dir --timeout 180 --retries 5 \
    FlagEmbedding==1.3.4

# ── Stage 5: Vector store + cache + utilities ────────────────────────────────
RUN pip install --no-cache-dir --timeout 120 --retries 5 \
    qdrant-client==1.11.3 \
    "redis[hiredis]==5.2.1" \
    numpy==1.26.4

COPY app ./app

# Pre-bake models into image (|| true = skip if no internet during build)
RUN python -c "from FlagEmbedding import BGEM3FlagModel; BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)" || true
RUN python -c "from FlagEmbedding import FlagReranker; FlagReranker('BAAI/bge-reranker-v2-m3')" || true

EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
    CMD curl -f http://localhost:9000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
