"""
Point d'entrée principal de l'API FastAPI BreastDiagAI.
Gère le cycle de vie de l'application, les routes, les middlewares CORS et les fichiers statiques.
"""

import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import CORS_ORIGINS, STATIC_DIR
from database import engine, Base, SessionLocal
from models.prediction import Prediction
from routers.predictions import router as predictions_router
from routers.analytics import router as analytics_router


def populate_initial_samples():
    """Initialise quelques prédictions de démonstration représentatives si la base est vide."""
    db = SessionLocal()
    try:
        if db.query(Prediction).count() == 0:
            sample_records = [
                Prediction(
                    radius_mean=12.45,
                    area_worst=546.7,
                    radius_worst=13.84,
                    texture_mean=15.70,
                    perimeter_mean=78.27,
                    concavity_mean=0.038,
                    features_json=json.dumps({
                        "radius_mean": 12.45,
                        "area_worst": 546.7,
                        "radius_worst": 13.84,
                        "texture_mean": 15.70,
                        "perimeter_mean": 78.27,
                        "concavity_mean": 0.038
                    }),
                    diagnosis="Bénin",
                    confidence=95.4,
                    risk_level="Faible",
                    notes="Contrôle systématique annuel - Rassemblement Octobre Rose"
                ),
                Prediction(
                    radius_mean=17.99,
                    area_worst=1682.0,
                    radius_worst=25.38,
                    texture_mean=20.38,
                    perimeter_mean=122.8,
                    concavity_mean=0.282,
                    features_json=json.dumps({
                        "radius_mean": 17.99,
                        "area_worst": 1682.0,
                        "radius_worst": 25.38,
                        "texture_mean": 20.38,
                        "perimeter_mean": 122.8,
                        "concavity_mean": 0.282
                    }),
                    diagnosis="Malin",
                    confidence=97.8,
                    risk_level="Élevé",
                    notes="Échographie montrant une lésion spiculée du quadrant supéro-externe"
                ),
                Prediction(
                    radius_mean=13.03,
                    area_worst=624.1,
                    radius_worst=14.96,
                    texture_mean=18.42,
                    perimeter_mean=82.61,
                    concavity_mean=0.045,
                    features_json=json.dumps({
                        "radius_mean": 13.03,
                        "area_worst": 624.1,
                        "radius_worst": 14.96,
                        "texture_mean": 18.42,
                        "perimeter_mean": 82.61,
                        "concavity_mean": 0.045
                    }),
                    diagnosis="Bénin",
                    confidence=91.2,
                    risk_level="Faible",
                    notes="Nodule régulier bien circonscrit (kyste probable)"
                )
            ]
            db.add_all(sample_records)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Création des tables SQLite au démarrage
    Base.metadata.create_all(bind=engine)
    populate_initial_samples()
    yield


app = FastAPI(
    title="BreastDiagAI API - Octobre Rose",
    description="API REST d'aide au diagnostic du cancer du sein (bénin/malin) basée sur le Machine Learning.",
    version="1.0.0",
    lifespan=lifespan
)

# Configuration CORS pour autoriser les requêtes du frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fichiers statiques (graphiques EDA : histogrammes, boxplots, heatmap)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Enregistrement des routeurs
app.include_router(predictions_router)
app.include_router(analytics_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "app": "BreastDiagAI API",
        "campaign": "Octobre Rose 🎗️",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "database": "connected"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
