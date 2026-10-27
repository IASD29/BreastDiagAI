/**
 * Service API pour communiquer avec le backend FastAPI BreastDiagAI.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = 'Une erreur est survenue lors de la communication avec le serveur.';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        if (Array.isArray(errorData.detail)) {
          errorDetail = errorData.detail.map(d => `${d.loc ? d.loc.join('.') + ': ' : ''}${d.msg}`).join('\n');
        } else {
          errorDetail = errorData.detail;
        }
      }
    } catch {
      errorDetail = `Erreur HTTP ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

export const api = {
  /**
   * Envoie les caractéristiques pour prédiction et enregistrement en base.
   */
  async predict(features) {
    const response = await fetch(`${API_BASE_URL}/api/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });
    return handleResponse(response);
  },

  /**
   * Récupère l'historique des prédictions avec filtres optionnels.
   */
  async getPredictions(params = {}) {
    const query = new URLSearchParams();
    if (params.diagnosis && params.diagnosis !== 'Tous') {
      query.append('diagnosis', params.diagnosis);
    }
    if (params.sortBy) {
      query.append('sort_by', params.sortBy);
    }
    if (params.limit) {
      query.append('limit', params.limit);
    }

    const url = `${API_BASE_URL}/api/predictions${query.toString() ? '?' + query.toString() : ''}`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  /**
   * Supprime une prédiction de l'historique.
   */
  async deletePrediction(id) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },

  /**
   * Récupère les métriques et statistiques globales.
   */
  async getStats() {
    const response = await fetch(`${API_BASE_URL}/api/analytics/stats`);
    return handleResponse(response);
  },

  /**
   * Vérifie l'état de l'API backend.
   */
  async checkHealth() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  },
  
  /**
   * URL de base pour les assets statiques (EDA plots).
   */
  getBaseUrl() {
    return API_BASE_URL;
  }
};
