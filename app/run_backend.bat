@echo off
title BreastDiagAI - Demarrage Backend FastAPI
echo ========================================================
echo    BreastDiagAI - Demarrage du Backend FastAPI
echo    Campagne Octobre Rose 2026
echo ========================================================
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
