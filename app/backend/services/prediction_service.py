"""
Service d'inférence et d'aide au diagnostic pour BreastDiagAI.
Ce module encapsule l'ensemble de la logique de prédiction.

NOTE D'INTÉGRATION :
C'est le SEUL fichier à modifier lorsque le modèle final Random Forest sera disponible.
"""

from typing import Dict, Any
import math

# ==============================================================================
# TODO: Remplacer par le vrai modèle entraîné (model.pkl généré par src/train_model.py).
# Charger avec : joblib.load("model.pkl")
#
# Features attendues dans cet ordre :
# [
#     'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
#     'smoothness_mean', 'compactness_mean', 'concavity_mean',
#     'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
#     'radius_se', 'texture_se', 'perimeter_se', 'area_se',
#     'smoothness_se', 'compactness_se', 'concavity_se',
#     'concave points_se', 'symmetry_se', 'fractal_dimension_se',
#     'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
#     'smoothness_worst', 'compactness_worst', 'concavity_worst',
#     'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
# ]
#
# TODO: charger scaler.pkl et appliquer scaler.transform() avant la prédiction
# Exemple d'intégration future :
# import joblib
# import numpy as np
# _model = joblib.load("model.pkl")
# _scaler = joblib.load("scaler.pkl")
# ==============================================================================


def predict_diagnosis(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fonction isolée d'inférence pour estimer la bénignité ou la malignité d'une lésion mammaire.
    
    Actuellement, cette fonction implémente une heuristique statistique réaliste basée sur
    les distributions empiriques du dataset Wisconsin Breast Cancer (WDBC) :
    - Les seuils discriminants principaux : radius_mean (~14.5 mm), area_worst (~880 mm²), radius_worst (~17.0 mm).
    - Un score sigmoïde continu est calculé pour estimer une probabilité et un taux de confiance réaliste.

    :param features: Dictionnaire contenant les caractéristiques biométriques
                     (ex: {'radius_mean': 14.2, 'area_worst': 780.0, 'radius_worst': 16.1, ...})
    :return: Dictionnaire contenant:
             - diagnosis: 'Bénin' ou 'Malin'
             - confidence: float en pourcentage (ex: 93.4)
             - risk_level: 'Faible', 'Modéré', ou 'Élevé'
             - probability_malignant: float (0.0 à 1.0)
             - explanation: Explication clinique vulgarisée des facteurs d'influence
             - disclaimer: Rappel légal de non-substitution au médecin
    """
    # Extraction des caractéristiques principales avec valeurs par défaut sécurisées
    radius_mean = float(features.get("radius_mean", 14.0))
    area_worst = float(features.get("area_worst", 700.0))
    radius_worst = float(features.get("radius_worst", 15.0))
    
    # Caractéristiques secondaires optionnelles
    concavity_mean = float(features.get("concavity_mean") or 0.05)
    texture_mean = float(features.get("texture_mean") or 19.0)

    # Calcul d'un score combiné normalisé (Z-score approximé selon WDBC)
    # Médianes bénignes typiques : radius_mean ~12.1, area_worst ~550, radius_worst ~13.4
    # Médianes malignes typiques : radius_mean ~17.5, area_worst ~1420, radius_worst ~21.1
    z_radius = (radius_mean - 14.5) / 2.5
    z_area = (area_worst - 880.0) / 300.0
    z_worst = (radius_worst - 16.5) / 3.0
    z_concav = (concavity_mean - 0.08) / 0.06

    score = 0.40 * z_radius + 0.30 * z_area + 0.20 * z_worst + 0.10 * z_concav
    
    # Fonction sigmoïde logistique pour obtenir la probabilité de malignité
    prob_malignant = 1.0 / (1.0 + math.exp(-score))

    # Détermination du diagnostic et du niveau de confiance
    if prob_malignant >= 0.50:
        diagnosis = "Malin"
        confidence = prob_malignant * 100.0
        risk_level = "Élevé" if prob_malignant >= 0.75 else "Modéré"
        
        reasons = []
        if radius_mean > 15.0:
            reasons.append(f"rayon moyen cellulaire élevé ({radius_mean:.1f} mm)")
        if area_worst > 880.0:
            reasons.append(f"aire maximale atypique ({area_worst:.0f} mm²)")
        if radius_worst > 17.0:
            reasons.append(f"taille périphérique importante ({radius_worst:.1f} mm)")
        
        explanation_details = ", ".join(reasons) if reasons else "paramètres morphologiques en faveur d'une atypie"
        explanation = (
            f"Les caractéristiques analysées indiquent une probabilité de malignité de {prob_malignant*100:.1f}%, "
            f"notamment en raison de : {explanation_details}. Une confirmation histologique immédiate est recommandée."
        )
    else:
        diagnosis = "Bénin"
        confidence = (1.0 - prob_malignant) * 100.0
        risk_level = "Faible" if prob_malignant <= 0.25 else "Modéré"
        
        explanation = (
            f"Les marqueurs morphologiques analysés (rayon moyen {radius_mean:.1f} mm, aire max {area_worst:.0f} mm²) "
            f"sont cohérents avec les profils tissulaires bénins (confiance de {confidence:.1f}%). "
            f"Un suivi de contrôle régulier reste conseillé."
        )

    return {
        "diagnosis": diagnosis,
        "confidence": round(confidence, 1),
        "risk_level": risk_level,
        "probability_malignant": round(prob_malignant, 4),
        "explanation": explanation,
        "disclaimer": "Cet outil est une aide à la décision et ne remplace en aucun cas un avis ou un diagnostic médical officiel établi par un professionnel de santé."
    }
