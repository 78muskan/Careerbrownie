FROM python:3.12-slim

WORKDIR /app

# Pip tuning — avoid timeouts and source builds on Railway's network
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=5 \
    PORT=8080

# Install deps first (cached layer — only re-runs if requirements.txt changes)
# Note: build context is ./backend_django, so files are at ./requirements.txt
COPY requirements.txt .
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

EXPOSE 8080

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn careerbrownie_backend.wsgi:application \
      --bind 0.0.0.0:${PORT:-8080} \
      --workers 2 \
      --timeout 120 \
      --log-level info
