import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  CheckCircle2, 
  AlertTriangle, 
  Sparkles, 
  Layers, 
  TrendingUp, 
  RefreshCw 
} from 'lucide-react';
import { api } from '../services/api';
import MetricCard from '../components/MetricCard';
import Button from '../components/ui/Button';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activePlot, setActivePlot] = useState('heatmap');

  const fetchStats = async () => {
    setLoading(true);
    try {
      const data = await api.getStats();
      setStats(data);
    } catch (err) {
      console.error("Erreur stats:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const baseUrl = api.getBaseUrl();

  const edaPlots = [
    {
      id: 'heatmap',
      title: 'Matrice de Corrélation',
      description: 'Met en évidence la forte colinéarité entre le rayon moyen, le périmètre et l’aire maximale.',
      file: `${baseUrl}/static/eda_plots/correlation_heatmap.svg`,
      insight: 'Observation clé : Le rayon, le périmètre et la surface ont des coefficients > 0.95. Lors de l\'entraînement du Random Forest, cette redondance sera régularisée par le sous-échantillonnage aléatoire des features à chaque split d\'arbre.'
    },
    {
      id: 'histogram',
      title: 'Distribution du Rayon Moyen',
      description: 'Comparaison des distributions de fréquences entre tumeurs bénignes et malignes.',
      file: `${baseUrl}/static/eda_plots/distribution_histogram.svg`,
      insight: 'Observation clé : La valeur seuil critique se situe autour de 14.5 - 15.0 mm. En dessous de 12 mm, la probabilité de bénignité dépasse 92%. Au-delà de 16 mm, la suspicion de malignité croît exponentiellement.'
    },
    {
      id: 'boxplot',
      title: 'Boxplot de l’Aire Maximale (Area Worst)',
      description: 'Dispersion statistique et mise en évidence des valeurs atypiques extrêmes.',
      file: `${baseUrl}/static/eda_plots/boxplot_comparison.svg`,
      insight: 'Observation clé : L’aire maximale présente une séparation très nette entre les deux populations : médiane à 550 mm² pour les cas bénins contre 1420 mm² pour les cas malins.'
    }
  ];

  return (
    <div className="space-y-12 py-6 max-w-6xl mx-auto">
      
      {/* ── En-tête : Titre & Badge parfaitement contrastés ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-light text-primary border border-primary-border text-xs font-bold uppercase tracking-wider mb-2">
            <BarChart3 className="w-3.5 h-3.5 text-primary" />
            Métriques & Visualisation Données (EDA)
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-text tracking-tight">
            Analyses Statistiques & Exploration des Données
          </h1>
          <p className="text-xs sm:text-sm text-text-muted mt-1">
            Indicateurs en temps réel des analyses enregistrées et graphiques exploratoires du dataset de référence.
          </p>
        </div>

        <Button
          variant="secondary"
          size="sm"
          icon={RefreshCw}
          loading={loading}
          onClick={fetchStats}
          className="self-start sm:self-auto"
        >
          Actualiser
        </Button>
      </div>

      {/* ── Cartes KPI avec adaptation totale au thème Clair / Nuit ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <MetricCard
          title="Analyses Réalisées"
          value={stats ? stats.total_predictions : '-'}
          subtitle="Enregistrées en base SQLite"
          icon={Layers}
          color="pink"
        />
        <MetricCard
          title="Cas Bénins Détectés"
          value={stats ? `${stats.benign_percentage}%` : '-'}
          subtitle={stats ? `${stats.benign_count} patientes (Faible risque)` : ''}
          icon={CheckCircle2}
          color="emerald"
        />
        <MetricCard
          title="Cas Malins Détectés"
          value={stats ? `${stats.malignant_percentage}%` : '-'}
          subtitle={stats ? `${stats.malignant_count} patientes (Suspicion élevée)` : ''}
          icon={AlertTriangle}
          color="rose"
        />
        <MetricCard
          title="Confiance Moyenne"
          value={stats ? `${stats.average_confidence}%` : '-'}
          subtitle="Précision estimée du modèle"
          icon={TrendingUp}
          color="blue"
        />
      </div>

      {/* ── Section EDA : Panneau thémé avec contraste et relief ── */}
      <section className="card p-6 sm:p-10 space-y-8">
        
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-border">
          <div>
            <span className="text-xs font-bold text-primary uppercase tracking-widest">
              Analyses Exploratoires Pré-entraînement
            </span>
            <h2 className="text-xl sm:text-2xl font-extrabold text-text mt-1">
              Visualisations Biomédicales
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-text-muted max-w-md">
            Graphiques générés sur les données histologiques pour guider l'ingénierie des variables et l'interprétabilité du futur modèle Random Forest.
          </p>
        </div>

        {/* Sélecteur d'onglets thématisé avec micro-interactions */}
        <div className="flex flex-wrap gap-2">
          {edaPlots.map((plot) => (
            <button
              key={plot.id}
              onClick={() => setActivePlot(plot.id)}
              className={`px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold btn-motion-spring ${
                activePlot === plot.id
                  ? 'btn-brand shadow-primary-glow scale-[1.02]'
                  : 'bg-surface-2 text-text-muted hover:text-text hover:bg-surface-3 border border-border hover:-translate-y-0.5'
              }`}
            >
              {plot.title}
            </button>
          ))}
        </div>

        {/* Affichage du graphique actif */}
        {edaPlots.map((plot) => {
          if (plot.id !== activePlot) return null;
          return (
            <div key={plot.id} className="space-y-6 animate-in fade-in-50 duration-300">
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                
                {/* Cadre SVG adapté avec arrière-plan net */}
                <div className="lg:col-span-8 bg-surface-2 p-3 sm:p-5 rounded-2xl border border-border overflow-hidden flex items-center justify-center">
                  <div className="bg-white rounded-xl p-2 w-full flex items-center justify-center shadow-xs">
                    <img
                      src={plot.file}
                      alt={plot.title}
                      className="w-full h-auto max-h-[460px] object-contain rounded-lg"
                    />
                  </div>
                </div>

                {/* Explications et Interprétation clinique */}
                <div className="lg:col-span-4 space-y-4">
                  <div className="space-y-2">
                    <span className="text-xs font-bold text-primary uppercase tracking-wider">
                      Interprétation Scientifique
                    </span>
                    <h3 className="text-lg font-bold text-text">
                      {plot.title}
                    </h3>
                    <p className="text-xs text-text-muted leading-relaxed">
                      {plot.description}
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-primary-light border border-primary-border space-y-2">
                    <div className="flex items-center gap-1.5 text-primary text-xs font-bold">
                      <Sparkles className="w-4 h-4 text-primary" />
                      <span>Apport pour le Random Forest</span>
                    </div>
                    <p className="text-xs text-text leading-relaxed">
                      {plot.insight}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-xl bg-surface-2 border border-border text-[11px] text-text-muted">
                    <strong className="text-text">Données sources</strong> : 569 prélèvements cellulaires de la base Wisconsin Diagnostic Breast Cancer (WDBC).
                  </div>
                </div>

              </div>

            </div>
          );
        })}

      </section>

    </div>
  );
}
