# BreastDiagAI

Prédiction du diagnostic du cancer du sein (bénin / malin) à partir de données médicales.

## Notre histoire

Ce projet est né d'une expérience personnelle : la découverte d'une anomalie mammaire chez la mère d'un membre de l'équipe, et le parcours médical long et angoissant qui a suivi (mammographie, échographie, biopsie...).

De cette expérience est née une question : l'intelligence artificielle peut-elle aider à détecter plus rapidement les situations nécessitant une attention médicale ?

BreastDiagAI n'a pas pour but de remplacer le médecin, mais d'offrir un outil d'aide à la décision, capable d'estimer si une tumeur présente des caractéristiques bénignes ou malignes, et d'expliquer pourquoi, pour rendre le dépistage plus rapide, accessible et compréhensible.

> **Avertissement :** cet outil est une aide à la décision à but pédagogique. Il ne remplace en aucun cas un avis médical.

## Objectif

Prédire le diagnostic (bénin / malin) du cancer du sein à partir de données médicales.

## Dataset

- Source : [Kaggle - Breast Cancer Dataset](https://www.kaggle.com/datasets/sharmajicoder/breast-cancer-dataset)
- Taille : 500 000 observations
- Voir `data/raw/README.md` pour les instructions de téléchargement.

## Structure du projet

```
BreastDiagAI
├── app/                  Application web
│   ├── frontend/         Interface (React, Vite, Tailwind CSS)
│   ├── backend/          API (FastAPI, SQLite, modèle Random Forest)
│   ├── docs/             Documentation de l'application
│   ├── run_backend.bat
│   ├── run_frontend.bat
│   └── start_app.bat
├── data/                 Informations sur le dataset (non inclus, trop volumineux)
├── notebooks/            Notebooks d'entraînement et d'analyse
├── results/              Résultats, graphiques, modèle entraîné
│   ├── cleaning/         Rapports de nettoyage
│   └── eda/              Visualisations et statistiques EDA
├── src/                  Scripts (nettoyage, EDA, prétraitement)
│   ├── clean_data.py
│   ├── exploratory_analysis.py
│   └── preprocessing.py
├── requirements.txt      Dépendances du pipeline de Data Science / ML
└── README.md
```

## ⚙️ Pipeline de Prétraitement des Données (`src/preprocessing.py`)

Le script `src/preprocessing.py` standardise et automatise les étapes de prétraitement pour alimenter les modèles d'apprentissage :

1. **Séparation X / y** : Extraction de la variable cible `diagnosis` et conservation intégrale des 40 variables explicatives numériques (conformément aux conclusions de l'EDA).
2. **Train / Test Split stratifié (80 / 20)** : Stratification stricte sur `y` (`random_state=42`) garantissant la parité de répartition 65% bénin (0) / 35% malin (1).
3. **Imputation préventive** : `SimpleImputer(strategy='median')` pour prémunir le pipeline contre les valeurs manquantes.
4. **Encodage** : `LabelEncoder` pour la variable cible `y` ; `OneHotEncoder` conditionnel pour toute colonne catégorielle.
5. **Normalisation robuste (`RobustScaler`)** : Retenu face à `StandardScaler` et `MinMaxScaler` pour sa résilience aux valeurs aberrantes avérées (jusqu'à 1.78% d'outliers sur `area_worst`) grâce à l'utilisation de la médiane et de l'IQR.
6. **Pipeline scikit-learn & ColumnTransformer** : Ajustement (`fit`) strictement confiné au sous-ensemble **TRAIN** (aucun risque de *Data Leakage*), puis transformation (`transform`) sur **TRAIN** et **TEST**.
7. **Export des artéfacts** :
   - Fichiers générés : `X_train.csv`, `X_test.csv`, `y_train.csv`, `y_test.csv` (non versionnés sur Git en raison de leur volume)
   - Modèle de préprocessing sérialisé : `preprocessor.joblib`
   - Rapport d'exécution détaillé : `preprocessing.log`

### Exécution du prétraitement

```bash
# Installation des dépendances
pip install -r requirements.txt

# Exécution du script
python src/preprocessing.py --input breast_cancer_cleaned.csv --output-dir .
```

## Application web

L'application permet de saisir les caractéristiques d'une tumeur et d'obtenir une prédiction avec un indice de confiance.

**Pages :** Accueil, Prédiction, Historique, Analytiques, Notre histoire.

**Fonctionnalités :**

- Prédiction bénin / malin avec indice de confiance
- Historique des prédictions enregistrées
- Visualisations d'analyse exploratoire (EDA)
- Thèmes clair et nuit, interface adaptée au mobile

**Technologies :**

- Frontend : React, Vite, Tailwind CSS
- Backend : Python, FastAPI, SQLite
- Modèle : Random Forest

### Lancer l'application

**Prérequis :** Node.js et Python 3.

**Méthode rapide (Windows) :** double-cliquez sur `app/start_app.bat`.

**Méthode manuelle :**

1. Backend

```bash
cd app/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API et documentation : http://localhost:8000/docs

2. Frontend (dans un second terminal)

```bash
cd app/frontend
npm install
npm run dev
```

Application : http://localhost:5173

### Endpoints principaux

| Méthode | Route | Rôle |
|---|---|---|
| POST | `/api/predict` | Calculer une prédiction |
| GET | `/api/predictions` | Lister l'historique |
| GET | `/api/analytics` | Statistiques et analyses |

## Entraîner le modèle

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Télécharger le dataset (voir `data/raw/README.md`)
3. Nettoyer les données :
   ```bash
   python src/clean_data.py --input data/raw/breast_cancer_40_features_1M.csv
   ```
4. Exécuter le prétraitement :
   ```bash
   python src/preprocessing.py --input breast_cancer_cleaned.csv
   ```
5. Ouvrir et exécuter `notebooks/training.ipynb`

## Équipe : Groupe IASD29

- IASD29
- IASD08
- IASD19 (Prétraitement des données & Pipeline Scikit-Learn)
- IASD24
- RSD19

**Répartition pour l'application :** Frontend et UX (interface, design system), Backend et IA (API, base de données, modèle).
