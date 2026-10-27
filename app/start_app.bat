@echo off
title BreastDiagAI - Lancement Global
echo ========================================================
echo          BreastDiagAI - Octobre Rose 🎗️
echo    Lancement conjoint Backend FastAPI + Frontend React
echo ========================================================
echo.
echo 1. Lancement du Backend FastAPI sur http://127.0.0.1:8000 ...
start "BreastDiagAI - Backend FastAPI" cmd /k "cd backend && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

echo 2. Lancement du Frontend React sur http://localhost:5173 ...
start "BreastDiagAI - Frontend React" cmd /k "cd frontend && npm run dev"

echo.
echo Application lancee !
echo Ouvrez votre navigateur sur : http://localhost:5173
echo Documentation API Swagger :   http://127.0.0.1:8000/docs
echo.
pause
