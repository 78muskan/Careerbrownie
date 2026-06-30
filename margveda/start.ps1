# ── MargVedA Local Development Starter (Windows PowerShell) ──────────────────
# Run this from the margveda\ directory:
#   cd path\to\margveda
#   .\start.ps1
#
# Prerequisites:
#   - Python 3.12+  (python --version)
#   - Node.js 22+   (node --version)
#   - pip install virtualenv
# ─────────────────────────────────────────────────────────────────────────────

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

function Write-Step($msg) { Write-Host "`n>> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "   $msg" -ForegroundColor Green }

# ── 1. Ensure virtualenv ─────────────────────────────────────────────────────
Write-Step "Checking Python virtual environment..."
if (-not (Test-Path "$root\venv")) {
    Write-Host "   Creating venv..." -ForegroundColor Yellow
    python -m venv "$root\venv"
}
$pip  = "$root\venv\Scripts\pip.exe"
$py   = "$root\venv\Scripts\python.exe"
Write-OK "venv ready"

# ── 2. Install Python deps ───────────────────────────────────────────────────
Write-Step "Installing Python dependencies..."
& $pip install -q -r "$root\backend_django\requirements.txt"
& $pip install -q -r "$root\ai_service\requirements.txt"
Write-OK "Python deps installed"

# ── 3. Copy .env files if missing ────────────────────────────────────────────
Write-Step "Checking .env files..."
if (-not (Test-Path "$root\backend_django\.env")) {
    Copy-Item "$root\backend_django\.env.example" "$root\backend_django\.env"
    Write-Host "   Created backend_django\.env from example" -ForegroundColor Yellow
}
if (-not (Test-Path "$root\ai_service\.env")) {
    Copy-Item "$root\ai_service\.env.example" "$root\ai_service\.env"
    Write-Host "   Created ai_service\.env from example" -ForegroundColor Yellow
}
if (-not (Test-Path "$root\frontend-next\.env.local")) {
    Copy-Item "$root\frontend-next\.env.local.example" "$root\frontend-next\.env.local"
    Write-Host "   Created frontend-next\.env.local from example" -ForegroundColor Yellow
}
Write-OK ".env files ready"

# ── 4. Django migrations ─────────────────────────────────────────────────────
Write-Step "Running Django migrations..."
Push-Location "$root\backend_django"
& $py manage.py migrate --run-syncdb
Pop-Location
Write-OK "Migrations done"

# ── 5. Install Node deps ──────────────────────────────────────────────────────
Write-Step "Installing Node.js dependencies for frontend-next..."
Push-Location "$root\frontend-next"
npm install --silent
Pop-Location
Write-OK "npm install done"

# ── 6. Launch services in separate windows ────────────────────────────────────
Write-Step "Launching all services..."

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
  Set-Location '$root\backend_django'
  Write-Host 'Django Backend (port 8001)' -ForegroundColor Cyan
  & '$py' manage.py runserver 0.0.0.0:8001
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
  Set-Location '$root\ai_service'
  Write-Host 'AI Service (port 9000)' -ForegroundColor Cyan
  & '$py' -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
  Set-Location '$root\frontend-next'
  Write-Host 'Next.js Frontend (port 3000)' -ForegroundColor Cyan
  npm run dev
"@

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "  Career Brownie is starting up in 3 new windows." -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend   → http://localhost:3000" -ForegroundColor White
Write-Host "  Django API → http://localhost:8001/api/v1/" -ForegroundColor White
Write-Host "  API Docs   → http://localhost:8001/api/schema/swagger-ui/" -ForegroundColor White
Write-Host "  AI Service → http://localhost:9000/docs" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
