@echo off
echo Starting Diabetes Risk Verification API...
echo Ensure artifacts are placed in ../models/ml and ../artifacts/ml

cd /d "%~dp0"
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause
