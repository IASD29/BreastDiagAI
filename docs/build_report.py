"""
build_report.py — Génère docs/Rapport_Projet.pdf (BreastDiagAI, Groupe IASD29).

Tous les chiffres proviennent des fichiers existants du projet :
  - cleaning_report.log, pre/preprocessing.log, RAPPORT_EDA_v2.md
  - notebooks/02_statistical_eda_validation.ipynb (sorties enregistrées)
  - results/eda/*.png (figures existantes du dépôt)
Aucun modèle n'a été entraîné : benchmark, SHAP et Streamlit sont marqués
« résultats non disponibles ».

Usage : python build_report.py   (depuis le dossier docs/)
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = Path(__file__).resolve().parent
FIG = HERE.parent / "results" / "eda"   # figures déjà versionnées dans le dépôt
OUT = HERE / "Rapport_Projet.pdf"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
pdfmetrics.registerFont(TTFont("DV", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-I", str(FONT_DIR / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DVM", str(FONT_DIR / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")

PINK = colors.HexColor("#c2185b")
DARK = colors.HexColor("#263238")
GREY = colors.HexColor("#eceff1")
NA_BG = colors.HexColor("#fff3e0")

ss = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=ss["Normal"], fontName="DV", fontSize=10, leading=14.5,
                      alignment=TA_JUSTIFY, spaceAfter=6)
BUL = ParagraphStyle("bul", parent=BODY, leftIndent=14, bulletIndent=4, spaceAfter=3)
H1 = ParagraphStyle("h1", parent=BODY, fontName="DV-B", fontSize=17, leading=21, textColor=PINK,
                    spaceBefore=4, spaceAfter=10, alignment=0)
H2 = ParagraphStyle("h2", parent=BODY, fontName="DV-B", fontSize=12.5, leading=16, textColor=DARK,
                    spaceBefore=10, spaceAfter=5, alignment=0)
CAP = ParagraphStyle("cap", parent=BODY, fontName="DV-I", fontSize=8.8, leading=11.5,
                     alignment=TA_CENTER, textColor=colors.HexColor("#455a64"), spaceAfter=10)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8.3, leading=10.5, alignment=0, spaceAfter=0)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="DV-B", textColor=colors.white)
NOTE = ParagraphStyle("note", parent=BODY, fontSize=9, leading=12.5, backColor=NA_BG,
                      borderColor=colors.HexColor("#ef6c00"), borderWidth=0.8, borderPadding=7,
                      spaceBefore=6, spaceAfter=12)
CODE = ParagraphStyle("code", parent=BODY, fontName="DVM", fontSize=8, leading=10.5, alignment=0,
                      backColor=GREY, borderPadding=6, spaceBefore=4, spaceAfter=10)

NA = "Résultats non disponibles"


class Doc(SimpleDocTemplate):
    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("h1", "h2"):
            lvl = 0 if f.style.name == "h1" else 1
            self.notify("TOCEntry", (lvl, f.getPlainText(), self.page))


def p(t, s=BODY):
    return Paragraph(t, s)


def bullets(items):
    return [Paragraph(i, BUL, bulletText="•") for i in items]


def table(rows, widths, header=True, na_rows=False):
    data = [[Paragraph(str(c), CELLB if (header and r == 0) else CELL) for c in row]
            for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b0bec5")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GREY]),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), DARK))
    if na_rows:
        st.append(("BACKGROUND", (1, 1), (-1, -1), NA_BG))
    t.setStyle(TableStyle(st))
    return t


def fig(name, caption, width=16.5 * cm, max_h=11.5 * cm):
    from reportlab.lib.utils import ImageReader
    path = FIG / name
    iw, ih = ImageReader(str(path)).getSize()
    w = width
    h = w * ih / iw
    if h > max_h:
        h = max_h
        w = h * iw / ih
    return KeepTogether([Image(str(path), width=w, height=h), Spacer(1, 3), p(caption, CAP)])


def on_page(c, d):
    if d.page == 1:
        return
    c.saveState()
    c.setFont("DV", 8)
    c.setFillColor(colors.HexColor("#78909c"))
    c.drawString(2 * cm, 1.2 * cm, "BreastDiagAI — Rapport de projet — Groupe IASD29")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {d.page}")
    c.setStrokeColor(PINK)
    c.setLineWidth(0.6)
    c.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    c.restoreState()


def cover(c, d):
    W, H = A4
    c.saveState()
    c.setFillColor(PINK)
    c.rect(0, H - 9 * cm, W, 9 * cm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("DV-B", 34)
    c.drawCentredString(W / 2, H - 4.3 * cm, "BreastDiagAI")
    c.setFont("DV", 14)
    c.drawCentredString(W / 2, H - 5.6 * cm, "Aide au diagnostic du cancer du sein (bénin / malin)")
    c.drawCentredString(W / 2, H - 6.4 * cm, "par Data Mining et Machine Learning")
    c.setFillColor(DARK)
    c.setFont("DV-B", 18)
    c.drawCentredString(W / 2, H - 12 * cm, "Rapport scientifique de projet")
    c.setFont("DV", 11)
    y = H - 14 * cm
    for line in ["Groupe IASD29",
                 "Membres : IASD29 · IASD08 · IASD19 · IASD24 · RSD19",
                 "Dépôt : github.com/IASD29/BreastDiagAI",
                 "Jeu de données : Kaggle — Breast Cancer Dataset (500 000 observations, 40 variables)"]:
        c.drawCentredString(W / 2, y, line)
        y -= 0.8 * cm
    c.setFont("DV-I", 9)
    c.setFillColor(colors.HexColor("#546e7a"))
    c.drawCentredString(W / 2, 3.2 * cm, "Outil d'aide à la décision à but pédagogique — ne remplace en aucun cas un avis médical.")
    c.drawCentredString(W / 2, 2.6 * cm, "Version : novembre 2026")
    c.restoreState()


def build():
    story = [PageBreak()]  # page 1 = page de garde dessinée par cover()

    # --- Sommaire
    story.append(p("Sommaire", ParagraphStyle("h1toc", parent=H1)))
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("t0", fontName="DV-B", fontSize=10.5, leading=16, leftIndent=0),
                       ParagraphStyle("t1", fontName="DV", fontSize=9.5, leading=13, leftIndent=16)]
    story += [toc, Spacer(1, 12)]
    story.append(p("<b>Note sur les sources.</b> Tous les chiffres de ce rapport sont repris des sorties existantes du "
                   "projet : <font name='DVM'>cleaning_report.log</font>, <font name='DVM'>pre/preprocessing.log</font>, "
                   "<font name='DVM'>RAPPORT_EDA_v2.md</font>, <font name='DVM'>results/eda/stats_by_group.csv</font> et les "
                   "sorties enregistrées du notebook <font name='DVM'>02_statistical_eda_validation.ipynb</font>. "
                   "Aucun modèle n'a encore été entraîné dans le projet. Les sections Benchmark, SHAP et Streamlit "
                   "sont donc marquées « " + NA + " ».", NOTE))
    story.append(PageBreak())

    # --- 1. Contexte médical
    story.append(p("1. Contexte médical et objectifs", H1))
    story.append(p("Le cancer du sein est l'un des cancers les plus fréquents chez la femme. Le pronostic dépend "
                   "largement de la précocité du diagnostic. Quand on découvre une masse mammaire, le parcours "
                   "classique enchaîne imagerie (mammographie, échographie) et prélèvement (cytoponction ou biopsie). "
                   "Le pathologiste analyse ensuite au microscope la morphologie des cellules : taille et forme des "
                   "noyaux, régularité des contours, texture de la chromatine. Ce parcours est long et source "
                   "d'anxiété pour les patientes."))
    story.append(p("Les caractéristiques morphologiques mesurées sur les noyaux cellulaires (rayon, périmètre, aire, "
                   "concavité, symétrie, dimension fractale…) sont la base des jeux de données de type "
                   "<i>Wisconsin Diagnostic Breast Cancer</i>. Pour chaque caractéristique, on calcule la valeur moyenne "
                   "(<font name='DVM'>_mean</font>), l'erreur standard (<font name='DVM'>_se</font>) et la valeur la plus "
                   "extrême (<font name='DVM'>_worst</font>). Le jeu utilisé ici reprend ce format et l'étend avec "
                   "10 variables « biologiques » supplémentaires (<font name='DVM'>nucleus_size</font>, "
                   "<font name='DVM'>mitosis_rate</font>, <font name='DVM'>chromatin_density</font>, etc.)."))
    story.append(p("Origine du projet", H2))
    story.append(p("D'après le README du dépôt, le projet est né d'une expérience personnelle : la découverte d'une "
                   "anomalie mammaire chez la mère d'un membre de l'équipe, et le parcours médical qui a suivi. "
                   "BreastDiagAI ne cherche pas à remplacer le médecin. Le but est un <b>outil d'aide à la "
                   "décision</b> qui estime si une tumeur présente des caractéristiques bénignes ou malignes, et qui "
                   "<b>explique</b> pourquoi."))
    story.append(p("Objectifs", H2))
    story += bullets([
        "Prédire le diagnostic binaire <font name='DVM'>diagnosis</font> (0 = bénin, 1 = malin) à partir de 40 variables numériques.",
        "Construire un pipeline de données reproductible : nettoyage, analyse exploratoire, validation statistique, prétraitement.",
        "Privilégier le <b>rappel (Recall)</b> sur la classe maligne : en dépistage, un faux négatif (cancer manqué) coûte bien plus cher qu'un faux positif.",
        "Rendre la prédiction explicable (SHAP) et accessible via une application web (API FastAPI + interface).",
    ])
    story.append(p("Avertissement éthique", H2))
    story.append(p("Le jeu de données est d'origine Kaggle et présente des caractéristiques typiques d'un jeu "
                   "<b>synthétique</b> : beaucoup de variables sont centrées-réduites et indépendantes de la cible. "
                   "Les conclusions de ce rapport valent pour ce jeu et ne doivent pas être généralisées à la "
                   "pratique clinique (voir la décision 5 de <font name='DVM'>RAPPORT_EDA_v2.md</font>)."))
    story.append(PageBreak())

    # --- 2. Données et pipeline
    story.append(p("2. Données et pipeline global", H1))
    story.append(p("2.1 Le jeu de données", H2))
    story.append(table([
        ["Caractéristique", "Valeur", "Source"],
        ["Fichier brut", "breast_cancer_40_features_1M.csv (≈ 387 Mo)", "RAPPORT_NETTOYAGE.md"],
        ["Observations", "500 000", "cleaning_report.log"],
        ["Colonnes", "41 = 40 features + 1 cible", "cleaning_report.log"],
        ["Types", "40 × float64, 1 × int64 (diagnosis)", "cleaning_report.log"],
        ["Cible", "diagnosis : 0 = bénin, 1 = malin", "clean_data.py"],
        ["Répartition", "325 000 bénins (65 %) / 175 000 malins (35 %), ratio 1,86", "cleaning_report.log"],
        ["Source", "Kaggle — sharmajicoder/breast-cancer-dataset", "data/raw/README.md"],
    ], [3.6 * cm, 8.2 * cm, 4.7 * cm]))
    story.append(Spacer(1, 8))
    story.append(p("2.2 Les étapes du pipeline", H2))
    steps = [
        ["Étape", "Script / artefact", "Entrée → Sortie", "Statut"],
        ["1. Nettoyage & audit", "src/clean_data.py", "CSV brut → breast_cancer_cleaned.csv + cleaning_report.log", "Réalisé"],
        ["2. EDA descriptive", "src/exploratory_analysis.py", "CSV nettoyé → stats_by_group.csv, histogrammes, boxplots, heatmap", "Réalisé"],
        ["3. EDA approfondie & tests", "notebooks/02_statistical_eda_validation.ipynb + src/statistical_tests.py", "CSV nettoyé → 12 figures + 4 tests", "Réalisé"],
        ["4. Prétraitement", "src/preprocessing.py (pre/)", "CSV nettoyé → X/y train/test + preprocessor.joblib", "Réalisé"],
        ["5. Entraînement & benchmark", "notebooks/training.ipynb (prévu)", "X/y → modèle + métriques", NA],
        ["6. Explicabilité", "SHAP (prévu)", "Modèle → contributions par variable", NA],
        ["7. Application", "app/backend (FastAPI) + app/frontend (React)", "Saisie → prédiction + historique", "Réalisé (modèle simulé)"],
    ]
    story.append(table(steps, [3.5 * cm, 4.6 * cm, 5.6 * cm, 2.8 * cm]))
    story.append(Spacer(1, 8))
    story.append(p("En résumé : les données brutes sont auditées et nettoyées, puis explorées visuellement. Les "
                   "observations sont ensuite validées par des tests statistiques formels, puis les données sont "
                   "transformées pour l'apprentissage. Les étapes 5 et 6 n'ont pas encore de résultats dans le dépôt. "
                   "L'application web existe, mais son service de prédiction utilise pour l'instant une heuristique "
                   "de démonstration (section 8)."))
    story.append(PageBreak())

    # --- 3. Nettoyage
    story.append(p("3. Nettoyage et audit des données", H1))
    story.append(p("Le script <font name='DVM'>clean_data.py</font> enchaîne 8 étapes journalisées dans "
                   "<font name='DVM'>cleaning_report.log</font>. Résultats obtenus :"))
    story.append(table([
        ["Étape", "Résultat"],
        ["Valeurs manquantes", "Aucune valeur manquante détectée"],
        ["Doublons", "Aucun doublon détecté"],
        ["Outliers (IQR 1,5 et Z-score > 4)", "Présents sur les 40 variables ; maximum sur area_worst (8 894 valeurs, 1,78 % ; 852 au Z-score). Signalés mais <b>non supprimés</b> (cas cliniques rares possibles)."],
        ["Corrélations > 0,95", "radius_mean ↔ area_mean : 0,989 ; radius_mean ↔ radius_worst : 0,952"],
        ["Équilibre des classes", "65 % / 35 % — déséquilibre modéré (ratio 1,86) → class_weight='balanced' recommandé"],
        ["Optimisation mémoire", "156,40 Mo → 76,77 Mo (−50,9 %) par downcasting float64 → float32"],
    ], [4.6 * cm, 11.9 * cm]))
    story.append(p("Variables les plus touchées par les outliers (extrait du log)", H2))
    story.append(table([
        ["Variable", "Outliers IQR", "% IQR", "Outliers Z > 4"],
        ["area_worst", "8 894", "1,78", "852"],
        ["area_mean", "6 612", "1,32", "449"],
        ["perimeter_mean", "3 990", "0,80", "82"],
        ["concavity_se", "3 599", "0,72", "22"],
        ["smoothness_mean", "3 592", "0,72", "25"],
        ["… (35 autres variables)", "3 355 – 3 588", "0,67 – 0,72", "13 – 40"],
        ["mitosis_rate", "1 772", "0,35", "25"],
        ["tumor_border_irregularity", "1 701", "0,34", "17"],
    ], [6 * cm, 3.5 * cm, 3 * cm, 4 * cm]))
    story.append(Spacer(1, 6))
    story.append(p("Le notebook <font name='DVM'>notebooks/01_data_cleaning_audit.ipynb</font>, livré avec ce rapport, "
                   "rejoue cet audit (types, valeurs manquantes, doublons, plages de valeurs, outliers, mémoire) de "
                   "façon interactive."))
    story.append(p("<b>Point de vigilance.</b> Le notebook 02 signale que sa copie locale de "
                   "<font name='DVM'>breast_cancer_cleaned.csv</font> était corrompue à partir de l'octet 20 971 521. Il n'a "
                   "donc utilisé que les <b>49 056</b> premières lignes valides. Les tests statistiques de la section 5 "
                   "portent sur ce sous-ensemble, et non sur les 500 000 lignes.", NOTE))
    story.append(PageBreak())

    # --- 4. EDA
    story.append(p("4. Analyse exploratoire (EDA) — 10 figures", H1))
    story.append(p("L'analyse exploratoire a été menée en deux temps. D'abord <font name='DVM'>exploratory_analysis.py</font> "
                   "(statistiques par groupe sur les 40 variables), puis le notebook 02 (figures 1 à 10 ci-dessous, "
                   "sur un échantillon stratifié de 10 000 lignes pour les graphiques les plus lourds). Le tableau "
                   "suivant reprend le classement de <font name='DVM'>RAPPORT_EDA_v2.md</font> :"))
    story.append(table([
        ["Rang", "Variable", "Moyenne bénin", "Moyenne malin", "Ratio M/B"],
        ["1", "area_worst", "617,70", "1 244,93", "× 2,02"],
        ["2", "area_mean", "498,22", "914,51", "× 1,84"],
        ["3", "perimeter_mean", "74,40", "101,75", "× 1,37"],
        ["4", "radius_mean", "12,40", "16,96", "× 1,37"],
        ["5", "radius_worst", "14,42", "18,98", "× 1,32"],
    ], [1.5 * cm, 4.5 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm]))
    story.append(Spacer(1, 4))
    story.append(p("Les 35 autres variables ont un écart de moyenne quasi nul entre bénins et malins."))

    figs = [
        ("01_distribution_cible.png", "Figure 1 — Répartition de la variable cible : 65 % bénin / 35 % malin (ratio 1,86). "
         "Ce déséquilibre modéré justifie la stratification du découpage train/test.", 11 * cm),
        ("02_distributions_variables_cles.png", "Figure 2 — Histogrammes + KDE des 5 variables géométriques discriminantes et de 3 variables "
         "biologiques. Seules les variables de taille montrent deux distributions décalées.", 11 * cm),
        ("03_distributions_variables_non_discriminantes.png", "Figure 3 — Variables standardisées à faible pouvoir discriminant : "
         "les courbes bénin (vert) et malin (rouge) se superposent.", 11 * cm),
        ("04_correlation_pearson.png", "Figure 4 — Matrice de corrélation de Pearson (40 variables) : un seul bloc fortement "
         "corrélé, formé des variables géométriques.", 12.5 * cm),
        ("05_correlation_spearman.png", "Figure 5 — Matrice de corrélation de Spearman : même structure. radius_mean et area_mean ont "
         "ρ = 1,000 (relation monotone A ∝ r²).", 12.5 * cm),
        ("06_correlation_cible_pearson_vs_spearman.png", "Figure 6 — Top 15 des corrélations avec diagnosis. area_worst "
         "(r = 0,799 ; ρ = 0,826), area_mean (0,745 ; 0,764), radius_mean (0,726 ; 0,764), radius_worst (0,693 ; 0,724), "
         "perimeter_mean (0,674 ; 0,697). Toutes les autres sont |r| ≤ 0,011.", 11 * cm),
        ("07_boxplots_par_diagnostic.png", "Figure 7 — Boxplots par diagnostic. Séparation nette des quartiles pour les 5 variables "
         "géométriques ; médianes identiques pour mitosis_rate, cell_density, nucleus_size, etc.", 11 * cm),
        ("08_pairplot_top5_discriminantes.png", "Figure 8 — Pairplot des 5 variables les plus discriminantes : frontière bivariée "
         "visible et forte colinéarité radius_mean ↔ area_mean.", 13 * cm),
        ("09_violin_plots.png", "Figure 9 — Violin plots : forme complète des densités (asymétrie à droite des variables d'aire).", 11 * cm),
        ("10_qq_plots_normalite.png", "Figure 10 — QQ-plots : 4 variables non normales (area_worst, area_mean, perimeter_mean, "
         "mitosis_rate) contre 4 variables proches de la loi normale.", 11 * cm),
    ]
    story.append(Spacer(1, 6))
    for i, (n, c, h) in enumerate(figs):
        story.append(fig(n, c, max_h=h))
    story.append(p("Synthèse de l'EDA", H2))
    story += bullets([
        "La <b>taille de la tumeur</b> (aire, rayon, périmètre ; moyenne et valeur extrême) porte l'essentiel du signal.",
        "Les variables au nom « biologique » prometteur (mitosis_rate, chromatin_density, nucleus_size) n'ont aucun pouvoir discriminant individuel dans ce jeu.",
        "Redondance forte entre radius_mean, area_mean et perimeter_mean. Elle gêne les modèles linéaires, beaucoup moins les arbres.",
        "Décision de l'équipe : <b>conserver les 40 variables</b>, car un modèle non linéaire peut exploiter des interactions invisibles en univarié.",
    ])
    story.append(PageBreak())

    # --- 5. Tests statistiques
    story.append(p("5. Validation statistique formelle — 4 tests", H1))
    story.append(p("Le module <font name='DVM'>src/statistical_tests.py</font> fournit quatre fonctions SciPy réutilisables. "
                   "Chacune renvoie la statistique, la p-value et la décision au seuil α = 0,05. Les résultats ci-dessous "
                   "sont les sorties enregistrées du notebook 02 (n = 49 056 lignes)."))

    story.append(p("5.1 Test 1 — Shapiro-Wilk (normalité)", H2))
    story.append(p("H0 : la variable suit une loi normale. Le test est appliqué sur un sous-échantillon de 5 000 valeurs par "
                   "variable (limite de validité du test). <b>Résultat : 34 variables normales, 6 non normales.</b>"))
    story.append(table([
        ["Variable non normale", "W", "p-value"],
        ["area_worst", "0,9633", "7,68 × 10⁻³⁴"],
        ["area_mean", "0,9809", "2,09 × 10⁻²⁵"],
        ["mitosis_rate", "0,9927", "2,40 × 10⁻¹⁵"],
        ["tumor_border_irregularity", "0,9981", "7,25 × 10⁻⁶"],
        ["perimeter_mean", "0,9983", "2,55 × 10⁻⁵"],
        ["compactness_worst", "0,9992", "0,0296"],
    ], [7 * cm, 4 * cm, 5.5 * cm]))
    story.append(p("Interprétation : les variables d'aire sont asymétriques. Cette non-normalité, ajoutée aux outliers, "
                   "justifie à la fois les tests non paramétriques et le choix de RobustScaler (section 6)."))

    story.append(p("5.2 Test 2 — U de Mann-Whitney (bénin vs malin)", H2))
    story.append(p("H0 : les deux groupes ont la même distribution. La taille d'effet est mesurée par la corrélation "
                   "rang-bisériale r (0 = aucun effet, 1 = séparation totale). <b>6 variables significatives sur 40.</b>"))
    story.append(table([
        ["Variable", "Médiane bénin", "Médiane malin", "r", "p-value", "Décision"],
        ["area_worst", "633,97", "1 172,36", "0,99998", "≈ 0", "Significatif"],
        ["radius_mean", "12,62", "16,75", "0,9248", "≈ 0", "Significatif"],
        ["area_mean", "499,99", "881,42", "0,9248", "≈ 0", "Significatif"],
        ["radius_worst", "14,58", "18,82", "0,8764", "≈ 0", "Significatif"],
        ["perimeter_mean", "74,92", "100,58", "0,8432", "≈ 0", "Significatif"],
        ["nucleus_size", "9,953", "10,027", "0,0137", "0,0124", "Significatif (effet négligeable)"],
        ["tumor_border_irregularity", "0,4995", "0,4953", "−0,0099", "0,0715", "Non significatif"],
        ["compactness_worst", "−0,0103", "0,0048", "0,0095", "0,0820", "Non significatif"],
        ["mitosis_rate*", "4,001", "3,991", "−0,0025", "0,6440", "Non significatif"],
    ], [4.1 * cm, 2.3 * cm, 2.3 * cm, 1.8 * cm, 1.8 * cm, 4.2 * cm]))
    story.append(p("* mitosis_rate : valeur issue du test restreint aux 6 variables non normales.", CAP))
    story.append(fig("11_synthese_tests_pvalues_effets.png", "Figure 11 — Synthèse des tests : taille d'effet |r| (gauche) et "
                     "−log10(p) plafonné à 300 (droite) pour les 15 premières variables. Rouge = p < 0,05.", max_h=8 * cm))

    story.append(p("5.3 Test 3 — ANOVA / Kruskal-Wallis (sélection adaptative)", H2))
    story.append(p("La fonction <font name='DVM'>anova_kruskal</font> vérifie la normalité de chaque groupe et l'homogénéité des "
                   "variances (Levene). Elle applique une ANOVA (F) si les deux conditions sont réunies, et sinon un "
                   "Kruskal-Wallis (H). Sur la comparaison bénin vs malin : <b>30 ANOVA et 10 Kruskal-Wallis ; 6 variables "
                   "significatives sur 40</b>, les mêmes que pour Mann-Whitney."))
    story.append(table([
        ["Variable", "Test retenu", "Statistique", "p-value", "Significatif"],
        ["area_worst", "Kruskal-Wallis (H)", "33 474,59", "≈ 0", "Oui"],
        ["radius_mean", "Kruskal-Wallis (H)", "28 629,42", "≈ 0", "Oui"],
        ["area_mean", "Kruskal-Wallis (H)", "28 629,42", "≈ 0", "Oui"],
        ["radius_worst", "Kruskal-Wallis (H)", "25 713,93", "≈ 0", "Oui"],
        ["perimeter_mean", "Kruskal-Wallis (H)", "23 801,15", "≈ 0", "Oui"],
        ["nucleus_size", "ANOVA (F)", "6,14", "0,0132", "Oui"],
        ["tumor_border_irregularity", "Kruskal-Wallis (H)", "3,25", "0,0715", "Non"],
        ["perimeter_se", "ANOVA (F)", "2,99", "0,0836", "Non"],
        ["texture_mean", "ANOVA (F)", "2,84", "0,0919", "Non"],
    ], [4.5 * cm, 3.8 * cm, 3 * cm, 2.4 * cm, 2.8 * cm]))
    story.append(p("Une comparaison multi-groupes sur les 4 quartiles d'area_worst confirme le résultat : les variables "
                   "géométriques varient fortement (H de 33 976 à 39 858). En revanche, cell_density (F = 0,40 ; p = 0,755) "
                   "et mitosis_rate (H = 0,12 ; p = 0,989) ne varient pas."))

    story.append(p("5.4 Test 4 — Chi-deux d'indépendance", H2))
    story.append(p("Le jeu nettoyé ne contient <b>aucune variable catégorielle native</b> : le test direct renvoie un tableau "
                   "vide. Pour le valider quand même, 8 variables ont été discrétisées en quartiles (Q1–Q4). L'effectif "
                   "attendu minimal de 4 291,25 respecte largement la condition de Cochran (≥ 5)."))
    story.append(table([
        ["Variable (quartiles)", "χ² (ddl = 3)", "p-value", "V de Cramér", "Décision"],
        ["area_worst", "36 120,61", "≈ 0", "0,858", "Dépendance"],
        ["area_mean", "30 732,43", "≈ 0", "0,792", "Dépendance"],
        ["radius_mean", "30 732,43", "≈ 0", "0,792", "Dépendance"],
        ["radius_worst", "26 722,11", "≈ 0", "0,738", "Dépendance"],
        ["perimeter_mean", "24 206,91", "≈ 0", "0,702", "Dépendance"],
        ["nucleus_size", "5,52", "0,1374", "0,011", "Indépendance"],
        ["cell_density", "2,10", "0,5523", "0,007", "Indépendance"],
        ["mitosis_rate", "0,64", "0,8866", "0,004", "Indépendance"],
    ], [4.3 * cm, 3 * cm, 2.4 * cm, 2.8 * cm, 4 * cm]))
    story.append(fig("12_contingence_chi2_quartiles.png", "Figure 12 — Taux de malignité (%) par quartile : gradient de risque très "
                     "net pour les variables géométriques, taux plat pour les variables biologiques.", max_h=8 * cm))
    story.append(p("Conclusion des tests", H2))
    story.append(p("Les quatre approches convergent vers les <b>5 mêmes biomarqueurs géométriques</b>. nucleus_size franchit "
                   "le seuil de 5 % mais avec un effet négligeable (r = 0,0137 ; V = 0,011). Avec un grand échantillon, "
                   "une p-value faible ne suffit pas : il faut toujours regarder la taille d'effet."))
    story.append(PageBreak())

    # --- 6. Prétraitement
    story.append(p("6. Prétraitement pour l'apprentissage", H1))
    story.append(p("Le script <font name='DVM'>preprocessing.py</font> suit le chapitre « Data Preprocessing » du TP Data Mining. "
                   "Résultats tirés de <font name='DVM'>pre/preprocessing.log</font> :"))
    story += bullets([
        "Séparation X (500 000 × 40) / y (500 000) ; les 40 variables sont conservées.",
        "Découpage stratifié 80/20 (random_state = 42) : TRAIN 400 000 lignes (260 000 bénins / 140 000 malins), TEST 100 000 lignes (65 000 / 35 000). Les 65,00 % / 35,00 % sont exactement préservés.",
        "Encodage de la cible par LabelEncoder (mapping {0: 0, 1: 1}) ; aucune colonne catégorielle, donc OneHotEncoder inactif.",
        "Pipeline ColumnTransformer : SimpleImputer(median) + RobustScaler, <b>fit sur TRAIN uniquement</b> pour éviter toute fuite de données (data leakage).",
        "Exports : X_train.csv (301,83 Mo), X_test.csv (75,46 Mo), y_train.csv, y_test.csv, preprocessor.joblib (4,91 Ko). Exécution totale : 54,88 s.",
    ])
    story.append(p("Comparaison des scalers (area_worst, valeurs du log)", H2))
    story.append(table([
        ["Méthode", "Min", "Max", "Moyenne", "Médiane", "Écart-type", "IQR"],
        ["Brut", "0,130", "4 010,403", "837,112", "787,221", "374,730", "490,046"],
        ["StandardScaler", "−2,234", "8,468", "0,000", "−0,133", "1,000", "1,308"],
        ["MinMaxScaler", "0,000", "1,000", "0,209", "0,196", "0,093", "0,122"],
        ["RobustScaler", "−1,606", "6,577", "0,102", "0,000", "0,765", "1,000"],
    ], [3.4 * cm, 1.8 * cm, 2.3 * cm, 2.2 * cm, 2.2 * cm, 2.3 * cm, 2.3 * cm]))
    story.append(p("Justification : MinMaxScaler écrase 75 % des valeurs dans un intervalle de largeur 0,122 à cause des "
                   "extrêmes. StandardScaler dépend de la moyenne et de l'écart-type, eux-mêmes gonflés par les outliers. "
                   "RobustScaler (médiane + IQR) n'est pas affecté par les valeurs aberrantes : <b>il est retenu</b>."))
    story.append(PageBreak())

    # --- 7. Benchmark
    story.append(p("7. Benchmark des modèles", H1))
    story.append(p("<b>" + NA + ".</b> Le dépôt ne contient encore aucun script ni notebook d'entraînement "
                   "(<font name='DVM'>notebooks/training.ipynb</font> et <font name='DVM'>src/train_model.py</font> sont cités "
                   "dans le README mais absents). Aucune métrique n'a donc été produite. Le tableau ci-dessous est la "
                   "<b>grille d'évaluation prévue</b>, à remplir après l'entraînement.", NOTE))
    story.append(p("7.1 Protocole prévu", H2))
    story += bullets([
        "Données : X_train / X_test issus de preprocessing.py (400 000 / 100 000 lignes, RobustScaler).",
        "Modèle principal annoncé dans le README : <b>Random Forest</b>. Comparaison suggérée avec une Régression logistique (référence linéaire) et un modèle de gradient boosting.",
        "Gestion du déséquilibre 65/35 : class_weight='balanced' (recommandation du nettoyage).",
        "Métrique principale : <b>Recall de la classe maligne</b> (taux de cancers détectés). Métrique secondaire : <b>ROC-AUC</b>, qui mesure le pouvoir de séparation indépendamment du seuil.",
        "Vérification prévue (Décision 4 de l'EDA) : comparer feature_importances_ du Random Forest avec le classement des 5 variables géométriques.",
    ])
    story.append(p("7.2 Tableau Recall / ROC-AUC", H2))
    story.append(table([
        ["Modèle", "Recall (malin)", "ROC-AUC"],
        ["Régression logistique", NA, NA],
        ["Random Forest", NA, NA],
        ["Gradient Boosting", NA, NA],
    ], [6 * cm, 5.25 * cm, 5.25 * cm], na_rows=True))
    story.append(Spacer(1, 10))

    # --- 8. SHAP
    story.append(p("8. Explicabilité des prédictions avec SHAP", H1))
    story.append(p("<b>" + NA + ".</b> SHAP n'est ni installé (absent des requirements.txt) ni utilisé dans le projet : "
                   "aucune valeur SHAP ni aucun graphique n'existe. Cette section présente la méthode prévue.", NOTE))
    story.append(p("8.1 Principe", H2))
    story.append(p("SHAP (<i>SHapley Additive exPlanations</i>) vient de la théorie des jeux coopératifs. Chaque variable est un "
                   "« joueur », et la prédiction est le « gain » à répartir entre eux. La valeur de Shapley d'une variable "
                   "est sa contribution marginale moyenne, calculée sur tous les ordres possibles d'ajout des variables. "
                   "Pour une patiente donnée, on obtient une décomposition additive :"))
    story.append(p("f(x) = E[f(X)] + φ<sub>1</sub> + φ<sub>2</sub> + … + φ<sub>40</sub>", ParagraphStyle("eq", parent=BODY, alignment=TA_CENTER, fontName="DV-B")))
    story.append(p("E[f(X)] est la prédiction moyenne (valeur de base) et φ<sub>j</sub> la contribution de la variable j. Un φ "
                   "positif pousse vers « malin », un φ négatif vers « bénin ». Pour les modèles à base d'arbres comme le "
                   "Random Forest, <font name='DVM'>shap.TreeExplainer</font> calcule ces valeurs de façon exacte et rapide."))
    story.append(p("8.2 Usage prévu dans BreastDiagAI", H2))
    story += bullets([
        "<b>Explication globale</b> (summary plot / beeswarm) : classer les 40 variables par |φ| moyen et confronter ce classement aux 4 tests statistiques. On s'attend, sans pouvoir le confirmer, à retrouver les variables géométriques en tête.",
        "<b>Explication locale</b> (waterfall / force plot) : pour chaque prédiction de l'application, montrer les 3 à 5 variables qui ont le plus pesé. C'est l'objectif « expliquer pourquoi » du projet.",
        "Aujourd'hui, le champ <font name='DVM'>explanation</font> de l'API est un texte produit par des seuils fixes, et non par SHAP.",
    ])
    story.append(PageBreak())

    # --- 9. Architecture
    story.append(p("9. Architecture applicative : FastAPI + Streamlit", H1))
    story.append(p("9.1 Ce qui existe : backend FastAPI", H2))
    story.append(p("Le dossier <font name='DVM'>app/backend/</font> contient une API REST (<font name='DVM'>main.py</font>, "
                   "FastAPI ≥ 0.110, Uvicorn) avec une base SQLite gérée par SQLAlchemy "
                   "(<font name='DVM'>breastdiagai.db</font>). Organisation en couches :"))
    story.append(table([
        ["Couche", "Fichier", "Rôle"],
        ["Configuration", "config.py", "Chemins, URL SQLite, origines CORS (localhost:5173, :3000)"],
        ["Persistance", "database.py, models/prediction.py", "Table predictions : 6 mesures, features_json, diagnosis, confidence, risk_level, notes, created_at"],
        ["Validation", "schemas/prediction.py", "Pydantic : radius_mean, area_worst, radius_worst obligatoires ; texture_mean, perimeter_mean, concavity_mean optionnels"],
        ["Logique métier", "services/prediction_service.py", "predict_diagnosis() — seul fichier à modifier pour brancher le vrai modèle"],
        ["Routes", "routers/predictions.py, routers/analytics.py", "Endpoints REST (tableau ci-dessous)"],
        ["Statique", "/static/eda_plots", "Graphiques EDA (SVG) servis au frontend"],
    ], [3 * cm, 5.2 * cm, 8.3 * cm]))
    story.append(Spacer(1, 6))
    story.append(table([
        ["Méthode", "Route", "Rôle"],
        ["POST", "/api/predict", "Calcule une prédiction et l'enregistre"],
        ["GET", "/api/predictions", "Historique des prédictions"],
        ["GET", "/api/predictions/{id}", "Détail d'une prédiction"],
        ["DELETE", "/api/predictions/{id}", "Suppression d'une prédiction"],
        ["GET", "/api/analytics/stats", "Statistiques globales de l'historique"],
        ["GET", "/ et /health", "État de l'API"],
    ], [2.5 * cm, 5 * cm, 9 * cm]))
    story.append(p("<b>Limite actuelle :</b> <font name='DVM'>predict_diagnosis()</font> n'utilise pas de modèle entraîné. Elle "
                   "calcule un score pondéré à partir de 4 mesures, avec des seuils codés à la main, puis lui applique "
                   "une sigmoïde. Le code le signale par des TODO, et <font name='DVM'>app/docs/README.md</font> précise que "
                   "« les prédictions affichées reposent sur une simulation / heuristique démonstrative temporaire ».", NOTE))
    story.append(p("9.2 Ce qui existe : frontend React", H2))
    story.append(p("L'interface est une application <b>React + Vite + Tailwind CSS</b> (<font name='DVM'>app/frontend/</font>) avec "
                   "5 pages : Accueil, Prédiction, Historique, Analytiques, Notre histoire. Elle propose un thème clair/nuit, "
                   "un affichage adapté au mobile et un avertissement médical. Elle appelle l'API via "
                   "<font name='DVM'>src/services/api.js</font>."))
    story.append(p("9.3 Interface Streamlit", H2))
    story.append(p("<b>" + NA + ".</b> Le projet ne contient pas d'application Streamlit "
                   "(<font name='DVM'>app/streamlit_app.py</font> n'existe pas, et streamlit ne figure dans aucun "
                   "requirements.txt). L'interface utilisateur réelle est le frontend React décrit ci-dessus.", NOTE))
    story.append(p("9.4 Flux d'une prédiction", H2))
    story.append(p("Utilisateur → formulaire (React ou, plus tard, Streamlit) → <font name='DVM'>POST /api/predict</font> → "
                   "validation Pydantic → <font name='DVM'>predict_diagnosis()</font> → enregistrement SQLite → réponse JSON "
                   "(diagnosis, confidence, risk_level, probability_malignant, explanation, disclaimer). Une fois le modèle "
                   "entraîné, il suffira de charger <font name='DVM'>preprocessor.joblib</font> et le modèle dans le service, "
                   "puis d'ajouter les valeurs SHAP à <font name='DVM'>explanation</font>.", BODY))
    story.append(p("<b>Incohérence à corriger avant l'intégration :</b> le commentaire du service liste les 30 variables du "
                   "format Wisconsin (par ex. <font name='DVM'>'concave points_mean'</font>, avec une espace). Or le "
                   "préprocesseur attend les <b>40</b> variables du jeu BreastDiagAI (<font name='DVM'>concave_points_mean</font>, "
                   "<font name='DVM'>nucleus_size</font>…), et l'API n'en reçoit que 6.", BODY))
    story.append(PageBreak())

    # --- 10. Conclusion
    story.append(p("10. Bilan, limites et perspectives", H1))
    story.append(p("10.1 Bilan", H2))
    story += bullets([
        "Un pipeline de données propre, journalisé et reproductible : nettoyage (0 NaN, 0 doublon), EDA sur 40 variables, 4 tests statistiques, prétraitement sans fuite de données.",
        "Un résultat scientifique cohérent : 5 variables géométriques (area_worst en tête, V de Cramér 0,858, r rang-bisérial ≈ 1) portent le signal. Les 35 autres sont statistiquement indépendantes de la cible.",
        "Une application web fonctionnelle (API FastAPI + interface React) prête à recevoir un modèle.",
    ])
    story.append(p("10.2 Limites", H2))
    story += bullets([
        "Aucun modèle entraîné : benchmark, SHAP et intégration du modèle restent à faire.",
        "Tests statistiques réalisés sur 49 056 lignes, à cause d'un fichier local corrompu. À rejouer sur les 500 000 lignes.",
        "Jeu de données vraisemblablement synthétique : pas de généralisation clinique possible.",
        "Prédictions actuelles de l'application simulées. L'outil ne doit pas être présenté comme diagnostique.",
    ])
    story.append(p("10.3 Perspectives", H2))
    story += bullets([
        "Écrire <font name='DVM'>notebooks/training.ipynb</font> : Régression logistique, Random Forest et boosting, avec class_weight='balanced', évalués sur le Recall malin et le ROC-AUC.",
        "Ajouter SHAP (TreeExplainer) : explications globales et locales.",
        "Brancher le modèle dans <font name='DVM'>prediction_service.py</font> et aligner le schéma d'entrée sur les 40 variables.",
        "Optionnel : une interface Streamlit légère pour la démonstration.",
    ])
    story.append(p("Annexe — Fichiers sources", H2))
    story.append(table([
        ["Fichier", "Contenu utilisé dans ce rapport"],
        ["cleaning_report.log", "Audit, outliers, corrélations, classes, mémoire"],
        ["RAPPORT_EDA_v2.md", "Classement des 5 variables, décisions EDA"],
        ["results/eda/stats_by_group.csv", "Moyennes, écarts-types, min, max par classe"],
        ["notebooks/02_statistical_eda_validation.ipynb", "Figures 1–12 et résultats des 4 tests"],
        ["src/statistical_tests.py", "Implémentation des 4 tests"],
        ["pre/preprocessing.log", "Découpage, scalers, exports"],
        ["app/backend/**", "Architecture FastAPI"],
    ], [7 * cm, 9.5 * cm]))

    doc = Doc(str(OUT), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
              bottomMargin=2 * cm, title="BreastDiagAI — Rapport de projet", author="Groupe IASD29")
    doc.multiBuild(story, onFirstPage=cover, onLaterPages=on_page)
    print(f"PDF généré : {OUT}")


if __name__ == "__main__":
    build()
