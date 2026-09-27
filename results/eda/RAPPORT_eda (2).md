# Rapport d'analyse exploratoire (EDA) — BreastDiagAI

**Réalisé par :** IASD08
**Fichier analysé :** breast_cancer_cleaned.csv (500 000 lignes, 40 features)
**Version :** analyse complète des 40 features (histogrammes, boxplots, heatmap)

---

## 1. Statistiques par groupe — classement réel des features

En calculant l'écart absolu de moyenne entre bénin et malin sur les 40
features, un classement net se dégage :

| Rang | Feature | Bénin (moyenne) | Malin (moyenne) | Ratio Malin/Bénin |
|---|---|---|---|---|
| 1 | `area_worst` | 617,70 | 1244,93 | **×2,02** |
| 2 | `area_mean` | 498,22 | 914,51 | ×1,84 |
| 3 | `perimeter_mean` | 74,40 | 101,75 | ×1,37 |
| 4 | `radius_mean` | 12,40 | 16,96 | ×1,37 |
| 5 | `radius_worst` | 14,42 | 18,98 | ×1,32 |

**Toutes les 35 autres features** (`texture_mean`, `nucleus_size`,
`cell_density`, `mitosis_rate`, `tumor_border_irregularity`,
`chromatin_density`, `cell_variation`, etc.) ont un écart de moyenne
quasi nul entre bénin et malin (différence < 1 % dans presque tous les
cas), malgré des noms évoquant des caractéristiques biologiques
pertinentes.

---

## 2. Distributions (histogrammes) — 40 features

- **5 features à distribution clairement séparée** (deux courbes bien
  distinctes, décalées l'une par rapport à l'autre) : `area_worst`,
  `area_mean`, `perimeter_mean`, `radius_mean`, `radius_worst`.
- **35 features à distributions superposées** : que ce soit des features
  standardisées (`smoothness_mean`, `concavity_mean`...) ou des features à
  échelle réelle mais non discriminantes (`nucleus_size`, `cell_density`,
  `mitosis_rate`, `tumor_border_irregularity`) — dans tous les cas, la
  courbe verte (bénin) et la courbe rouge (malin) se superposent presque
  parfaitement.
- Point notable : certaines features au nom "biologique" prometteur
  (`mitosis_rate`, `chromatin_density`, `nuclear_variation`) auraient pu
  laisser penser à un fort pouvoir prédictif, mais l'analyse montre que ce
  n'est pas le cas **prises individuellement**.

---

## 3. Boxplots comparatifs — 40 features

- **`area_worst`** : la séparation la plus nette de tout le dataset — la
  boîte "Malin" est presque entièrement au-dessus de la boîte "Bénin",
  avec un chevauchement minimal.
- **`radius_worst`** : bonne séparation également, confirmant l'intérêt
  des mesures "worst" (valeur extrême observée) en complément des
  moyennes.
- **`area_mean`, `perimeter_mean`, `radius_mean`** : séparation nette et
  cohérente, comme identifié dans l'analyse précédente.
- **Les 35 autres boxplots** : boîtes à la même hauteur, médianes
  identiques entre bénin et malin — aucune séparation visuelle, y compris
  pour les features non standardisées comme `mitosis_rate` ou
  `nucleus_size`.

---

## 4. Corrélations (heatmap) — 40×40 features

- Un bloc de forte corrélation (rouge foncé) entre `radius_mean`,
  `perimeter_mean` et `area_mean` — confirmé sur l'ensemble du dataset.
- Une corrélation modérée (orange, ~0,4-0,6) entre ce groupe et
  `radius_worst` / `area_worst`.
- **Aucune autre corrélation significative** parmi les 35 autres
  features : elles sont statistiquement indépendantes les unes des
  autres et des 5 features géométriques identifiées.

---

## 5. Décisions et recommandations pour l'entraînement du modèle

### Décision 1 — Features à conserver en priorité
Les 5 features suivantes portent l'essentiel du signal prédictif et
doivent être conservées sans hésitation :
`area_worst`, `area_mean`, `perimeter_mean`, `radius_mean`, `radius_worst`.

### Décision 2 — Gestion de la redondance
`area_mean`, `perimeter_mean` et `radius_mean` étant très corrélées entre
elles (>0,95), conserver **une seule** de ces trois pour l'entraînement
(recommandation : garder `radius_mean`, la plus simple à interpréter
cliniquement) plutôt que de supprimer au hasard. `radius_worst` reste
pertinent car corrélé plus modérément (~0,5) et apporte une information
complémentaire (valeur extrême vs moyenne).

**Nouvelle liste de features "cœur" recommandée :**
`radius_mean`, `area_worst`, `radius_worst`
(3 features au lieu des 2 initialement identifiées lors du nettoyage)

### Décision 3 — Ne pas supprimer les 35 autres features pour autant
Bien qu'individuellement peu discriminantes, ces features ne doivent
**pas** être retirées du modèle : un Random Forest est capable de
détecter des **interactions non linéaires** entre plusieurs variables
faibles qu'une simple comparaison de moyennes ne peut pas révéler. Les
supprimer risquerait de faire perdre au modèle un signal combiné invisible
en analyse univariée.

### Décision 4 — Score d'importance des features à vérifier après entraînement
Il faudra comparer ce classement "manuel" (basé sur l'écart de moyenne)
avec le classement `feature_importance` produit automatiquement par le
Random Forest après entraînement, pour vérifier si le modèle confirme ou
nuance cette analyse exploratoire.

### Décision 5 — Prudence sur l'interprétation clinique
Le fait que `mitosis_rate`, `chromatin_density` ou `nucleus_size` ne
montrent pas de différence significative ici est probablement une
caractéristique du **jeu de données synthétique** utilisé pour ce
projet académique, et ne doit pas être interprété comme une conclusion
médicale généralisable — un vrai jeu de données clinique pourrait montrer
des résultats différents pour ces variables.

---

## 6. Conclusion générale

L'analyse exploratoire complète (40 features) confirme et affine les
observations précédentes : **la taille de la tumeur** (mesurée par
`area_worst`, `area_mean`, `perimeter_mean`, `radius_mean`,
`radius_worst`) est de loin le facteur le plus déterminant et le plus
facilement observable pour distinguer une tumeur bénigne d'une tumeur
maligne dans ce dataset. Les 35 autres features n'apportent pas de signal
individuel visible, mais restent conservées dans le modèle pour leur
potentiel de contribution combinée. Ces conclusions orientent directement
les choix de préparation des données (`preprocessing.py`) et
d'entraînement (`train_model.py`) à venir.
