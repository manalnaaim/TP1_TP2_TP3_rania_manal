# Semaine 6 : le paquet, notes du binôme

## 1. Pourquoi le modèle n'est-il pas dans la roue ? Comment le paquet le trouve-t-il ?

Le modèle ne doit pas être dans la roue parce qu'il est trop lourd et qu'on doit pouvoir le réentraîner sans recréer un paquet à chaque fois. Le code reste le même et joblib change.

Pour que la roue le trouve, on a du utiliser la variable `SENTIMENT_MODELE`. Quand on l'a installée dans un dossier temporaire (`roue-tp6`), on a vu le message "modèle introuvable" tant qu'on n'avait pas mis cette variable. Une fois la variable mise avec le chemin vers le .joblib, ça a marché.

## 2. Qu'est-ce qui a changé dans api/model.py quand predict() est entré dans le paquet, et pourquoi est-ce mieux ?

Avant, on avait des lignes avec `sys.path.insert` dans `api/model.py` pour dire à Python d'aller chercher dans le dossier `src`. Ça marchait mais ce n'etait pas une bonne solution. 

Maintenant qu'on a déplacé `predict.py` dans `sentiment_app/`, on a juste mis `from sentiment_app.predict import ...`. C'est plus propre, c'est un import normal. On n'a plus besoin de toucher au chemin de Python à la main. Le test `test_l_api_ne_bricole_plus_le_chemin_de_python` vérifie justement qu'il n'y a plus de `sys.path` dans le dossier `api/`.

## 3. La roue installée hors du dépôt : qu'a-t-il fallu lui fournir, et pourquoi scikit-learn est-il épinglé dans pyproject.toml ?

Il a fallu lui donner le chemin du modèle avec `SENTIMENT_MODELE`, comme on l'a dit à la question 1.

Pour scikit-learn, si on entraîne le modèle avec une version et qu'on le relit avec une autre, ça peut planter. Par exemple l'erreur `AttributeError: 'LogisticRegression' object has no attribute 'multi_class'`. Pour éviter ça, on a mis `scikit-learn>=1.5,<1.6` dans le `pyproject.toml` et dans la CI, comme ça les deux utilisent la même version.