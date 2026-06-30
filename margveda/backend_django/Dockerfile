FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (from repo root context)
COPY margveda/backend_django/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the Django app
COPY margveda/backend_django/ .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn careerbrownie_backend.wsgi:application \
      --bind 0.0.0.0:${PORT:-8080} \
      --workers 3 \
      --timeout 120
