"""
statistical_tests.py
====================
Module de validation statistique formelle — Projet BreastDiagAI (Groupe IASD29).

Fournit des fonctions réutilisables basées sur SciPy pour valider formellement
les observations de l'analyse exploratoire (EDA) :
    1. shapiro_wilk      : test de normalité sur les variables numériques
    2. mann_whitney_u    : comparaison non paramétrique bénin vs malin
    3. anova_kruskal     : ANOVA paramétrique (si normalité & homogénéité) sinon Kruskal-Wallis
    4. chi2_independence : test du Chi-deux d'indépendance sur les variables catégorielles

Toutes les fonctions retournent un DataFrame pandas propre contenant au minimum :
la statistique du test, la p-value et la décision au seuil alpha = 0.05.
"""

from __future__ import annotations

import logging
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger("BreastDiagAI-Stats")

DEFAULT_ALPHA = 0.05
DEFAULT_TARGET_COL = "diagnosis"


def _resolve_numeric_columns(
    df: pd.DataFrame,
    cols: Iterable[str] | None,
    exclude_cols: Sequence[str] = (),
) -> list[str]:
    """Retourne la liste ordonnée des colonnes numériques à tester."""
    if cols is not None:
        resolved = [c for c in cols if c in df.columns and c not in exclude_cols]
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise ValueError(f"Colonnes introuvables dans le DataFrame : {missing}")
        return resolved

    num_cols = df.select_dtypes(include=[np.number]).columns
    return [c for c in num_cols if c not in exclude_cols]


def _resolve_categorical_columns(
    df: pd.DataFrame,
    cat_cols: Iterable[str] | None,
    exclude_cols: Sequence[str] = (),
) -> list[str]:
    """Retourne la liste ordonnée des colonnes catégorielles à tester."""
    if cat_cols is not None:
        resolved = [c for c in cat_cols if c in df.columns and c not in exclude_cols]
        missing = [c for c in cat_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Colonnes catégorielles introuvables : {missing}")
        return resolved

    detected = df.select_dtypes(include=["object", "category", "bool", "string"]).columns
    return [c for c in detected if c not in exclude_cols]


def shapiro_wilk(
    df: pd.DataFrame,
    cols: Iterable[str] | None = None,
    target_col: str = DEFAULT_TARGET_COL,
    alpha: float = DEFAULT_ALPHA,
    sample_size: int | None = 5000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Exécute le test de normalité de Shapiro-Wilk sur les variables numériques.

    Note méthodologique :
        L'algorithme de Shapiro-Wilk implémenté dans `scipy.stats.shapiro` est
        calibré pour N <= 5 000 observations (au-delà, SciPy émet un avertissement
        car l'approximation de la p-value devient imprécise). Par défaut, un
        échantillon aléatoire reproductible de 5 000 observations est utilisé
        lorsque la variable dépasse ce seuil.

    Args:
        df: DataFrame d'entrée.
        cols: Liste des colonnes numériques à tester. Si None, sélectionne toutes
            les colonnes numériques hors `target_col`.
        target_col: Nom de la colonne cible à exclure par défaut.
        alpha: Seuil de significativité (défaut : 0.05).
        sample_size: Taille maximale d'échantillon pour Shapiro-Wilk (défaut : 5000).
            Passer None pour tester l'ensemble des valeurs (non recommandé si N > 5000).
        random_state: Graine aléatoire pour le sous-échantillonnage reproductible.

    Returns:
        DataFrame avec les colonnes :
        ['feature', 'n_total', 'n_tested', 'statistic', 'p_value', 'is_normal', 'decision'].
    """
    numeric_cols = _resolve_numeric_columns(df, cols, exclude_cols=(target_col,))
    rng = np.random.default_rng(random_state)
    records = []

    for col in numeric_cols:
        series = df[col].dropna()
        n_total = len(series)
        if n_total < 3:
            logger.warning("Colonne '%s' ignorée (< 3 observations valides).", col)
            continue

        if sample_size is not None and n_total > sample_size:
            idx = rng.choice(n_total, size=sample_size, replace=False)
            tested_values = series.iloc[idx].to_numpy()
        else:
            tested_values = series.to_numpy()

        stat, p_val = stats.shapiro(tested_values)
        is_normal = bool(p_val >= alpha)
        decision = (
            f"Normale (ne rejette pas H0 au seuil {alpha})"
            if is_normal
            else f"Non normale (rejette H0 au seuil {alpha})"
        )

        records.append(
            {
                "feature": col,
                "n_total": int(n_total),
                "n_tested": int(len(tested_values)),
                "statistic": float(stat),
                "p_value": float(p_val),
                "is_normal": is_normal,
                "decision": decision,
            }
        )

    columns = [
        "feature",
        "n_total",
        "n_tested",
        "statistic",
        "p_value",
        "is_normal",
        "decision",
    ]
    return pd.DataFrame(records, columns=columns)


def mann_whitney_u(
    df: pd.DataFrame,
    cols: Iterable[str] | None = None,
    target_col: str = DEFAULT_TARGET_COL,
    group_a: int | str = 0,
    group_b: int | str = 1,
    alpha: float = DEFAULT_ALPHA,
    alternative: str = "two-sided",
) -> pd.DataFrame:
    """
    Compare les distributions (médianes/rangs) entre deux groupes (ex. bénin vs malin)
    via le test non paramétrique U de Mann-Whitney.

    Args:
        df: DataFrame d'entrée contenant les variables et la cible.
        cols: Colonnes numériques à tester. Si None, toutes les colonnes numériques
            hors `target_col` sont analysées.
        target_col: Nom de la colonne définissant les deux groupes (défaut : 'diagnosis').
        group_a: Valeur du premier groupe (défaut : 0, Bénin).
        group_b: Valeur du second groupe (défaut : 1, Malin).
        alpha: Seuil de significativité (défaut : 0.05).
        alternative: Hypothèse alternative ('two-sided', 'less', 'greater').

    Returns:
        DataFrame trié par p-value croissante puis |taille d'effet| décroissante avec :
        ['feature', 'median_group_0', 'median_group_1', 'rank_biserial_r',
         'statistic', 'p_value', 'significant', 'decision'].
    """
    if target_col not in df.columns:
        raise ValueError(f"Colonne cible '{target_col}' absente du DataFrame.")

    numeric_cols = _resolve_numeric_columns(df, cols, exclude_cols=(target_col,))
    mask_a = df[target_col] == group_a
    mask_b = df[target_col] == group_b

    records = []
    for col in numeric_cols:
        vals_a = df.loc[mask_a, col].dropna().to_numpy()
        vals_b = df.loc[mask_b, col].dropna().to_numpy()

        if len(vals_a) == 0 or len(vals_b) == 0:
            logger.warning("Colonne '%s' ignorée (un des groupes est vide).", col)
            continue

        stat, p_val = stats.mannwhitneyu(vals_a, vals_b, alternative=alternative)
        # Corrélation rang-bisériale : mesure d'effet bornée dans [-1, 1]
        n1, n2 = len(vals_a), len(vals_b)
        rank_biserial = 1.0 - (2.0 * stat) / (n1 * n2)

        significant = bool(p_val < alpha)
        decision = (
            f"Différence significative (rejette H0 au seuil {alpha})"
            if significant
            else f"Pas de différence significative (ne rejette pas H0 au seuil {alpha})"
        )

        records.append(
            {
                "feature": col,
                f"median_group_{group_a}": float(np.median(vals_a)),
                f"median_group_{group_b}": float(np.median(vals_b)),
                "rank_biserial_r": float(rank_biserial),
                "statistic": float(stat),
                "p_value": float(p_val),
                "significant": significant,
                "decision": decision,
            }
        )

    columns = [
        "feature",
        f"median_group_{group_a}",
        f"median_group_{group_b}",
        "rank_biserial_r",
        "statistic",
        "p_value",
        "significant",
        "decision",
    ]
    result = pd.DataFrame(records, columns=columns)
    if not result.empty:
        result = result.assign(_abs_r=result["rank_biserial_r"].abs()).sort_values(
            by=["p_value", "_abs_r"], ascending=[True, False]
        ).drop(columns=["_abs_r"]).reset_index(drop=True)
    return result


def anova_kruskal(
    df: pd.DataFrame,
    cols: Iterable[str] | None = None,
    group_col: str = DEFAULT_TARGET_COL,
    alpha: float = DEFAULT_ALPHA,
    sample_size_normality: int | None = 5000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Effectue une comparaison inter-groupes adaptative pour chaque variable numérique :
        - Vérifie la normalité de chaque groupe (Shapiro-Wilk) et l'homogénéité des
          variances (test de Levene).
        - Si normalité ET homogénéité sont satisfaites (p >= alpha) : applique l'ANOVA
          à un facteur (`scipy.stats.f_oneway`).
        - Sinon : applique le test non paramétrique de Kruskal-Wallis (`scipy.stats.kruskal`).

    Args:
        df: DataFrame d'entrée.
        cols: Colonnes numériques à tester. Si None, toutes les colonnes numériques
            hors `group_col` sont testées.
        group_col: Colonne catégorielle ou discrète définissant les groupes (2 groupes ou plus).
        alpha: Seuil de significativité (défaut : 0.05).
        sample_size_normality: Taille max par groupe pour le test de Shapiro-Wilk.
        random_state: Graine aléatoire pour le sous-échantillonnage de normalité.

    Returns:
        DataFrame avec les colonnes :
        ['feature', 'n_groups', 'normality_ok', 'homogeneity_ok', 'levene_p_value',
         'test_used', 'statistic', 'p_value', 'significant', 'decision'].
    """
    if group_col not in df.columns:
        raise ValueError(f"Colonne de regroupement '{group_col}' absente du DataFrame.")

    numeric_cols = _resolve_numeric_columns(df, cols, exclude_cols=(group_col,))
    rng = np.random.default_rng(random_state)
    group_labels = [g for g in df[group_col].dropna().unique()]
    group_masks = [df[group_col] == g for g in group_labels]

    records = []
    for col in numeric_cols:
        groups = [df.loc[m, col].dropna().to_numpy() for m in group_masks]
        groups = [g for g in groups if len(g) >= 3]
        if len(groups) < 2:
            logger.warning("Colonne '%s' ignorée (< 2 groupes valides).", col)
            continue

        # 1. Normalité dans chaque groupe
        normality_flags = []
        for g in groups:
            if sample_size_normality is not None and len(g) > sample_size_normality:
                idx = rng.choice(len(g), size=sample_size_normality, replace=False)
                g_sample = g[idx]
            else:
                g_sample = g
            _, p_norm = stats.shapiro(g_sample)
            normality_flags.append(p_norm >= alpha)
        normality_ok = all(normality_flags)

        # 2. Homogénéité des variances (test de Levene)
        _, levene_p = stats.levene(*groups)
        homogeneity_ok = bool(levene_p >= alpha)

        # 3. Choix du test : ANOVA si hypothèses vérifiées, sinon Kruskal-Wallis
        if normality_ok and homogeneity_ok:
            stat, p_val = stats.f_oneway(*groups)
            test_used = "ANOVA (F)"
        else:
            stat, p_val = stats.kruskal(*groups)
            test_used = "Kruskal-Wallis (H)"

        significant = bool(p_val < alpha)
        decision = (
            f"Différence inter-groupes significative (rejette H0 au seuil {alpha})"
            if significant
            else f"Pas de différence inter-groupes (ne rejette pas H0 au seuil {alpha})"
        )

        records.append(
            {
                "feature": col,
                "n_groups": int(len(groups)),
                "normality_ok": bool(normality_ok),
                "homogeneity_ok": homogeneity_ok,
                "levene_p_value": float(levene_p),
                "test_used": test_used,
                "statistic": float(stat),
                "p_value": float(p_val),
                "significant": significant,
                "decision": decision,
            }
        )

    columns = [
        "feature",
        "n_groups",
        "normality_ok",
        "homogeneity_ok",
        "levene_p_value",
        "test_used",
        "statistic",
        "p_value",
        "significant",
        "decision",
    ]
    result = pd.DataFrame(records, columns=columns)
    if not result.empty:
        result = result.sort_values(by=["p_value", "statistic"], ascending=[True, False]).reset_index(drop=True)
    return result


def chi2_independence(
    df: pd.DataFrame,
    cat_cols: Iterable[str] | None = None,
    target_col: str = DEFAULT_TARGET_COL,
    alpha: float = DEFAULT_ALPHA,
) -> pd.DataFrame:
    """
    Exécute le test du Chi-deux d'indépendance entre des variables catégorielles
    et la variable cible.

    Args:
        df: DataFrame d'entrée.
        cat_cols: Colonnes catégorielles à tester. Si None, détecte automatiquement
            les colonnes de type object, category, bool ou string (hors `target_col`).
        target_col: Variable cible (défaut : 'diagnosis').
        alpha: Seuil de significativité (défaut : 0.05).

    Returns:
        DataFrame avec les colonnes :
        ['feature', 'n_categories', 'dof', 'min_expected_freq', 'cramers_v',
         'statistic', 'p_value', 'significant', 'decision'].
        Retourne un DataFrame vide avec ces colonnes si aucune variable catégorielle
        n'est présente.
    """
    if target_col not in df.columns:
        raise ValueError(f"Colonne cible '{target_col}' absente du DataFrame.")

    resolved_cols = _resolve_categorical_columns(df, cat_cols, exclude_cols=(target_col,))
    columns = [
        "feature",
        "n_categories",
        "dof",
        "min_expected_freq",
        "cramers_v",
        "statistic",
        "p_value",
        "significant",
        "decision",
    ]

    if not resolved_cols:
        logger.info("Aucune variable catégorielle détectée pour le test du Chi-deux.")
        return pd.DataFrame(columns=columns)

    records = []
    for col in resolved_cols:
        sub = df[[col, target_col]].dropna()
        if sub.empty:
            continue

        contingency = pd.crosstab(sub[col], sub[target_col])
        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            logger.warning("Colonne '%s' ignorée (tableau de contingence < 2x2).", col)
            continue

        chi2, p_val, dof, expected = stats.chi2_contingency(contingency)
        n_obs = contingency.to_numpy().sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = float(np.sqrt(chi2 / (n_obs * min_dim))) if n_obs > 0 and min_dim > 0 else 0.0

        significant = bool(p_val < alpha)
        decision = (
            f"Dépendance significative (rejette H0 au seuil {alpha})"
            if significant
            else f"Indépendance (ne rejette pas H0 au seuil {alpha})"
        )

        records.append(
            {
                "feature": col,
                "n_categories": int(contingency.shape[0]),
                "dof": int(dof),
                "min_expected_freq": float(expected.min()),
                "cramers_v": cramers_v,
                "statistic": float(chi2),
                "p_value": float(p_val),
                "significant": significant,
                "decision": decision,
            }
        )

    result = pd.DataFrame(records, columns=columns)
    if not result.empty:
        result = result.sort_values(by=["p_value", "cramers_v"], ascending=[True, False]).reset_index(drop=True)
    return result
