# Semaine 3 : l'API, notes du binôme

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

Quand on a testé le contrôle T20 (en renommant le modèle), on a vu que l'API plantait direct au lancement avec une `FileNotFoundError` et que `Application startup failed` s'affichait dans le terminal. 

On pense que c'est mieux comme ça : si l'API démarre sans le modèle, elle va répondre des erreurs 503 à chaque requête et on ne comprendra pas d'où vient le problème. En plantant au démarrage, on voit tout de suite qu'il manque le fichier et on sait exactement quoi faire (relancer `python src/train.py`). C'est plus simple pour détecter les erreurs.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Oui, c'est un peu redondant. Le schéma Pydantic refuse le texte vide (on l'a vu avec le `field_validator` au TP4), et la fonction `predict()` du TP2 le refuse aussi.

Mais on a compris que c'est une sécurité. Si on appelle `predict()` directement depuis un script Python (sans passer par l'API), le schéma Pydantic n'est pas là pour vérifier. Du coup, c'est `predict()` qui fait le travail. Et si quelqu'un modifie le schéma plus tard, `predict()` bloque quand même. 

Par contre, au TP4 on a vu que ça posait problème parce que les deux refus n'étaient pas pareils (l'un renvoyait une erreur standard et l'autre une simple chaîne). C'est pour ça qu'on a dû les aligner et enlever l'erreur 422 dans `main.py`.