param([string]$msg = "")

if (-not $msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $msg = "update: $timestamp"
}

Write-Host ""
Write-Host "Deploying CareerBrownie..." -ForegroundColor Cyan
Write-Host ""

git add .

$status = git status --porcelain
if (-not $status) {
    Write-Host "Nothing to deploy — no changes detected." -ForegroundColor Yellow
    exit 0
}

git commit -m $msg
git push origin master

Write-Host ""
Write-Host "Pushed! Auto-deployments started:" -ForegroundColor Green
Write-Host "  Railway  (backend API) -> builds in ~3 min" -ForegroundColor White
Write-Host "  Vercel   (frontend)    -> builds in ~2 min" -ForegroundColor White
Write-Host ""
Write-Host "Monitor:" -ForegroundColor DarkGray
Write-Host "  Railway : https://railway.com/project/b3dbbdfb-5546-4686-bd03-cecd0aec560e" -ForegroundColor DarkGray
Write-Host "  Vercel  : https://vercel.com/dashboard" -ForegroundColor DarkGray
Write-Host ""
