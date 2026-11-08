# Semaine 5 : l'interface, notes du binôme

## 1. Pourquoi l'interface n'importe-t-elle jamais predict() ni le fichier .joblib ?

L'interface est un client de l'API. Elle n'a pas besoin de connaître le modèle ni scikit-learn : elle envoie des requêtes HTTP à l'API et traduit les réponses en messages pour l'utilisateur.

Cela présente plusieurs avantages :
- **Découplage** : on peut réentraîner le modèle et redémarrer l'API sans modifier l'interface.
- **Sécurité** : le modèle et le fichier .joblib restent sur le serveur, l'interface n'y a pas accès.
- **Scalabilité** : l'API peut être déployée sur une machine différente de l'interface.

C'est le principe de la séparation des responsabilités : l'interface ne fait qu'afficher, l'API fait le calcul.

## 2. Que se passe-t-il quand on envoie un texte fait d'espaces ?

Nous avons observé que l'API renvoie une erreur 422, que le client traduit en message clair : "Texte refusé : vide, fait d'espaces, ou de plus de 2000 caractères."

C'est le schéma Pydantic (`PredictRequest`) qui refuse le texte vide après `strip()`. Le client n'a pas besoin de faire cette vérification lui-même : il délègue à l'API, qui est la seule source de vérité pour le contrat d'entrée.

## 3. Que se passe-t-il quand l'API est arrêtée ?

Nous avons observé que l'interface affiche "API injoignable : lancez d'abord uvicorn api.main:app" au lieu de planter ou d'afficher une erreur technique.

C'est le client (`ui/client.py`) qui capture l'exception `httpx.TransportError` et la traduit en message compréhensible. L'utilisateur sait exactement quoi faire : relancer l'API.