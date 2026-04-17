# TP — Premiers pas en analyse de ventes (Python + Plotly)

## Objectif simple

À la fin, vous saurez :

- charger un fichier CSV ;
- créer une nouvelle colonne de calcul ;
- écrire des fonctions simples ;
- afficher des graphiques lisibles.

## Comment travailler

- Exécutez les cellules dans l’ordre, de haut en bas.
- Après chaque étape, vérifiez le résultat demandé.
- Si une cellule échoue, corrigez avant de continuer.

## Étape 1 — Importer les bibliothèques

### À faire

Exécuter la cellule d’import (`pandas`, `plotly`, `calendar`).

### Résultat attendu

Aucune erreur affichée.

## Étape 2 — Charger et préparer les données

### À faire

1. Charger `data.csv` dans un DataFrame `df`.
2. Garder uniquement les colonnes utiles ('CustomerID', 'Gender', 'Location', 'Product_Category', 'Quantity', 'Avg_Price', 'Transaction_Date', 'Month', 'Discount_pct').
3. Remplacer les valeurs manquantes dans `CustomerID` par 0 et convertir `CustomerID` en entier.
4. Convertir `Transaction_Date` en date.
5. Créer `Total_price` avec la remise.

### Résultat attendu

- `df.head()` affiche des lignes.
- `df.dtypes` montre les bons types.
- `Total_price` existe et contient des valeurs numériques.

## Étape 3 — Écrire les fonctions métier

### Fonctions à compléter

1. `calculer_chiffre_affaire(data)`
2. `frequence_meilleure_vente(data, top=10, ascending=False)`
3. `indicateur_du_mois(data, current_month=12, freq=True, abbr=False)`

### Résultat attendu

Chaque fonction retourne un résultat sans erreur.

## Étape 4 — Créer les graphiques

### Fonctions à compléter

1. `barplot_top_10_ventes(data)`
2. `plot_evolution_chiffre_affaire(data)`
3. `plot_chiffre_affaire_mois(data)`
4. `plot_vente_mois(data, abbr=False)`

### Résultat attendu

Les figures s’affichent correctement (barres, courbe, indicateurs).

## Étape 5 — Vérification finale

Exécuter les cellules de test en bas du notebook.
Si tout fonctionne : TP validé.

## Erreurs fréquentes (et solution rapide)

- Erreur de colonne introuvable : vérifier l’orthographe des noms de colonnes.
- Erreur de type sur les dates : vérifier `pd.to_datetime(...)`.
- Résultat vide sur un mois : vérifier la logique mois courant / mois précédent.
- Figure qui ne s’affiche pas : vérifier que la fonction retourne bien une figure Plotly.

## Conseils pour débuter sereinement

- Faites une chose à la fois.
- Testez chaque fonction juste après l’avoir écrite.
- Utilisez des noms de variables clairs.
- Demandez de l’aide dès la première erreur bloquante.
