Write-Host "========================================"
Write-Host "Edu Content Platform - Windows Setup"
Write-Host "========================================"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python was not found. Install Python 3.12 and try again."
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_project.py --seed-demo

if (Get-Command npm -ErrorAction SilentlyContinue) {
    npm run frontend:install
} else {
    Write-Warning "npm was not found. Skipping frontend install. Install Node.js later and run npm run frontend:install."
}

Write-Host ""
Write-Host "Setup completed."
Write-Host "Start backend:  .venv\Scripts\activate && uvicorn app.main:app --reload"
Write-Host "Start frontend: npm run frontend:dev"
