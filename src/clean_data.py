"""
clean_data.py
=============
Pipeline de nettoyage de données — Projet BreastDiagAI (Groupe IASD29)

Ce script effectue un nettoyage complet et professionnel du dataset
breast_cancer_40_features_1M.csv :
    1. Chargement robuste (avec gestion du chemin)
    2. Audit initial (types, mémoire, aperçu)
    3. Traitement des valeurs manquantes
    4. Traitement des doublons
    5. Détection des outliers (IQR + Z-score)
    6. Analyse de la corrélation entre features
    7. Analyse de l'équilibre des classes (diagnosis)
    8. Optimisation mémoire (downcasting)
    9. Export du dataset nettoyé + rapport de nettoyage (log)

Usage :
    python clean_data.py --input "chemin/vers/breast_cancer_40_features_1M.csv"


"""

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# ----------------------------------------------------------------------
# Configuration du logging (affiche les étapes dans la console + fichier)
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("cleaning_report.log", mode="w", encoding="utf-8"),
    ],
)
logger = logging.getLogger("BreastDiagAI-Cleaning")

TARGET_COL = "diagnosis"


# ----------------------------------------------------------------------
# 1. CHARGEMENT
# ----------------------------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    """Charge le CSV en vérifiant d'abord que le fichier existe."""
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"Fichier introuvable : {file_path.resolve()}")
        logger.error("-> Vérifie le chemin, ou place le CSV dans le même dossier que ce script.")
        sys.exit(1)

    logger.info(f"Chargement de {file_path.name} ...")
    df = pd.read_csv(file_path)
    logger.info(f"Chargement terminé : {df.shape[0]:,} lignes x {df.shape[1]} colonnes")
    return df


# ----------------------------------------------------------------------
# 2. AUDIT INITIAL
# ----------------------------------------------------------------------
def initial_audit(df: pd.DataFrame) -> None:
    logger.info("=== AUDIT INITIAL ===")
    mem_mb = df.memory_usage(deep=True).sum() / 1024**2
    logger.info(f"Mémoire utilisée : {mem_mb:.2f} Mo")
    logger.info(f"Types de données :\n{df.dtypes.value_counts().to_string()}")

    if TARGET_COL not in df.columns:
        logger.warning(f"Colonne cible '{TARGET_COL}' absente du dataset !")


# ----------------------------------------------------------------------
# 3. VALEURS MANQUANTES
# ----------------------------------------------------------------------
def handle_missing_values(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
    logger.info("=== VALEURS MANQUANTES ===")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if missing.empty:
        logger.info("Aucune valeur manquante détectée.")
        return df

    logger.info(f"Colonnes concernées :\n{missing.to_string()}")

    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL, errors="ignore")

    for col in missing.index:
        if col in num_cols:
            if strategy == "median":
                fill_value = df[col].median()
            else:
                fill_value = df[col].mean()
            df[col] = df[col].fillna(fill_value)
            logger.info(f"  '{col}' : imputée par la {strategy} ({fill_value:.3f})")
        else:
            df = df.dropna(subset=[col])
            logger.info(f"  '{col}' : lignes supprimées (colonne non numérique)")

    return df


# ----------------------------------------------------------------------
# 4. DOUBLONS
# ----------------------------------------------------------------------
def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("=== DOUBLONS ===")
    n_dup = df.duplicated().sum()
    if n_dup == 0:
        logger.info("Aucun doublon détecté.")
        return df

    logger.info(f"{n_dup:,} doublons trouvés -> suppression")
    df = df.drop_duplicates().reset_index(drop=True)
    logger.info(f"Nouvelles dimensions : {df.shape}")
    return df


# ----------------------------------------------------------------------
# 5. OUTLIERS (IQR + Z-SCORE)
# ----------------------------------------------------------------------
def detect_outliers(df: pd.DataFrame, z_thresh: float = 4.0) -> pd.DataFrame:
    """
    Détecte les outliers avec deux méthodes complémentaires :
    - IQR (robuste, ne suppose pas de distribution normale)
    - Z-score (utile pour repérer les valeurs extrêmes ponctuelles)

    Ne supprime PAS automatiquement les lignes : un outlier médical peut être
    un vrai cas clinique rare (ex : tumeur particulièrement grosse), pas une
    erreur de saisie. On les *signale* pour décision éclairée.
    """
    logger.info("=== DÉTECTION DES OUTLIERS ===")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL, errors="ignore")

    report = []
    for col in num_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_iqr = ((df[col] < lower) | (df[col] > upper)).sum()

        z_scores = np.abs(stats.zscore(df[col]))
        n_z = (z_scores > z_thresh).sum()

        if n_iqr > 0 or n_z > 0:
            report.append((col, n_iqr, round(n_iqr / len(df) * 100, 2), n_z))

    if report:
        report_df = pd.DataFrame(
            report, columns=["colonne", "outliers_IQR", "%_IQR", "outliers_Zscore(>4)"]
        ).sort_values("outliers_IQR", ascending=False)
        logger.info(f"Résumé des outliers :\n{report_df.to_string(index=False)}")
    else:
        logger.info("Aucun outlier significatif détecté.")

    return df  # dataset inchangé, décision de suppression laissée au data scientist


# ----------------------------------------------------------------------
# 6. CORRÉLATION ENTRE FEATURES (redondance)
# ----------------------------------------------------------------------
def check_correlation(df: pd.DataFrame, threshold: float = 0.95) -> None:
    logger.info("=== CORRÉLATIONS FORTES ENTRE FEATURES (redondance) ===")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL, errors="ignore")
    corr_matrix = df[num_cols].corr().abs()

    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    pairs = [
        (col, row, upper.loc[row, col])
        for col in upper.columns
        for row in upper.index
        if pd.notna(upper.loc[row, col]) and upper.loc[row, col] > threshold
    ]

    if pairs:
        for col, row, val in sorted(pairs, key=lambda x: -x[2]):
            logger.info(f"  {row}  <->  {col} : corrélation = {val:.3f}")
        logger.info(
            "-> Ces paires sont redondantes : envisager d'en retirer une par paire avant l'entraînement."
        )
    else:
        logger.info(f"Aucune paire de features corrélée > {threshold}.")


# ----------------------------------------------------------------------
# 7. ÉQUILIBRE DES CLASSES
# ----------------------------------------------------------------------
def check_class_balance(df: pd.DataFrame) -> None:
    logger.info("=== ÉQUILIBRE DES CLASSES (diagnosis) ===")
    if TARGET_COL not in df.columns:
        return
    counts = df[TARGET_COL].value_counts()
    pct = df[TARGET_COL].value_counts(normalize=True) * 100
    summary = pd.DataFrame({"count": counts, "%": pct.round(2)})
    logger.info(f"\n{summary.to_string()}")

    ratio = counts.max() / counts.min()
    if ratio > 1.5:
        logger.info(
            f"Déséquilibre modéré détecté (ratio {ratio:.2f}). "
            "Pense à utiliser class_weight='balanced' ou du sur/sous-échantillonnage lors de l'entraînement."
        )


# ----------------------------------------------------------------------
# 8. OPTIMISATION MÉMOIRE
# ----------------------------------------------------------------------
def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """Downcast les float64/int64 vers des types plus légers sans perte utile de précision."""
    logger.info("=== OPTIMISATION MÉMOIRE ===")
    before = df.memory_usage(deep=True).sum() / 1024**2

    for col in df.select_dtypes(include=["float64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="float")
    for col in df.select_dtypes(include=["int64"]).columns:
        df[col] = pd.to_numeric(df[col], downcast="integer")

    after = df.memory_usage(deep=True).sum() / 1024**2
    logger.info(f"Mémoire avant : {before:.2f} Mo -> après : {after:.2f} Mo (-{(1 - after/before)*100:.1f}%)")
    return df


# ----------------------------------------------------------------------
# PIPELINE PRINCIPAL
# ----------------------------------------------------------------------
def run_pipeline(input_path: str, output_path: str) -> pd.DataFrame:
    df = load_data(input_path)
    initial_audit(df)
    df = handle_missing_values(df)
    df = handle_duplicates(df)
    detect_outliers(df)
    check_correlation(df)
    check_class_balance(df)
    df = optimize_memory(df)

    df.to_csv(output_path, index=False)
    logger.info(f"=== TERMINÉ === Fichier nettoyé exporté : {output_path}")
    logger.info("Rapport détaillé disponible dans : cleaning_report.log")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nettoyage du dataset BreastDiagAI")
    parser.add_argument(
        "--input", "-i",
        default="breast_cancer_40_features_1M.csv",
        help="Chemin vers le CSV brut (par défaut : dans le dossier courant)",
    )
    parser.add_argument(
        "--output", "-o",
        default="breast_cancer_cleaned.csv",
        help="Chemin de sortie du CSV nettoyé",
    )
    args = parser.parse_args()

    run_pipeline(args.input, args.output)

