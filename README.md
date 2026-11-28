# BreastDiagAI

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.13-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%E2%89%A51.2-F7931E?logo=scikitlearn&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react&logoColor=black)
![Données](https://img.shields.io/badge/Donn%C3%A9es-500%20000%20%C3%97%2040-informational)
![Statut](https://img.shields.io/badge/Mod%C3%A8le-non%20entra%C3%AEn%C3%A9-orange)
![Octobre Rose](https://img.shields.io/badge/Octobre-Rose-E91E63)

**Aide au diagnostic du cancer du sein (bénin / malin) par Data Mining et Machine Learning.** Projet académique du **Groupe IASD29**.

> ⚠️ **Avertissement :** outil d'aide à la décision à but pédagogique. Il ne remplace en aucun cas un avis médical. Dans la version actuelle, les prédictions de l'application reposent sur une **heuristique de démonstration** : aucun modèle n'est encore entraîné.

---

## Sommaire

- [Notre histoire](#notre-histoire)
- [Résultats clés](#résultats-clés)
- [Pipeline](#pipeline)
- [Structure des dossiers](#structure-des-dossiers)
- [Exécution en une ligne](#exécution-en-une-ligne-python-311--313)
- [API](#api-fastapi)
- [Documentation](#documentation)
- [Contributions](#contributions)

---

## Notre histoire

Le projet est né d'une expérience personnelle : la découverte d'une anomalie mammaire chez la mère d'un membre de l'équipe, puis un parcours médical long et angoissant (mammographie, échographie, biopsie). BreastDiagAI ne cherche pas à remplacer le médecin. Le but est d'estimer si une tumeur présente des caractéristiques bénignes ou malignes, et d'**expliquer pourquoi**.

## Résultats clés

Les résultats proviennent de `cleaning_report.log`, `pre/preprocessing.log` et du notebook `02_statistical_eda_validation.ipynb`.

| Étape | Résultat |
|---|---|
| Données | 500 000 observations × 40 variables + cible `diagnosis` ; 65 % bénin / 35 % malin |
| Qualité | 0 valeur manquante, 0 doublon ; outliers conservés (max. 1,78 % sur `area_worst`) |
| EDA | 5 variables géométriques discriminantes : `area_worst`, `area_mean`, `radius_mean`, `radius_worst`, `perimeter_mean` |
| Tests statistiques | Shapiro-Wilk, Mann-Whitney U, ANOVA/Kruskal-Wallis, Chi-deux : mêmes 5 variables ; `area_worst` : V de Cramér = 0,858 |
| Prétraitement | Split stratifié 80/20 (400 000 / 100 000), `SimpleImputer(median)` + `RobustScaler`, fit sur TRAIN uniquement |
| Benchmark (Recall / ROC-AUC) | **Résultats non disponibles** (aucun modèle entraîné) |
| Explicabilité SHAP | **Résultats non disponibles** |

## Pipeline

```
CSV brut ──► clean_data.py ──► breast_cancer_cleaned.csv ──► exploratory_analysis.py ─┐
                                                                                       ├─► preprocessing.py ──► X/y train/test + preprocessor.joblib ──► [entraînement : à faire]
             notebooks/01 (audit) · notebooks/02 + statistical_tests.py (EDA + 4 tests) ┘
                                                                                                    app/backend (FastAPI) ◄──► app/frontend (React)
```

## Structure des dossiers

```
BreastDiagAI/
├── app/
│   ├── backend/                 API FastAPI + SQLite
│   │   ├── main.py              Point d'entrée (CORS, routes, fichiers statiques)
│   │   ├── config.py · database.py
│   │   ├── models/              Modèle SQLAlchemy « predictions »
│   │   ├── schemas/             Schémas Pydantic (entrée / sortie)
│   │   ├── routers/             predictions.py, analytics.py
│   │   ├── services/            prediction_service.py (heuristique → futur modèle)
│   │   ├── static/eda_plots/    Graphiques EDA servis au frontend
│   │   └── requirements.txt
│   ├── frontend/                React + Vite + Tailwind (5 pages)
│   ├── docs/                    Documentation de l'interface
│   └── *.bat                    Lanceurs Windows (backend, frontend, les deux)
├── data/
│   ├── raw/README.md            Téléchargement du dataset Kaggle
│   └── processed/README.md      Régénération des données traitées
├── docs/
│   ├── Rapport_Projet.pdf       Rapport scientifique (21 pages)
│   └── build_report.py          Script de génération du rapport (lit les figures de results/eda/)
├── notebooks/
│   ├── 01_data_cleaning_audit.ipynb          Nettoyage, types, audit
│   └── 02_statistical_eda_validation.ipynb   EDA approfondie + 4 tests
├── results/
│   ├── cleaning/                cleaning_report.log, RAPPORT_NETTOYAGE.md
│   └── eda/                     12 figures, stats_by_group.csv, rapport EDA
├── src/
│   ├── clean_data.py            Nettoyage & audit
│   ├── exploratory_analysis.py  Statistiques par groupe, histogrammes, boxplots
│   ├── statistical_tests.py     Shapiro, Mann-Whitney, ANOVA/Kruskal, Chi-deux
│   └── preprocessing.py         Split, imputation, RobustScaler, export
├── requirements.txt
└── README.md
```

> Les CSV (`breast_cancer_40_features_1M.csv`, `breast_cancer_cleaned.csv`, `X_*.csv`, `y_*.csv`) et les `.joblib` ne sont pas versionnés (taille > 100 Mo). Voir `data/raw/README.md`.

## Exécution en une ligne (Python 3.11 / 3.13)

Chaque commande se lance depuis la racine du dépôt. Remplacez `3.11` par `3.13` selon la version installée. Sous Windows, utilisez `py -3.11` au lieu de `python3.11`.

| Action | Commande (une ligne) |
|---|---|
| Installer l'environnement | `python3.11 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt` |
| Nettoyer les données | `python src/clean_data.py --input data/raw/breast_cancer_40_features_1M.csv` |
| Analyse exploratoire | `python src/exploratory_analysis.py --input breast_cancer_cleaned.csv` |
| Prétraitement | `python src/preprocessing.py --input breast_cancer_cleaned.csv` |
| Notebook d'audit | `pip install jupyter && jupyter nbconvert --to notebook --execute notebooks/01_data_cleaning_audit.ipynb` |
| Régénérer le rapport PDF | `pip install reportlab && cd docs && python build_report.py` |
| API FastAPI | `pip install -r app/backend/requirements.txt && cd app/backend && uvicorn main:app --reload` → http://localhost:8000/docs |
| Frontend React | `cd app/frontend && npm install && npm run dev` → http://localhost:5173 |
| Application complète (Windows) | `app\start_app.bat` |
| Interface Streamlit `streamlit run app/streamlit_app.py` | **Non disponible** : `app/streamlit_app.py` n'existe pas encore dans le projet |

Le notebook d'audit trouve le CSV brut automatiquement (dossier courant ou parents). Sinon, définissez `BREASTDIAG_ROOT=<dossier du CSV>`.

## API FastAPI

| Méthode | Route | Rôle |
|---|---|---|
| POST | `/api/predict` | Calcule une prédiction et l'enregistre |
| GET | `/api/predictions` | Historique des prédictions |
| GET | `/api/predictions/{id}` | Détail d'une prédiction |
| DELETE | `/api/predictions/{id}` | Supprime une prédiction |
| GET | `/api/analytics/stats` | Statistiques globales |
| GET | `/health` | État de l'API |

Pour brancher le futur modèle, il suffit de modifier `app/backend/services/prediction_service.py`.

## Documentation

- 📄 [`docs/Rapport_Projet.pdf`](docs/Rapport_Projet.pdf) : rapport scientifique complet (contexte médical, pipeline, 10 figures EDA, 4 tests, benchmark, SHAP, architecture).
- 🧹 [`results/cleaning/RAPPORT_NETTOYAGE.md`](results/cleaning/RAPPORT_NETTOYAGE.md) : rapport de nettoyage.
- 📊 [`results/eda/`](results/eda/) : rapport EDA et figures.
- 🖥️ [`app/docs/DOCUMENTATION_INTERFACE.md`](app/docs/DOCUMENTATION_INTERFACE.md) : guide de l'interface.

## Contributions

Ce tableau est établi à partir de l'historique Git du dépôt et de la section « Équipe » du README précédent.

| Membre | Contributions | Fichiers principaux |
|---|---|---|
| **IASD29** | Création et structure du dépôt, nettoyage des données, rapport de nettoyage, intégration du backend et du frontend, `.gitignore`, README | `src/clean_data.py`, `results/cleaning/`, `app/backend/`, `app/frontend/` |
| **IASD08** | Analyse exploratoire des 40 variables, rapport EDA, module de tests statistiques, notebook 02, 12 figures EDA | `src/exploratory_analysis.py`, `src/statistical_tests.py`, `notebooks/02_*.ipynb`, `results/eda/` |
| **IASD19** | Prétraitement des données et pipeline scikit-learn (split, RobustScaler, ColumnTransformer) | `src/preprocessing.py`, `requirements.txt` |
| **IASD24** | Backend et documentation de l'application, mises à jour du README | `app/backend/`, `app/docs/` |
| **RSD19** | *Aucun commit dans l'historique Git — à compléter par l'équipe* | — |

---

<sub>Projet académique — Groupe IASD29 · Dataset : [Kaggle — Breast Cancer Dataset](https://www.kaggle.com/datasets/sharmajicoder/breast-cancer-dataset)</sub>
