"""
preprocessing.py
================
Pipeline de prétraitement des données (Data Preprocessing) — Projet BreastDiagAI
Application du chapitre "Data Preprocessing" (TP Data Mining, pages 43-55) :

1. Chargement et séparation X / y (cible : 'diagnosis')
2. Division Train / Test (80/20, stratifié sur y, random_state=42)
3. Imputation : SimpleImputer(strategy='median') (sécurité préventive)
4. Encodage :
   - LabelEncoder sur la variable cible y
   - OneHotEncoder sur les colonnes catégorielles si présentes
5. Comparaison des Scalers (RobustScaler vs StandardScaler vs MinMaxScaler)
   - RobustScaler retenu en raison de la présence avérée d'outliers
6. Construction du ColumnTransformer & Pipeline scikit-learn
   - Fit sur le jeu d'entraînement TRAIN uniquement (anti-data leakage)
   - Transform sur TRAIN et TEST
7. Export des jeux transformés et de l'objet préprocesseur :
   - X_train.csv, X_test.csv, y_train.csv, y_test.csv
   - preprocessor.joblib

Auteur : Équipe Data Science / BreastDiagAI
"""

import argparse
import logging
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    LabelEncoder,
    MinMaxScaler,
    OneHotEncoder,
    RobustScaler,
    StandardScaler,
)

# ----------------------------------------------------------------------
# Configuration du logging (console + fichier preprocessing.log)
# Format identique à cleaning_report.log : HH:MM:SS | INFO     | message
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("preprocessing.log", mode="w", encoding="utf-8"),
    ],
)
logger = logging.getLogger("BreastDiagAI-Preprocessing")

TARGET_COL = "diagnosis"


# ----------------------------------------------------------------------
# 1. CHARGEMENT ET AUDIT PRÉ-TRAITEMENT
# ----------------------------------------------------------------------
def load_dataset(path: str | Path) -> pd.DataFrame:
    """
    Charge le dataset nettoyé à partir du chemin spécifié.
    Vérifie l'existence du fichier et loggue les dimensions initiales.
    """
    t0 = time.time()
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"Fichier introuvable : {file_path.resolve()}")
        logger.error("-> Veuillez exécuter clean_data.py au préalable.")
        sys.exit(1)

    logger.info(f"Chargement du dataset : {file_path.name} ...")
    df = pd.read_csv(file_path)
    elapsed = time.time() - t0
    logger.info(
        f"Chargement terminé en {elapsed:.2f}s : {df.shape[0]:,} lignes x {df.shape[1]} colonnes"
    )

    # Vérification des NaN
    total_nan = df.isna().sum().sum()
    logger.info(f"Vérification des valeurs manquantes initiales : {total_nan} NaN détecté(s).")

    return df


# ----------------------------------------------------------------------
# 2. SÉPARATION X / y
# ----------------------------------------------------------------------
def separate_features_target(
    df: pd.DataFrame, target_col: str = TARGET_COL
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Sépare la matrice des variables explicatives X de la variable cible y.
    Conserve les 40 features conformément aux conclusions de l'EDA.
    """
    logger.info("=== ÉTAPE 1 : SÉPARATION X / y ===")
    if target_col not in df.columns:
        logger.error(f"Colonne cible '{target_col}' introuvable dans le DataFrame !")
        sys.exit(1)

    X = df.drop(columns=[target_col]).copy()
    y = df[target_col].copy()

    logger.info(f"Dimensions de X (features) : {X.shape[0]:,} lignes x {X.shape[1]} colonnes")
    logger.info(f"Dimensions de y (cible '{target_col}') : {y.shape[0]:,} observations")
    logger.info(f"Décision EDA validée : l'ensemble des {X.shape[1]} features numériques est conservé.")

    return X, y


# ----------------------------------------------------------------------
# 3. TRAIN / TEST SPLIT STRATIFIÉ
# ----------------------------------------------------------------------
def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.20,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Divise les données en ensembles d'entraînement (80%) et de test (20%).
    Stratification basée sur y pour conserver le ratio 65/35 entre les classes.
    """
    logger.info("=== ÉTAPE 2 : DÉCOUPAGE TRAIN / TEST (80 / 20) ===")
    t0 = time.time()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )
    elapsed = time.time() - t0

    logger.info(f"Découpage réalisé en {elapsed:.3f}s (random_state={random_state}, test_size={test_size:.2f})")
    logger.info(f"  Ensemble TRAIN : X_train={X_train.shape}, y_train={y_train.shape}")
    logger.info(f"  Ensemble TEST  : X_test={X_test.shape}, y_test={y_test.shape}")

    # Répartition des classes
    train_dist = y_train.value_counts(normalize=True) * 100
    train_counts = y_train.value_counts()
    test_dist = y_test.value_counts(normalize=True) * 100
    test_counts = y_test.value_counts()

    logger.info("Répartition des classes (Stratification) :")
    for cls in sorted(y.unique()):
        logger.info(
            f"  Classe {cls} -> TRAIN : {train_counts[cls]:,} obs ({train_dist[cls]:.2f}%) "
            f"| TEST : {test_counts[cls]:,} obs ({test_dist[cls]:.2f}%)"
        )

    return X_train, X_test, y_train, y_test


# ----------------------------------------------------------------------
# 4. ENCODAGE DE LA VARIABLE CIBLE (LabelEncoder)
# ----------------------------------------------------------------------
def encode_target(
    y_train: pd.Series, y_test: pd.Series
) -> tuple[pd.Series, pd.Series, LabelEncoder]:
    """
    Encode la variable cible avec LabelEncoder (ajusté sur le TRAIN uniquement).
    """
    logger.info("=== ÉTAPE 3 : ENCODAGE DE LA CIBLE (LabelEncoder) ===")
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_test_encoded = le.transform(y_test)

    # Conversion en Series Pandas pour préserver l'intégrité
    y_train_s = pd.Series(y_train_encoded, index=y_train.index, name=TARGET_COL)
    y_test_s = pd.Series(y_test_encoded, index=y_test.index, name=TARGET_COL)

    classes_mapping = {int(cls): int(label) for label, cls in enumerate(le.classes_)}
    logger.info(f"Classes détectées et encodées : {classes_mapping}")
    logger.info(f"y_train encodé : {y_train_s.shape} | y_test encodé : {y_test_s.shape}")

    return y_train_s, y_test_s, le


# ----------------------------------------------------------------------
# 5. COMPARAISON PRÉALABLE DES SCALERS
# ----------------------------------------------------------------------
def compare_scalers(
    X_train: pd.DataFrame, sample_cols: list[str] | None = None
) -> None:
    """
    Compare brièvement le comportement de RobustScaler, StandardScaler et
    MinMaxScaler sur un sous-ensemble de variables clés présentant des outliers.
    Affiche les statistiques descriptives avant et après transformation dans les logs.
    """
    logger.info("=== ÉTAPE 4 : COMPARAISON DES MÉTHODES DE SCALING ===")
    if sample_cols is None:
        # Variables mises en avant lors du nettoyage et de l'EDA
        candidate_cols = ["area_worst", "area_mean", "radius_mean"]
        sample_cols = [c for c in candidate_cols if c in X_train.columns]
        if not sample_cols:
            sample_cols = list(X_train.columns[:3])

    logger.info(
        f"Comparaison effectuée sur les variables représentatives à fort taux d'outliers : {sample_cols}"
    )

    scalers = {
        "StandardScaler": StandardScaler(),
        "MinMaxScaler": MinMaxScaler(),
        "RobustScaler": RobustScaler(),
    }

    sample_df = X_train[sample_cols].copy()

    for col in sample_cols:
        raw_series = sample_df[col]
        logger.info(f"--- Statistiques brutes pour '{col}' (AVANT scaling) ---")
        logger.info(
            f"  Min: {raw_series.min():.3f} | Max: {raw_series.max():.3f} | "
            f"Moyenne: {raw_series.mean():.3f} | Médiane: {raw_series.median():.3f} | "
            f"Écart-type: {raw_series.std():.3f} | IQR: {(raw_series.quantile(0.75) - raw_series.quantile(0.25)):.3f}"
        )

        for name, scaler in scalers.items():
            scaled_vals = scaler.fit_transform(sample_df[[col]]).flatten()
            q25, q75 = np.percentile(scaled_vals, [25, 75])
            iqr = q75 - q25
            logger.info(
                f"  [{name:14s}] Min: {scaled_vals.min():8.3f} | Max: {scaled_vals.max():8.3f} | "
                f"Moyenne: {scaled_vals.mean():8.3f} | Médiane: {np.median(scaled_vals):8.3f} | "
                f"Écart-type: {scaled_vals.std():8.3f} | IQR: {iqr:8.3f}"
            )

    logger.info(">>> CHOIX DU SCALER : RobustScaler retenu.")
    logger.info(
        "    Justification : En présence d'outliers documentés lors du nettoyage (jusqu'à 1.78% sur area_worst), "
        "StandardScaler compresse excessivement les données non aberrantes à cause de la variance gonflée, "
        "et MinMaxScaler est totalement écrasé par les extremums. "
        "RobustScaler utilise la médiane et l'IQR (interquartile), restant ainsi insensible aux valeurs aberrantes."
    )


# ----------------------------------------------------------------------
# 6. CONSTRUCTION DU PIPELINE & COLUMN TRANSFORMER
# ----------------------------------------------------------------------
def build_preprocessing_pipeline(
    X_train: pd.DataFrame,
) -> tuple[ColumnTransformer, list[str], list[str]]:
    """
    Construit le préprocesseur complet combinant SimpleImputer, Encodage
    et RobustScaler au sein d'un Pipeline et make_column_transformer.
    """
    logger.info("=== ÉTAPE 5 : CONSTRUCTION DU PIPELINE DE PRÉTRAITEMENT ===")

    numerical_cols = list(X_train.select_dtypes(include=[np.number]).columns)
    categorical_cols = list(X_train.select_dtypes(include=["object", "category"]).columns)

    logger.info(f"Colonnes numériques identifiées   : {len(numerical_cols)}")
    logger.info(f"Colonnes catégorielles identifiées : {len(categorical_cols)}")

    # 1. Pipeline numérique : Imputation par la médiane + RobustScaler
    num_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )

    transformers = []
    transformers.append(("num", num_pipeline, numerical_cols))

    # 2. Pipeline catégoriel : Imputation + OneHotEncoder si nécessaire
    if categorical_cols:
        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]
        )
        transformers.append(("cat", cat_pipeline, categorical_cols))
        logger.info(f"Pipeline catégoriel activé pour {len(categorical_cols)} colonne(s).")
    else:
        logger.info("Aucune colonne catégorielle détectée dans le jeu de features.")

    # Assemblage via ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
        verbose_feature_names_out=False,
    )

    logger.info(
        "Structure du préprocesseur assemblée : "
        "SimpleImputer(strategy='median') + RobustScaler() sur toutes les features numériques."
    )

    return preprocessor, numerical_cols, categorical_cols


# ----------------------------------------------------------------------
# 7. FIT ET TRANSFORM (PRÉVENTION DU DATA LEAKAGE)
# ----------------------------------------------------------------------
def apply_preprocessing(
    preprocessor: ColumnTransformer,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    numerical_cols: list[str],
    categorical_cols: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, ColumnTransformer]:
    """
    Ajuste (fit) le préprocesseur UNIQUEMENT sur le jeu d'entraînement TRAIN.
    Applique la transformation (transform) sur TRAIN et TEST.
    Garantit l'absence totale de fuite de données (Data Leakage).
    """
    logger.info("=== ÉTAPE 6 : FIT SUR TRAIN & TRANSFORM SUR TRAIN/TEST ===")
    t0 = time.time()

    # Fit uniquement sur TRAIN
    logger.info("Fit du préprocesseur sur X_train (TRAIN uniquement, pas de data leakage)...")
    preprocessor.fit(X_train)
    fit_time = time.time() - t0
    logger.info(f"Fit achevé avec succès en {fit_time:.2f}s.")

    # Transformation de X_train et X_test
    t1 = time.time()
    X_train_transformed = preprocessor.transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)
    trans_time = time.time() - t1
    logger.info(f"Transform sur TRAIN et TEST achevé en {trans_time:.2f}s.")

    # Récupération des noms de colonnes pour reconstituer des DataFrames propres
    try:
        feature_names = list(preprocessor.get_feature_names_out())
    except Exception:
        feature_names = list(numerical_cols)

    # Conversion en DataFrames pandas avec types optimisés
    X_train_clean = pd.DataFrame(
        X_train_transformed, columns=feature_names, index=X_train.index
    )
    X_test_clean = pd.DataFrame(
        X_test_transformed, columns=feature_names, index=X_test.index
    )

    logger.info(f"Forme finale X_train_clean : {X_train_clean.shape}")
    logger.info(f"Forme finale X_test_clean  : {X_test_clean.shape}")
    logger.info(
        f"Contrôle NaN post-transformation : "
        f"X_train={X_train_clean.isna().sum().sum()}, X_test={X_test_clean.isna().sum().sum()}"
    )

    return X_train_clean, X_test_clean, preprocessor


# ----------------------------------------------------------------------
# 8. EXPORT DES RÉSULTATS ET ARTÉFACTS
# ----------------------------------------------------------------------
def export_artifacts(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
    output_dir: Path | str = ".",
) -> None:
    """
    Exporte les jeux d'entraînement et de test pré-traités en CSV,
    ainsi que l'objet preprocessor.joblib réutilisable en inférence.
    """
    logger.info("=== ÉTAPE 7 : EXPORT DES JEUX PRÉ-TRAITÉS ET DU MODÈLE ===")
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    files_to_export = [
        ("X_train.csv", X_train),
        ("X_test.csv", X_test),
        ("y_train.csv", y_train.to_frame()),
        ("y_test.csv", y_test.to_frame()),
    ]

    t0 = time.time()
    for filename, df_obj in files_to_export:
        fpath = out_path / filename
        logger.info(f"Export de {filename} ({df_obj.shape[0]:,} lignes x {df_obj.shape[1]} colonnes)...")
        df_obj.to_csv(fpath, index=False)
        size_mb = fpath.stat().st_size / (1024 * 1024)
        logger.info(f"  -> {filename} sauvegardé ({size_mb:.2f} Mo)")

    # Export du pipeline scikit-learn
    joblib_path = out_path / "preprocessor.joblib"
    logger.info(f"Sérialisation du pipeline dans {joblib_path.name}...")
    joblib.dump(preprocessor, joblib_path)
    joblib_size_kb = joblib_path.stat().st_size / 1024
    logger.info(f"  -> {joblib_path.name} sauvegardé ({joblib_size_kb:.2f} Ko)")

    total_export_time = time.time() - t0
    logger.info(f"Ensemble des artéfacts exporté avec succès en {total_export_time:.2f}s.")


# ----------------------------------------------------------------------
# POINT D'ENTRÉE PRINCIPAL (main)
# ----------------------------------------------------------------------
def main() -> None:
    """Fonction principale orchestrant le flux de data preprocessing."""
    parser = argparse.ArgumentParser(
        description="Pipeline de Data Preprocessing pour le dataset Breast Cancer (BreastDiagAI)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="breast_cancer_cleaned.csv",
        help="Chemin du dataset nettoyé d'entrée (défaut : breast_cancer_cleaned.csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Dossier d'export des fichiers pré-traités (défaut : .)",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.20,
        help="Proportion de l'ensemble de test (défaut : 0.20)",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Graine aléatoire pour la reproductibilité (défaut : 42)",
    )
    args = parser.parse_args()

    start_total_time = time.time()
    logger.info("======================================================================")
    logger.info("DÉMARRAGE DU PIPELINE DE DATA PREPROCESSING (BreastDiagAI)")
    logger.info("======================================================================")

    # 1. Chargement
    df = load_dataset(args.input)

    # 2. Séparation X / y
    X, y = separate_features_target(df, target_col=TARGET_COL)

    # 3. Train / Test Split
    X_train, X_test, y_train, y_test = split_train_test(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    # 4. Encodage de la variable cible
    y_train_enc, y_test_enc, label_encoder = encode_target(y_train, y_test)

    # 5. Comparaison des Scalers
    compare_scalers(X_train)

    # 6. Construction du pipeline
    preprocessor, num_cols, cat_cols = build_preprocessing_pipeline(X_train)

    # 7. Fit & Transform
    X_train_proc, X_test_proc, fitted_preprocessor = apply_preprocessing(
        preprocessor, X_train, X_test, num_cols, cat_cols
    )

    # 8. Export des fichiers
    export_artifacts(
        X_train=X_train_proc,
        X_test=X_test_proc,
        y_train=y_train_enc,
        y_test=y_test_enc,
        preprocessor=fitted_preprocessor,
        output_dir=args.output_dir,
    )

    total_time = time.time() - start_total_time
    logger.info("======================================================================")
    logger.info(f"PIPELINE DE PRÉTRAITEMENT TERMINÉ AVEC SUCCÈS en {total_time:.2f} secondes !")
    logger.info("Fichiers générés :")
    logger.info("  - X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    logger.info("  - preprocessor.joblib")
    logger.info("  - preprocessing.log")
    logger.info("======================================================================")


if __name__ == "__main__":
    main()
