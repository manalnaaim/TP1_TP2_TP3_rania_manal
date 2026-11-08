import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from api.main import app

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier."""
    with TestClient(app) as c:
        yield c

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "OK"

def test_predict_positif(client):
    r = client.post("/predict", json={"text": "Livraison rapide, produit conforme, très satisfait"})
    assert r.status_code == 200
    assert r.json()["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]

def test_predict_negatif(client):
    r = client.post("/predict", json={"text": "Produit cassé et service injoignable, à fuir"})
    assert r.status_code == 200
    assert r.json()["label"] in ["POSITIVE", "NEGATIVE", "INDETERMINE"]

def test_predict_texte_vide_422(client):
    r = client.post("/predict", json={"text": ""})
    assert r.status_code == 422

def test_predict_champ_manquant_422(client):
    r = client.post("/predict", json={})
    assert r.status_code == 422