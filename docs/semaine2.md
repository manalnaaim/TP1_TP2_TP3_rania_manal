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

## 4. Limites constatées

- **Décalage de domaine** : avec le modèle Allociné, l'avis « Livraison rapide, produit conforme, très satisfait » ressort `negative (confiance 50 %)`. Le vocabulaire du commerce est absent du corpus de films, et la confiance proche de 50 % signale l'incertitude.
- **Avis mitigés** : le modèle ne distingue pas « négatif puis positif » de « positif puis négatif » (mêmes mots, ordre différent).
- **Version de scikit-learn** : nos scores diffèrent légèrement des chiffres de référence, ce qui montre qu'un résultat de modèle n'est pas reproductible à l'identique entre environnements.