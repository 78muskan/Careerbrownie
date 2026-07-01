FROM python:3.12-slim

WORKDIR /app

# psycopg2-binary includes its own libpq — no system packages needed
COPY margveda/backend_django/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY margveda/backend_django/ .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn careerbrownie_backend.wsgi:application \
      --bind 0.0.0.0:${PORT:-8080} \
      --workers 2 \
      --timeout 120 \
      --log-level info
