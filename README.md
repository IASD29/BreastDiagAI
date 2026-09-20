# BreastDiagAI

Breast cancer  prediction .

## Notre histoire
Ce projet est né d'une expérience personnelle : la découverte d'une anomalie mammaire chez la mère d'un membre de l'équipe, et le parcours médical long et angoissant qui a suivi (mammographie, échographie, biopsie...).

De cette expérience est née une question : *l'intelligence artificielle peut-elle aider à détecter plus rapidement les situations nécessitant une attention médicale ?*

BreastAI n'a pas pour but de remplacer le médecin, mais d'offrir un outil d'aide à la décision — capable d'estimer si une tumeur présente des caractéristiques bénignes ou malignes, et d'expliquer pourquoi, pour rendre le dépistage plus rapide, accessible et compréhensible.

## Objectif
Prédire le diagnostic (bénin/malin) du cancer du sein à partir de données médicales.

## Dataset
Source : [Kaggle - Breast Cancer Dataset](https://www.kaggle.com/datasets/sharmajicoder/breast-cancer-dataset)
Taille : 500 000 observations

Voir `data/raw/README.md` pour les instructions de téléchargement.

## Structure du projet
- `data/raw/` : informations sur le dataset (non inclus, trop volumineux)
- `notebooks/` : notebooks d'entraînement et d'analyse
- `results/` : résultats, graphiques, modèle entraîné

## Équipe — Groupe IASD29
- IASD29 
- IASD08
- IASD19
- IASD24
- RSD19

## Comment exécuter
1. Installer les dépendances 
2. Télécharger le dataset (voir `data/raw/README.md`)
3. Ouvrir et exécuter `notebooks/training.ipynb`
