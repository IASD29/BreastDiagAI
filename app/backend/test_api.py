"""
Script de test automatisé des endpoints de l'API BreastDiagAI.
"""
import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("[OK] Health check passed!")

def test_predict_benign():
    payload = {
        "radius_mean": 12.0,
        "area_worst": 520.0,
        "radius_worst": 13.5,
        "notes": "Test Bénin"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["diagnosis"] == "Bénin"
    assert data["result"]["confidence"] > 50.0
    print(f"[OK] Prediction Benign passed: {data['result']['diagnosis']} ({data['result']['confidence']}%)")

def test_predict_malignant():
    payload = {
        "radius_mean": 18.5,
        "area_worst": 1650.0,
        "radius_worst": 24.0,
        "notes": "Test Malin"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["result"]["diagnosis"] == "Malin"
    assert data["result"]["confidence"] > 50.0
    print(f"[OK] Prediction Malignant passed: {data['result']['diagnosis']} ({data['result']['confidence']}%)")

def test_predictions_history():
    response = client.get("/api/predictions")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    print(f"[OK] History check passed: {data['total']} items in database")

def test_analytics_stats():
    response = client.get("/api/analytics/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_predictions"] >= 2
    assert "benign_percentage" in stats
    assert "malignant_percentage" in stats
    print(f"[OK] Analytics stats passed: {stats['benign_percentage']}% Bénin, {stats['malignant_percentage']}% Malin")

def test_static_eda_plot():
    response = client.get("/static/eda_plots/correlation_heatmap.svg")
    assert response.status_code == 200
    assert "<svg" in response.text
    print("[OK] Static EDA plot served successfully!")

if __name__ == "__main__":
    print("\n--- Demarrage des tests de l'API BreastDiagAI ---")
    test_health()
    test_predict_benign()
    test_predict_malignant()
    test_predictions_history()
    test_analytics_stats()
    test_static_eda_plot()
    print(">>> Tous les tests backend ont reussi avec succes !\n")
