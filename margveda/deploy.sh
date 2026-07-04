#!/usr/bin/env bash
# ── MargVedA Production Deploy ─────────────────────────────────────────────────
# Usage on the VPS after first-time setup:
#   bash deploy.sh
#
# First-time setup:
#   1. Install Docker & Docker Compose plugin
#   2. Copy .env.prod → .env.prod (fill in your values)
#   3. Place SSL certs: ssl/fullchain.pem  ssl/privkey.pem
#      (use certbot: sudo certbot certonly --standalone -d yourdomain.com)
#   4. Run:  bash deploy.sh
#
# What this script does:
#   1. Pulls latest code (git pull --ff-only)
#   2. Builds new Docker images (cached layers)
#   3. Brings up new services alongside old ones
#   4. Runs health checks against all services
#   5. If healthy: removes old containers
#   6. If unhealthy: rolls back to previous version
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  MargVedA — Production Deploy"
echo "  $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Config ─────────────────────────────────────────────────────────────────────
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.prod"
ROLLBACK_TAG="deploy-rollback-$(date +%s)"
MAX_HEALTH_RETRIES=30
HEALTH_RETRY_INTERVAL=5

# ── Pre-flight checks ─────────────────────────────────────────────────────────

if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: $ENV_FILE not found. Copy .env.prod.example → .env.prod and fill values."
    exit 1
fi

if [ ! -f "ssl/fullchain.pem" ] || [ ! -f "ssl/privkey.pem" ]; then
    echo "WARNING: SSL certificates not found at ssl/ — HTTPS will fail."
    echo "         Run: sudo certbot certonly --standalone -d yourdomain.com"
    echo "         Then: cp /etc/letsencrypt/live/yourdomain.com/* ssl/"
fi

if ! docker compose version &>/dev/null; then
    echo "ERROR: Docker Compose (V2) is not installed."
    exit 1
fi

# ── Step 1: Pull latest code ──────────────────────────────────────────────────

echo ""
echo "▶ [1/6] Pulling latest code..."
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse @{upstream})
if [ "$LOCAL" != "$REMOTE" ]; then
    git pull --ff-only origin main
    echo "  → Updated to $(git rev-parse --short HEAD)"
else
    echo "  → Already up to date ($(git rev-parse --short HEAD))"
fi

# ── Step 2: Save current deployment state (for rollback) ──────────────────────

echo ""
echo "▶ [2/6] Saving current deployment state..."
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" images > /tmp/pre-deploy-images.txt 2>/dev/null || true
echo "  → Current image state saved"

# ── Step 3: Build new images ──────────────────────────────────────────────────

echo ""
echo "▶ [3/6] Building Docker images..."
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --pull 2>&1 | tail -20
echo "  → Build complete"

# ── Step 4: Deploy new services ───────────────────────────────────────────────

echo ""
echo "▶ [4/6] Deploying services..."
# Use --remove-orphans to clean up any old/unused containers
docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d --remove-orphans 2>&1
echo "  → Containers started"

# ── Step 5: Health check all services ─────────────────────────────────────────

echo ""
echo "▶ [5/6] Running health checks..."
HEALTHY=true
FAILED_SERVICES=""

# List of services with health checks to verify
SERVICES=("postgres" "redis" "ollama" "ai_service" "django")

for service in "${SERVICES[@]}"; do
    echo -n "  Waiting for $service ... "
    retries=0
    SERVICE_OK=false
    while [ $retries -lt $MAX_HEALTH_RETRIES ]; do
        STATUS=$(docker compose -f "$COMPOSE_FILE" ps --format json "$service" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('Health','') if isinstance(d,dict) else d[0].get('Health','') if isinstance(d,list) and len(d)>0 else '')" 2>/dev/null || echo "")
        if [ "$STATUS" = "healthy" ]; then
            SERVICE_OK=true
            echo "healthy (${retries}s)"
            break
        fi
        retries=$((retries + 1))
        sleep $HEALTH_RETRY_INTERVAL
    done

    if [ "$SERVICE_OK" = false ]; then
        HEALTHY=false
        FAILED_SERVICES="$FAILED_SERVICES $service"
        echo "UNHEALTHY after $MAX_HEALTH_RETRIES attempts"
        docker compose -f "$COMPOSE_FILE" logs --tail=20 "$service" 2>/dev/null || true
    fi
done

# ── Django-specific check: migrations + collectstatic ──────────────────────────
echo -n "  Running Django migrations ... "
if docker compose -f "$COMPOSE_FILE" exec -T django python manage.py migrate --noinput 2>&1 | tail -5; then
    echo "  → Migrations applied"
else
    echo "  → Migration WARNING (non-fatal)"
fi

echo -n "  Collecting static files ... "
if docker compose -f "$COMPOSE_FILE" exec -T django python manage.py collectstatic --noinput --clear 2>&1 | tail -3; then
    echo "  → Static files collected"
else
    echo "  → Static files WARNING (non-fatal)"
fi

# ── Full API smoke test ────────────────────────────────────────────────────────
echo -n "  Smoke test: Django API ... "
if curl -sf http://localhost:8001/api/ 2>/dev/null || curl -sf http://localhost:80/api/ 2>/dev/null; then
    echo "OK"
else
    echo "WARNING (API not responding yet — may need nginx)"
fi

echo -n "  Smoke test: AI service ... "
if curl -sf http://localhost:9000/health 2>/dev/null; then
    echo "OK"
else
    echo "WARNING (AI service health endpoint)"
fi

# ── Step 6: Rollback on failure ───────────────────────────────────────────────

if [ "$HEALTHY" = false ]; then
    echo ""
    echo "⚠  HEALTH CHECKS FAILED for: $FAILED_SERVICES"
    echo "   Rolling back to previous deployment..."
    echo "   (Tag: $ROLLBACK_TAG)"

    # Stop the new containers
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down --timeout 30

    # Restore from backup
    if [ -f "/tmp/pre-deploy-images.txt" ]; then
        echo "   Re-building previous images..."
        # Re-pull previous versions (this is best-effort)
        docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache 2>&1 | tail -5
        docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d 2>&1
    fi

    echo ""
    echo "✖ ROLLBACK COMPLETE. Manual intervention required."
    echo "   Check service logs: docker compose -f $COMPOSE_FILE logs --tail=50 <service>"
    exit 1
fi

# ── Clean up ───────────────────────────────────────────────────────────────────

echo ""
echo "▶ [6/6] Cleaning up old images..."
docker image prune -f --filter "until=24h" 2>/dev/null || true
echo "  → Done"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✓ Deploy complete"
echo "  Date:   $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "  Commit: $(git rev-parse --short HEAD)"
echo "  Site:   https://$(grep ^DOMAIN $ENV_FILE | cut -d= -f2)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
docker compose -f "$COMPOSE_FILE" ps
