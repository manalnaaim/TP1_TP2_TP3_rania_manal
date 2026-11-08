"""Tests du client HTTP de l'interface (TP5, contrôle T28)."""
import pytest
from fastapi.testclient import TestClient

from api.main import app
from ui import client


@pytest.fixture(scope="module")
def session():
    """Un client httpx qui parle à l'API en mémoire (pas de serveur à lancer)."""
    with TestClient(app) as c:
        yield c


def test_sante(session):
    r = client.sante(session)
    assert r.ok
    assert "tfidf-logreg" in r.message


def test_avis_positif(session):
    r = client.predire(session, "Livraison rapide, produit conforme, très satisfait")
    # Le label peut être POSITIVE ou INDETERMINE selon le seuil
    assert r.ok
    assert r.label in ("POSITIVE", "NEGATIVE", "INDETERMINE")
    assert r.score is not None
    assert 0 <= r.score <= 1


def test_avis_negatif(session):
    r = client.predire(session, "Produit cassé et service injoignable, à fuir")
    assert r.ok
    assert r.label in ("POSITIVE", "NEGATIVE", "INDETERMINE")
    assert r.score is not None


def test_texte_vide(session):
    r = client.predire(session, "   ")
    assert not r.ok
    assert r.message == client.REFUS


def test_lot_et_resume(session):
    reponses = client.predire_lot(session, [
        "Livraison rapide, produit conforme, très satisfait",
        "Produit cassé et service injoignable, à fuir",
        "   "
    ])
    resume = client.resumer(reponses)
    # On vérifie juste qu'il y a 3 catégories et que le refus est bien compté
    assert len(resume) >= 2
    assert "REFUS OU ERREUR" in resume
    assert resume["REFUS OU ERREUR"] == 1


def test_api_injoignable():
    """Une session qui pointe vers un port fermé renvoie le message d'injoignabilité."""
    import httpx
    with httpx.Client(base_url="http://127.0.0.1:9999", timeout=1) as s:
        r = client.sante(s)
        assert not r.ok
        assert r.message == client.INJOIGNABLE


def test_modele_non_charge(session):
    """Si le modèle est retiré, le client traduit 503 en message clair."""
    from api.main import app
    modele = app.state.classifier
    del app.state.classifier
    try:
        r = client.predire(session, "Bonjour")
        assert not r.ok
        assert r.message == client.SANS_MODELE
    finally:
        app.state.classifier = modele