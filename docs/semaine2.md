<<<<<<< HEAD
# TP2 : Analyse et décisions

## 1. Mes chiffres
**Sur le jeu de démonstration :**
- F1 macro : 0.879 (le seuil technique de 0.85 est passé)
- Rappel sur la classe négative : 0.931
- Nombre d'erreurs : 7 sur 58

**Sur le jeu Allociné :**
- L'entraînement sur Allociné n'a pas pu être effectué sur mon poste en raison d'une erreur liée à la dépendance `pyarrow` (impossible de lire le fichier Parquet). J'ai donc conservé le modèle de démonstration.
- *Note de l'énoncé* : avec Allociné, le F1 macro attendu est de 0.9020 et le rappel négatif de 0.8905.

## 2. Lecture des erreurs
Les trois erreurs affichées par `evaluate.py` sont :
1. "Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme..." (vrai positif, prédit négatif).
2. "Commande jamais reçue et remboursement en attente au début, sauf que ensuite je recommande..." (vrai positif, prédit négatif).
3. "Service impeccable et livraison en avance sur le papier, sauf que ensuite produit cassé..." (vrai négatif, prédit positif).

**Ce qu'elles ont en commun :**
Ces trois avis sont des avis "mitigés". Ils sont construits en deux propositions séparées par un retournement de situation ("sauf que ensuite"). L'étiquette (positive ou négative) correspond à la seconde proposition, celle qui conclut l'avis.

**Pourquoi le modèle se trompe :**
Notre modèle utilise une vectorisation TF-IDF (un "sac de mots"). Il ne comprend pas l'ordre des mots ni la grammaire. Pour lui, "bon puis mauvais" et "mauvais puis bon" produisent exactement le même vecteur. Il ne sait pas que c'est la fin de la phrase qui détermine le sentiment global. Pour corriger cela, il faudrait utiliser un modèle qui comprend la séquence (comme un réseau de neurones récurrent ou un Transformer type BERT), ou ajouter des règles métier qui accordent plus de poids aux mots situés après "mais" ou "sauf que".

## 3. Décision d'accepter ou refuser
Le modèle de démonstration est **accepté** car il passe le seuil technique (F1 macro de 0.879 > 0.85) et qu'il atteint largement le besoin métier de la fiche de cadrage (Rappel négatif de 0.931 > 0.90). 

Cependant, si l'on se base sur les chiffres théoriques d'Allociné (Rappel de 0.8905), le modèle serait **refusé** pour la mise en production : il laisserait passer environ 11 clients mécontents sur 100 sans alerte, ce qui est inacceptable pour le service relation client.

## 4. Limites constatées
- **Décalage de domaine :** Avec le modèle Allociné, un avis de livraison ("Livraison rapide, produit conforme") aurait été classé "négatif" avec une confiance de 54%, car le modèle n'a lu que des critiques de films. C'est une limite majeure : une métrique ne vaut que sur des données de même nature que celles d'entraînement.
- **Taille du jeu de test :** Le jeu de démonstration ne contient que 58 avis de test, ce qui rend les scores statistiquement fragiles.
- **Incompréhension de la négation et des retournements :** Le sac de mots ne gère pas la structure des phrases.
=======
# Semaine 2 : entraînement, évaluation, décision

## 1. Nos chiffres

| Mesure | Démonstration (290 avis) | Allociné (20 000 avis) |
| --- | --- | --- |
| Avis en test | 58 | 4 000 |
| F1 macro | 0.879 | 0.920 |
| Rappel sur la classe négative | 0.931 | 0.911 |
| Erreurs sur le jeu de test | 7 | 318 |

Écart par rapport aux chiffres de référence de l'énoncé : nos scores diffèrent légèrement (F1 0.879 au lieu de 0.8961 en démo, 0.920 au lieu de 0.9020 sur Allociné, 7 erreurs au lieu de 6, 318 au lieu de 392). La cause probable est une version plus récente de scikit-learn sur nos postes (warning `OptimizeWarning: Unknown solver options: iprint`). Nous n'avons pas modifié les seuils.

## 2. Lecture des trois erreurs (démo)

Les trois avis mal classés affichés par `evaluate.py` :
- « Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme à la d... » (positif prédit négatif)
- « Commande jamais reçue et remboursement en attente au début, sauf que ensuite je recommande... » (positif prédit négatif)
- « Service impeccable et livraison en avance sur le papier, sauf que ensuite produit cassé à... » (négatif prédit positif)

**Ce qu'ils ont en commun** : ce sont des avis **mitigés**, construits par paires avec exactement les mêmes mots, seul l'ordre des propositions change (« X négatif, sauf que ensuite Y positif » vs « X positif, sauf que ensuite Y négatif »). Un modèle TF-IDF + régression logistique **ignore l'ordre des mots** : il voit les mêmes termes dans les deux avis et leur attribue le même score. C'est une limite structurelle de l'approche « sac de mots ».

## 3. Décision

Deux seuils doivent être vérifiés :
- **Seuil technique** (`train.py`) : F1 macro ≥ 0,85 → les deux modèles le passent (0.879 et 0.920).
- **Seuil métier** (fiche de cadrage cas 3) : rappel négatif ≥ 0,90 → la démo passe (0.931), Allociné passe aussi (0.911) sur nos chiffres.

**Décision** : nous acceptons le modèle de démonstration pour l'API de la semaine 3, car il est reproductible et dépasse les deux seuils. Le modèle Allociné est meilleur en F1 macro mais nous notons que le rappel négatif est proche du seuil, et que le décalage de domaine le rend inutilisable pour des avis de commerce.

> Note : sur les chiffres de référence de l'énoncé, Allociné échouait au seuil métier (0.8905 < 0.90). Sur nos chiffres, il passe de justesse (0.911). Cette différence illustre qu'un seuil métier doit être vérifié sur **ses propres** données, pas sur celles d'un autre.

## 4. Limites constatées

- **Décalage de domaine** : avec le modèle Allociné, l'avis « Livraison rapide, produit conforme, très satisfait » ressort `negative (confiance 50 %)`. Le vocabulaire du commerce est absent du corpus de films, et la confiance proche de 50 % signale l'incertitude.
- **Avis mitigés** : le modèle ne distingue pas « négatif puis positif » de « positif puis négatif » (mêmes mots, ordre différent).
- **Version de scikit-learn** : nos scores diffèrent légèrement des chiffres de référence, ce qui montre qu'un résultat de modèle n'est pas reproductible à l'identique entre environnements.
>>>>>>> 04fdeb0c48fadf5e8eb8fa315157ae9fdc15426c
