# Dataset nettoyé

Le fichier `breast_cancer_cleaned.csv` n'est pas inclus dans ce dépôt car il est trop volumineux (203 Mo, au-delà de la limite GitHub de 25 Mo pour un upload web).

## Comment le régénérer

1. Télécharger le dataset brut (voir `data/raw/README.md`)
2. Exécuter le script de nettoyage depuis la racine du projet :

​```bash
python src/clean_data.py --input data/raw/breast_cancer_40_features_1M.csv --output breast_cancer_cleaned.csv
​```

Le fichier sera généré, ainsi qu'un rapport détaillé (voir `results/cleaning_report.log` et `results/RAPPORT_NETTOYAGE.md`).
