# sentiment-app : dépôt du binôme

Application fil rouge du cours **Développement et déploiement d'applications intelligentes**.

Ce dépôt grandit chaque semaine ; la semaine 1 met en place le cadrage et l'environnement.

## Installation (3 commandes)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Vérifier son installation

```bash
python scripts/check_setup.py    # Diagnostic lisible : versions, dossiers, Git
pytest -q                        # Mêmes vérifications sous forme de tests
```

La démarche complète de test, étape par étape, est dans `TESTS.md`.

## Structure

```text
sentiment-app/
├── README.md                 # Ce fichier
├── requirements.txt          # Dépendances de tout le semestre
├── requirements-dev.txt      # Outils de qualité (ruff, mypy, pre-commit)
├── pyproject.toml            # Configuration de ruff, mypy et coverage
├── pytest.ini                # Configuration de pytest
├── .gitignore                # Fichiers exclus de Git
├── .pre-commit-config.yaml   # Crochet de pré-commit
├── CHANGELOG.md              # Journal des versions (TP6)
│
├── sentiment_app/            # Paquet installable (TP6)
│   ├── __init__.py           # Version 0.6.0
│   ├── __main__.py           # Point d'entrée
│   ├── cli.py                # Commande sentiment
│   └── predict.py            # Fonction predict()
│
├── api/                      # API FastAPI (TP3)
│   ├── __init__.py
│   ├── main.py               # Routes /, /health, /predict
│   ├── model.py              # Enveloppe du modèle (seuil d'abstention)
│   └── schemas.py            # Contrat Pydantic (validation)
│
├── ui/                       # Interface Streamlit (TP5)
│   ├── __init__.py
│   ├── app.py                # Page web (un avis / fichier d'avis)
│   └── client.py             # Client HTTP qui appelle l'API
│
├── src/                      # Modèle et scripts (TP2)
│   ├── make_demo.py          # Génère le jeu de démonstration
│   ├── train.py              # Entraîne le modèle (TF-IDF + logreg)
│   ├── evaluate.py           # Évalue et affiche les erreurs
│   ├── predict.py             # Fonction predict() utilisée par l'API
│   ├── courbe_seuil.py       # Mesure le seuil d'abstention
│   └── bilan_jeu_or.py       # Bilan des 20 avis du jeu d'or
│
├── tests/                    # Tests pytest (TP1 à TP6)
│   ├── test_environment.py   # Tests d'environnement (TP1)
│   ├── test_cadrage.py       # Tests des fiches de cadrage (TP1)
│   ├── test_git_history.py   # Tests de l'historique Git (TP1)
│   ├── test_model.py         # Tests du modèle (TP2)
│   ├── test_api.py           # Tests de l'API (TP3)
│   ├── test_limites.py       # Tests aux limites (TP4)
│   ├── test_integration.py   # Tests d'intégration (TP4)
│   ├── test_jeu_or.py        # Tests du jeu d'or (TP4)
│   ├── test_client.py        # Tests du client HTTP (TP5)
│   ├── test_interface.py     # Tests de la page Streamlit (TP5)
│   └── test_packaging.py     # Tests du paquet (TP6)
│
├── data/                     # Jeux de données
│   ├── .gitkeep
│   ├── sample_reviews.csv    # Exemple fourni au TP1
│   ├── demo_reviews.csv      # Généré par make_demo.py (hors Git)
│   ├── jeu_or.csv            # Les 20 avis du jeu d'or (TP4)
│   └── avis_exemple.csv      # Exemple pour l'interface (TP5)
│
├── models/                   # Modèles entraînés
│   ├── .gitkeep
│   ├── metrics.json          # Mesures du modèle (versionné)
│   └── sentiment.joblib      # Modèle (jamais dans Git)
│
├── scripts/                  # Utilitaires
│   ├── check_setup.py        # Diagnostic de l'environnement
│   ├── new_cadrage.py        # Crée une nouvelle fiche de cadrage
│   ├── setup.ps1             # Installation sous Windows
│   └── setup.sh              # Installation sous Linux/macOS
│
└── docs/                     # Documentation et comptes rendus
    ├── cadrage/              # Fiches de cadrage (TP1)
    │   ├── TEMPLATE.md
    │   ├── EXEMPLE-corrige.md
    │   ├── BANQUE-DE-CAS.md
    │   ├── cas1-pharmacie.md
    │   ├── cas2-reglement.md
    │   └── cas3-avis-negatifs.md
    ├── semaine2.md            # Compte rendu TP2
    ├── semaine3.md            # Compte rendu TP3
    ├── semaine4.md            # Compte rendu TP4
    ├── semaine5.md            # Compte rendu TP5
    └── semaine6.md            # Compte rendu TP6
```

## Membres du binôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
|---|---|---|---|
| Membre A | Naaim Manal | [@manalnaaim](https://github.com/manalnaaim) | Cadrage cas 3 + tests + check_setup + vérification CI |
| Membre B | Abdelali Rania | [@Rania20042004](https://github.com/Rania20042004) | Cadrage cas 1 et 2 + dépôt GitHub + setup |

## Répartition du travail (TP1 à TP6)

| Semaine | Membre A (Manal) | Membre B (Rania) |
|---|---|---|
| **TP1** | Cadrage cas 3, création du dépôt, script `check_setup`, vérification CI. | Rédaction des fiches cas 1 et 2, setup de l'environnement. |
| **TP2** | Installation du kit, entraînement du modèle (démo et Allociné), `docs/semaine2.md`. | Relecture des erreurs, vérification des métriques. |
| **TP3** | Création de l'API (`api/main.py`), correction des schémas, tests `/docs`. | Rédaction de `docs/semaine3.md`, vérification des refus (422). |
| **TP4** | Tests d'intégration (`test_integration.py`), correction des pannes (500), jeu d'or. | Tests du client, vérification des erreurs (xfail). |
| **TP5** | Création de l'interface Streamlit (`ui/app.py`), connexion avec l'API. | Rédaction de `docs/semaine5.md`, tests des erreurs (API injoignable). |
| **TP6** | Création du paquet (`sentiment_app/`), configuration de la roue. | Rédaction de `docs/semaine6.md`, tests du paquet. | 
