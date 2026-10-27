import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
EDA_DIR = STATIC_DIR / "eda_plots"
DATABASE_URL = f"sqlite:///{BASE_DIR}/breastdiagai.db"

# Configuration CORS pour le frontend React
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

# Assurer l'existence des répertoires statiques
os.makedirs(EDA_DIR, exist_ok=True)
