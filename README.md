# sentiment-app : dépôt du binôme

Application fil rouge du cours *Développement et déploiement d'applications intelligentes*.
Ce dépôt grandit chaque semaine ; la semaine 1 met en place le cadrage et l'environnement.

## Installation (3 commandes)

``bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
``

## Vérifier son installation

``bash
python scripts/check_setup.py    # diagnostic lisible : versions, dossiers, Git
pytest -q                        # mêmes vérifications sous forme de tests
``

La démarche complète de test, étape par étape, est dans `TESTS.md`.

## Structure

``text
sentiment-app/
├── README.md                # ce fichier
├── requirements.txt         # dépendances de tout le semestre
├── requirements-dev.txt     # outils de qualité (ruff, mypy, pre-commit)
├── pyproject.toml           # configuration de ruff, mypy et coverage
├── pytest.ini               # configuration de pytest
├── .gitignore               # fichiers exclus de Git
├── .pre-commit-config.yaml  # crochet de pré-commit
│
├── api/                     # API FastAPI (TP3)
│   ├── __init__.py
│   ├── main.py              # routes /, /health, /predict
│   ├── model.py             # enveloppe du modèle (seuil d'abstention)
│   └── schemas.py           # contrat Pydantic (validation)
│
├── ui/                      # Interface Streamlit (TP5)
│   ├── __init__.py
│   ├── app.py               # page web (un avis / fichier d'avis)
│   └── client.py            # client HTTP qui appelle l'API
│
├── src/                     # Modèle et scripts (TP2)
│   ├── make_demo.py         # génère le jeu de démonstration
│   ├── train.py             # entraîne le modèle (TF-IDF + logreg)
│   ├── evaluate.py          # évalue et affiche les erreurs
│   ├── predict.py           # fonction predict() utilisée par l'API
│   ├── courbe_seuil.py      # mesure le seuil d'abstention
│   └── bilan_jeu_or.py      # bilan des 20 avis du jeu d'or
│
├── tests/                   # Tests pytest (TP1 à TP5)
│   ├── test_environment.py  # tests d'environnement (TP1)
│   ├── test_cadrage.py      # tests des fiches de cadrage (TP1)
│   ├── test_git_history.py  # tests de l'historique Git (TP1)
│   ├── test_model.py        # tests du modèle (TP2)
│   ├── test_api.py          # tests de l'API (TP3)
│   ├── test_limites.py      # tests aux limites (TP4)
│   ├── test_integration.py  # tests d'intégration (TP4)
│   ├── test_jeu_or.py       # tests du jeu d'or (TP4)
│   ├── test_client.py       # tests du client HTTP (TP5)
│   └── test_interface.py    # tests de la page Streamlit (TP5)
│
├── data/                    # jeux de données
│   ├── .gitkeep
│   ├── sample_reviews.csv   # exemple fourni au TP1
│   ├── demo_reviews.csv     # généré par make_demo.py (hors Git)
│   ├── jeu_or.csv           # les 20 avis du jeu d'or (TP4)
│   └── avis_exemple.csv     # exemple pour l'interface (TP5)
│
├── models/                  # modèles entraînés
│   ├── .gitkeep
│   ├── metrics.json         # mesures du modèle (versionné)
│   └── sentiment.joblib     # modèle (jamais dans Git)
│
├── scripts/                 # utilitaires
│   ├── check_setup.py       # diagnostic de l'environnement
│   ├── new_cadrage.py       # crée une nouvelle fiche de cadrage
│   ├── setup.ps1            # installation sous Windows
│   └── setup.sh             # installation sous Linux/macOS
│
└── docs/                    # documentation et comptes rendus
    ├── cadrage/             # fiches de cadrage (TP1)
    │   ├── TEMPLATE.md
    │   ├── EXEMPLE-corrige.md
    │   ├── BANQUE-DE-CAS.md
    │   ├── cas1-pharmacie.md
    │   ├── cas2-reglement.md
    │   └── cas3-avis-negatifs.md
    ├── semaine2.md          # compte rendu TP2
    ├── semaine3.md          # compte rendu TP3
    ├── semaine4.md          # compte rendu TP4
    └── semaine5.md          # compte rendu TP5
``

## Membres du binôme

| Rôle | Nom | Identifiant GitHub | Travail de la semaine 1 |
| --- | --- | --- | --- |
| Membre A | Naaim Manal | [@manalnaaim](https://github.com/manalnaaim) | Cadrage cas 3 + tests + check_setup + vérification CI |
| Membre B | Abdelali Rania | [@Rania20042004](https://github.com/Rania20042004) | Cadrage cas 1 et 2 + dépôt GitHub + setup |

## Répartition du travail (TP1 à TP5)

| Semaine | Membre A (Manal) | Membre B (Rania) |
| --- | --- | --- |
| **TP1** | Cadrage cas 3, création du dépôt, script `check_setup`, vérification CI. | Rédaction des fiches cas 1 et 2, setup de l'environnement. |
| **TP2** | Installation du kit, entraînement du modèle (démo et Allociné), `docs/semaine2.md`. | Relecture des erreurs, vérification des métriques. |
| **TP3** | Création de l'API (`api/main.py`), correction des schémas, tests `/docs`. | Rédaction de `docs/semaine3.md`, vérification des refus (422). |
| **TP4** | Tests d'intégration (`test_integration.py`), correction des pannes (500), jeu d'or. | Tests du client, vérification des erreurs (xfail). |
| **TP5** | Création de l'interface Streamlit (`ui/app.py`), connexion avec l'API. | Rédaction de `docs/semaine5.md`, tests des erreurs (API injoignable). |

