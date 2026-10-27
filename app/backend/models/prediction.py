from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from database import Base

class Prediction(Base):
    """
    Modèle SQLAlchemy pour l'enregistrement de l'historique des prédictions.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    # Caractéristiques principales (Wisconsin Breast Cancer Dataset)
    radius_mean = Column(Float, nullable=False)
    area_worst = Column(Float, nullable=False)
    radius_worst = Column(Float, nullable=False)
    
    # Caractéristiques secondaires optionnelles
    texture_mean = Column(Float, nullable=True)
    perimeter_mean = Column(Float, nullable=True)
    concavity_mean = Column(Float, nullable=True)
    
    # Stockage de l'ensemble des caractéristiques en JSON pour flexibilité future
    features_json = Column(Text, nullable=True)
    
    # Résultat de la prédiction
    diagnosis = Column(String(20), nullable=False, index=True)  # "Bénin" ou "Malin"
    confidence = Column(Float, nullable=False)                  # Score de confiance en % (ex: 94.5)
    risk_level = Column(String(20), nullable=False)            # "Faible", "Modéré", "Élevé"
    notes = Column(Text, nullable=True)                         # Remarques éventuelles
