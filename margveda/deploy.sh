#!/usr/bin/env bash
# ── MargVedA one-line Hostinger VPS deploy ───────────────────────────────────
# Usage (on the server after first-time setup):
#   bash deploy.sh
#
# First-time setup:
#   1. Install Docker: https://docs.docker.com/engine/install/ubuntu/
#   2. Copy .env.prod.example → .env.prod and fill in your values
#   3. Place SSL certs: ssl/fullchain.pem  ssl/privkey.pem
#      (use certbot: sudo certbot certonly --standalone -d yourdomain.com)
#   4. Run:  bash deploy.sh
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MargVedA — Production Deploy"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Load prod env
if [ ! -f .env.prod ]; then
  echo "ERROR: .env.prod not found. Copy .env.prod.example → .env.prod and fill values."
  exit 1
fi
export $(grep -v '^#' .env.prod | xargs)

# Pull latest code
echo "▶ Pulling latest code..."
git pull --ff-only

# Build & restart all services
echo "▶ Building images..."
docker compose -f docker-compose.prod.yml --env-file .env.prod build --no-cache

echo "▶ Starting services..."
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --remove-orphans

# Run migrations inside django container
echo "▶ Running database migrations..."
docker compose -f docker-compose.prod.yml exec django python manage.py migrate --noinput

# Collect static files
echo "▶ Collecting static files..."
docker compose -f docker-compose.prod.yml exec django python manage.py collectstatic --noinput --clear

echo ""
echo "✓ Deploy complete."
echo "  Site:      https://${DOMAIN}"
echo "  API docs:  https://${DOMAIN}/api/v1/schema/"
echo "  Admin:     https://${DOMAIN}/admin/"
echo ""
docker compose -f docker-compose.prod.yml ps
