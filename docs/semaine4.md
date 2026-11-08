# Semaine 4 : tests approfondis et qualité, notes du binôme

## 1. Couverture

- Avant (étape A) : on avait **89 %** de couverture. Il manquait 6 lignes dans `api/main.py` et `api/model.py`. C'étaient les lignes des pannes (le 500, le 503) et la vérification des classes du modèle.
- Après (étape D) : on est monté à **97,75 %**. On n'a pas eu besoin d'exclure de lignes avec des `# pragma`, les tests d'intégration qu'on a écrits ont réussi à couvrir les pannes.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Quand on envoyait un texte avec juste des espaces, l'erreur 422 n'avait pas le même format que les autres. | `test_frontieres_du_contrat[texte-espaces]` | On a ajouté un `field_validator` dans `api/schemas.py` pour refuser le texte vide après `strip()`. |
| Quand le modèle plantait, l'API renvoyait une erreur 422 au lieu d'une 500. | `test_panne_du_modele_valueerror` | On a supprimé le `except ValueError` dans `api/main.py` pour que toutes les erreurs du modèle soient des 500. |
| Le modèle renvoyait `pos` / `neg` au lieu de `POSITIVE` / `NEGATIVE`. | `test_correspondance_explicite` | On a remplacé `.upper()` par une correspondance explicite dans `api/model.py`. |

## 3. Seuil d'abstention

- Voici ce qu'on a vu avec `python src/courbe_seuil.py` :
  - Seuil 0,50 : 58 avis (100%), exactitude 0,879, 7 erreurs, 0 vers un humain.
  - Seuil 0,60 : 42 avis (72%), exactitude 0,952, 2 erreurs, 16 vers un humain.
  - Seuil 0,70 : 37 avis (64%), exactitude 1,000, 0 erreur, 21 vers un humain.
- **Seuil choisi : 0,60**. On a préféré ce seuil parce qu'on passe de 7 erreurs à 2, et on n'envoie "que" 16 avis à un humain sur 58. C'est un bon équilibre : le modèle ne dit pas de bêtises, mais on ne fait pas tout relire par un humain.

## 4. Jeu d'or

- Le bilan (`python src/bilan_jeu_or.py`) donne **17 justes** et **3 erreurs franches** (qu'on a déclarées). Il n'y a pas eu d'abstention sur ces avis.
- Ce qu'on en déduit : le modèle est bon sur les avis faciles, mais il se trompe sur les négations ("pas mauvais", "pas le meilleur") et l'ironie ("j'adore attendre 3 semaines"). Comme c'est un TF-IDF, il compte juste les mots et ne comprend pas le sens de la phrase.

## 5. Outils statiques

- Au début, ruff a râlé **8 fois** (imports mal triés, `zip` sans `strict`) et mypy a donné **2 erreurs** (il ne trouvait pas `joblib` et `predict`).
- Ruff et mypy n'ont trouvé **aucun** des défauts de la partie 2. Ils vérifient juste que le code est bien écrit, mais ils ne peuvent pas voir qu'un texte avec des espaces passe le schéma par exemple. C'est pour ça que les tests sont indispensables.