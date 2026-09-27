"""
exploratory_analysis.py
========================
Analyse exploratoire (EDA) — Projet BreastDiagAI (Groupe IASD29)

Ce script explore le dataset nettoyé en profondeur, au-delà du simple
nettoyage, pour mieux comprendre les différences entre les tumeurs
bénignes et malignes avant l'entraînement du modèle.

Usage :
    python exploratory_analysis.py --input breast_cancer_cleaned.csv
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("BreastDiagAI-EDA")

TARGET_COL = "diagnosis"
OUTPUT_DIR = Path("results/eda")


def load_data(path: str) -> pd.DataFrame:
    """Charge le dataset nettoyé, en vérifiant que le fichier existe."""
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"Fichier introuvable : {file_path.resolve()}")
        logger.error("-> Régénère-le avec src/clean_data.py avant de lancer ce script.")
        sys.exit(1)
    df = pd.read_csv(file_path)
    logger.info(f"Dataset chargé : {df.shape[0]:,} lignes x {df.shape[1]} colonnes")
    return df


def compute_group_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule les statistiques descriptives (moyenne, écart-type, min, max)
    séparément pour les tumeurs bénignes (0) et malignes (1).

    Args:
        df: le dataset nettoyé complet.

    Returns:
        Un DataFrame résumé, aussi sauvegardé en CSV dans results/eda/.
    """
    logger.info("Calcul des statistiques par groupe (bénin vs malin)...")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL)

    stats = df.groupby(TARGET_COL)[num_cols].agg(["mean", "std", "min", "max"]).T
    stats.columns = ["Bénin (0)", "Malin (1)"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stats.to_csv(OUTPUT_DIR / "stats_by_group.csv")
    logger.info(f"Statistiques sauvegardées : {OUTPUT_DIR / 'stats_by_group.csv'}")
    return stats


def _grid_size(n_items: int, n_cols: int = 5) -> tuple:
    """Calcule le nombre de lignes nécessaires pour une grille de n_items,
    étant donné un nombre de colonnes fixe."""
    n_rows = (n_items + n_cols - 1) // n_cols
    return n_rows, n_cols


def plot_histograms(df: pd.DataFrame, n_features: int = None) -> None:
    """
    Dessine des histogrammes de distribution pour toutes les features
    (ou un sous-ensemble), séparés par diagnostic (bénin/malin).

    Args:
        df: le dataset nettoyé complet.
        n_features: nombre de features à afficher. None = toutes les features.
    """
    logger.info("Génération des histogrammes de distribution...")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL)
    if n_features is not None:
        num_cols = num_cols[:n_features]

    n_rows, n_cols = _grid_size(len(num_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4.5, n_rows * 3.5))
    axes = axes.flatten()

    for i, col in enumerate(num_cols):
        sns.histplot(data=df, x=col, hue=TARGET_COL, kde=True, ax=axes[i], palette=["#2ecc71", "#e74c3c"])
        axes[i].set_title(col, fontsize=9)

    # Cacher les axes vides restants (si le nombre de features n'est pas un multiple de n_cols)
    for j in range(len(num_cols), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "histograms.png", dpi=100)
    plt.close()
    logger.info(f"Histogrammes sauvegardés ({len(num_cols)} features) : {OUTPUT_DIR / 'histograms.png'}")


def plot_boxplots(df: pd.DataFrame, n_features: int = None) -> None:
    """
    Dessine des boxplots comparatifs bénin/malin pour visualiser si les
    features séparent bien les deux classes.

    Args:
        df: le dataset nettoyé complet.
        n_features: nombre de features à afficher. None = toutes les features.
    """
    logger.info("Génération des boxplots comparatifs...")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL)
    if n_features is not None:
        num_cols = num_cols[:n_features]

    n_rows, n_cols = _grid_size(len(num_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4.5, n_rows * 3.5))
    axes = axes.flatten()

    for i, col in enumerate(num_cols):
        sns.boxplot(data=df, x=TARGET_COL, y=col, hue=TARGET_COL, ax=axes[i],
                    palette=["#2ecc71", "#e74c3c"], legend=False)
        axes[i].set_title(col, fontsize=9)
        axes[i].set_xticks([0, 1])
        axes[i].set_xticklabels(["Bénin", "Malin"])

    for j in range(len(num_cols), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "boxplots.png", dpi=100)
    plt.close()
    logger.info(f"Boxplots sauvegardés ({len(num_cols)} features) : {OUTPUT_DIR / 'boxplots.png'}")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Dessine une heatmap de corrélation complète entre toutes les features
    numériques, pour repérer visuellement toutes les redondances possibles.

    Args:
        df: le dataset nettoyé complet.
    """
    logger.info("Génération de la heatmap de corrélation complète...")
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(TARGET_COL)
    corr = df[num_cols].corr()

    plt.figure(figsize=(20, 16))
    sns.heatmap(corr, cmap="coolwarm", center=0, square=True, linewidths=0.3)
    plt.title("Heatmap de corrélation — 40 features")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=120)
    plt.close()
    logger.info(f"Heatmap sauvegardée : {OUTPUT_DIR / 'correlation_heatmap.png'}")


def main(input_path: str) -> None:
    """Exécute le pipeline complet d'analyse exploratoire sur toutes les features."""
    df = load_data(input_path)
    compute_group_statistics(df)
    plot_histograms(df, n_features=None)   # None = toutes les 40 features
    plot_boxplots(df, n_features=None)     # None = toutes les 40 features
    plot_correlation_heatmap(df)
    logger.info("=== EDA TERMINÉE === Tous les résultats sont dans results/eda/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse exploratoire BreastDiagAI")
    parser.add_argument("--input", "-i", default="breast_cancer_cleaned.csv")
    args = parser.parse_args()
    main(args.input)