FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000
EXPOSE 3001

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--frontend-port", "3000", "--backend-port", "3001"]
