from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.prediction import Prediction
from schemas.prediction import AnalyticsStats

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/stats", response_model=AnalyticsStats, summary="Statistiques globales des analyses")
def get_analytics_stats(db: Session = Depends(get_db)):
    """
    Calcule les métriques globales sur l'ensemble de l'historique des prédictions :
    - Nombre total de prédictions
    - Répartition Bénin / Malin (comptes et pourcentages)
    - Confiance moyenne globale
    - Date de la dernière prédiction
    """
    total = db.query(Prediction).count()
    
    if total == 0:
        return AnalyticsStats(
            total_predictions=0,
            benign_count=0,
            malignant_count=0,
            benign_percentage=0.0,
            malignant_percentage=0.0,
            average_confidence=0.0,
            latest_prediction_date=None
        )
        
    benign_count = db.query(Prediction).filter(Prediction.diagnosis == "Bénin").count()
    malignant_count = db.query(Prediction).filter(Prediction.diagnosis == "Malin").count()
    
    avg_conf = db.query(func.avg(Prediction.confidence)).scalar() or 0.0
    latest = db.query(Prediction.created_at).order_by(Prediction.created_at.desc()).first()
    latest_date = latest[0] if latest else None
    
    benign_pct = round((benign_count / total) * 100.0, 1)
    malignant_pct = round((malignant_count / total) * 100.0, 1)
    
    return AnalyticsStats(
        total_predictions=total,
        benign_count=benign_count,
        malignant_count=malignant_count,
        benign_percentage=benign_pct,
        malignant_percentage=malignant_pct,
        average_confidence=round(float(avg_conf), 1),
        latest_prediction_date=latest_date
    )
