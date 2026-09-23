# Rapport de Nettoyage des Données — BreastDiagAI

**Projet :** Breast Cancer Diagnosis Prediction
**Groupe :** IASD29
**Dataset :** `breast_cancer_40_features_1M.csv`
**Date du traitement :** voir `cleaning_report.log`

---

## 1. Présentation du dataset

| Caractéristique | Valeur |
|---|---|
| Nombre de lignes (observations) | 500 000 |
| Nombre de colonnes | 41 (40 features + 1 cible) |
| Colonne cible | `diagnosis` (0 = bénin, 1 = malin) |
| Taille du fichier brut | ~387 Mo |
| Source | [Kaggle - Breast Cancer Dataset](https://www.kaggle.com/datasets/sharmajicoder/breast-cancer-dataset) |

Les 40 features décrivent des caractéristiques mesurées sur les cellules d'une tumeur : rayon, texture, périmètre, aire, symétrie, concavité, etc. (mesures moyennes, écarts-types et valeurs extrêmes).

---

## 2. Méthodologie de nettoyage

Le nettoyage a été réalisé avec un script Python (`clean_data.py`) structuré en 8 étapes automatisées, avec journalisation complète (`cleaning_report.log`).

### Étape 1 — Chargement des données
Le fichier CSV est chargé avec `pandas`, après vérification que le chemin existe (pour éviter les erreurs silencieuses).

### Étape 2 — Audit initial
Vérification de la mémoire utilisée et des types de données (`float64`, `int64`).

### Étape 3 — Valeurs manquantes
Recherche de cellules vides. **Résultat : 0 valeur manquante** — aucune imputation nécessaire.

### Étape 4 — Doublons
Recherche de lignes strictement identiques. **Résultat : 0 doublon** — aucune suppression nécessaire.

### Étape 5 — Détection des outliers (valeurs aberrantes)
Deux méthodes statistiques complémentaires ont été appliquées :
- **IQR (écart interquartile)** : une valeur est atypique si elle sort de l'intervalle [Q1 − 1.5×IQR ; Q3 + 1.5×IQR]
- **Z-score** : une valeur est atypique si elle est à plus de 4 écarts-types de la moyenne

### Étape 6 — Analyse de corrélation
Recherche de paires de colonnes portant une information redondante (corrélation > 0.95).

### Étape 7 — Équilibre des classes
Analyse de la répartition bénin/malin dans la colonne `diagnosis`.

### Étape 8 — Optimisation mémoire
Conversion des types de données vers des formats plus légers (*downcasting*) sans perte de précision utile.

---

## 3. Résultats obtenus

### 3.1 Valeurs manquantes et doublons
✅ **Aucun problème détecté** — le dataset était déjà propre sur ces deux aspects.

### 3.2 Outliers
Entre **0,3 % et 1,8 %** de valeurs atypiques selon les colonnes (ex : `area_worst` : 1,78 % ; `mitosis_rate` : 0,35 %).

**Interprétation :** dans un contexte médical, ces valeurs extrêmes correspondent probablement à de vrais cas cliniques (tumeurs particulièrement grosses ou agressives), et non à des erreurs de mesure.

**Décision retenue :** ces valeurs sont **conservées** dans le dataset nettoyé, car les supprimer risquerait de retirer au modèle des informations importantes sur les cas graves à détecter.

### 3.3 Corrélations fortes (redondance)
Deux paires de variables fortement corrélées ont été identifiées :

| Paire de variables | Corrélation | Explication |
|---|---|---|
| `radius_mean` ↔ `area_mean` | 0,989 | L'aire d'un cercle dépend directement du rayon (aire = π·r²) |
| `radius_mean` ↔ `radius_worst` | 0,952 | Le rayon moyen et le rayon maximal évoluent ensemble |

**Décision retenue :** ces colonnes sont conservées dans le fichier nettoyé (`breast_cancer_cleaned.csv`), mais **une colonne par paire sera retirée au moment de l'entraînement** du modèle, pour éviter de donner un poids artificiellement élevé à une même information mesurée deux fois.

### 3.4 Équilibre des classes

| Classe | Nombre | Pourcentage |
|---|---|---|
| 0 — Bénin | 325 000 | 65 % |
| 1 — Malin | 175 000 | 35 % |

**Ratio de déséquilibre : 1,86** (modéré, pas critique).

**Solutions proposées :**
1. **`class_weight='balanced'`** *(solution retenue)* : donne plus de poids aux erreurs sur la classe minoritaire pendant l'entraînement, sans modifier les données. Simple à mettre en œuvre avec scikit-learn.
2. **Sur-échantillonnage (SMOTE)** ou **sous-échantillonnage** : rééquilibrer manuellement le nombre d'exemples par classe. Non nécessaire ici, le déséquilibre étant modéré.

### 3.5 Optimisation mémoire

| Avant | Après | Gain |
|---|---|---|
| 156,40 Mo | 76,77 Mo | **-50,9 %** |

Obtenu en convertissant les colonnes `float64` → `float32` et `int64` → types entiers plus petits, sans perte de précision utile pour l'analyse.


##  Prochaine étape

Les données étant nettoyées, documentées et validées, l'étape suivante est l'**entraînement du modèle de classification** (Random Forest), en tenant compte de :
- La suppression de `area_mean` et `radius_worst` (redondance)
- L'utilisation de `class_weight='balanced'` (déséquilibre des classes)
- La conservation des outliers (information clinique potentiellement utile)
