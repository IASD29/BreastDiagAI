from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    """
    Schéma de validation des données d'entrée pour l'analyse d'une tumeur.
    Mesures issues de la biopsie / ponction mammaire (Wisconsin Breast Cancer format).
    """
    radius_mean: float = Field(
        ...,
        gt=0,
        lt=50,
        description="Rayon moyen des cellules (distances du centre aux points du contour, en mm)"
    )
    area_worst: float = Field(
        ...,
        gt=0,
        lt=5000,
        description="Aire maximale (worst) observée sur les trois plus grandes cellules"
    )
    radius_worst: float = Field(
        ...,
        gt=0,
        lt=60,
        description="Rayon maximal (worst) observé sur les trois plus grandes cellules"
    )
    texture_mean: Optional[float] = Field(
        default=None,
        gt=0,
        lt=50,
        description="Écart-type des valeurs d'échelle de gris"
    )
    perimeter_mean: Optional[float] = Field(
        default=None,
        gt=0,
        lt=300,
        description="Périmètre moyen du contour des cellules"
    )
    concavity_mean: Optional[float] = Field(
        default=None,
        ge=0,
        lt=1.0,
        description="Gravité des portions concaves du contour"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Notes cliniques ou identifiant anonymisé de référence"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "radius_mean": 13.54,
                "area_worst": 572.2,
                "radius_worst": 14.97,
                "texture_mean": 14.36,
                "perimeter_mean": 87.46,
                "concavity_mean": 0.0667,
                "notes": "Échantillon de contrôle bilan annuel"
            }
        }
    }

class PredictionResult(BaseModel):
    """Résultat immédiat renvoyé par le service de prédiction."""
    diagnosis: str = Field(..., description="'Bénin' ou 'Malin'")
    confidence: float = Field(..., description="Pourcentage de certitude (ex: 94.2)")
    risk_level: str = Field(..., description="'Faible', 'Modéré', ou 'Élevé'")
    probability_malignant: float = Field(..., description="Probabilité de malignité calculée (0.0 à 1.0)")
    explanation: str = Field(..., description="Synthèse explicative des indicateurs prédominants")
    disclaimer: str = Field(
        default="Cet outil est une aide à la décision et ne remplace en aucun cas un avis ou un diagnostic médical officiel établi par un professionnel de santé.",
        description="Mention légale d'aide à la décision"
    )

class PredictionRecord(BaseModel):
    """Modèle d'une prédiction persistée en base de données."""
    id: int
    created_at: datetime
    radius_mean: float
    area_worst: float
    radius_worst: float
    texture_mean: Optional[float] = None
    perimeter_mean: Optional[float] = None
    concavity_mean: Optional[float] = None
    diagnosis: str
    confidence: float
    risk_level: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    """Format de réponse paginé ou listé pour l'historique."""
    items: List[PredictionRecord]
    total: int

class AnalyticsStats(BaseModel):
    """Statistiques globales sur l'ensemble des analyses enregistrées."""
    total_predictions: int
    benign_count: int
    malignant_count: int
    benign_percentage: float
    malignant_percentage: float
    average_confidence: float
    latest_prediction_date: Optional[datetime] = None
