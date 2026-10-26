import json
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from database import get_db
from models.prediction import Prediction
from schemas.prediction import (
    PredictionInput,
    PredictionResult,
    PredictionRecord,
    HistoryResponse
)
from services.prediction_service import predict_diagnosis

router = APIRouter(prefix="/api", tags=["Predictions"])


@router.post(
    "/predict",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Effectuer une analyse diagnostique et l'enregistrer"
)
def create_prediction(payload: PredictionInput, db: Session = Depends(get_db)):
    """
    Reçoit les caractéristiques morphologiques de la tumeur,
    exécute l'analyse diagnostique via le service de prédiction,
    et enregistre le résultat dans la base de données SQLite.
    """
    try:
        # Exécution de l'analyse (isolée dans services/prediction_service.py)
        result = predict_diagnosis(payload.model_dump())
        
        # Enregistrement en base de données SQLite
        features_dict = payload.model_dump()
        features_json_str = json.dumps(features_dict)
        
        db_prediction = Prediction(
            radius_mean=payload.radius_mean,
            area_worst=payload.area_worst,
            radius_worst=payload.radius_worst,
            texture_mean=payload.texture_mean,
            perimeter_mean=payload.perimeter_mean,
            concavity_mean=payload.concavity_mean,
            features_json=features_json_str,
            diagnosis=result["diagnosis"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            notes=payload.notes
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        return {
            "id": db_prediction.id,
            "created_at": db_prediction.created_at,
            "input": payload.model_dump(),
            "result": result
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse diagnostique : {str(e)}"
        )


@router.get(
    "/predictions",
    response_model=HistoryResponse,
    summary="Récupérer l'historique des prédictions"
)
def get_predictions_history(
    diagnosis: Optional[str] = Query(None, description="Filtrer par 'Bénin' ou 'Malin'"),
    sort_by: str = Query("date_desc", description="Options: date_desc, date_asc, conf_desc, conf_asc"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des prédictions passées enregistrées en base,
    avec prise en charge du filtrage et du tri.
    """
    query = db.query(Prediction)
    
    # Filtrage par diagnostic si spécifié
    if diagnosis and diagnosis in ["Bénin", "Malin"]:
        query = query.filter(Prediction.diagnosis == diagnosis)
        
    # Tri
    if sort_by == "date_asc":
        query = query.order_by(asc(Prediction.created_at))
    elif sort_by == "conf_desc":
        query = query.order_by(desc(Prediction.confidence))
    elif sort_by == "conf_asc":
        query = query.order_by(asc(Prediction.confidence))
    else:  # Par défaut : date_desc
        query = query.order_by(desc(Prediction.created_at))
        
    total = query.count()
    items = query.limit(limit).all()
    
    return HistoryResponse(items=items, total=total)


@router.get(
    "/predictions/{prediction_id}",
    response_model=PredictionRecord,
    summary="Détail d'une prédiction spécifique"
)
def get_prediction_detail(prediction_id: int, db: Session = Depends(get_db)):
    """Obtient le détail complet d'une prédiction à partir de son ID."""
    pred = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not pred:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prédiction #{prediction_id} introuvable"
        )
    return pred


@router.delete(
    "/predictions/{prediction_id}",
    status_code=status.HTTP_200_OK,
    summary="Supprimer une prédiction de l'historique"
)
def delete_prediction(prediction_id: int, db: Session = Depends(get_db)):
    """Supprime un enregistrement de l'historique."""
    pred = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not pred:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prédiction #{prediction_id} introuvable"
        )
    db.delete(pred)
    db.commit()
    return {"message": f"Prédiction #{prediction_id} supprimée avec succès"}
