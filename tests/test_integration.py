import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.model import charger_modele


# D.1 : Démarrage réel
def test_demarrage_reel_charge_le_modele():
    """D.1 : un client ouvert par « with » exécute le lifespan."""
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert "OK" in r.json()["status"]
        assert "tfidf-logreg" in r.json()["model"]

# D.2 : Modèle absent
def test_modele_absent(monkeypatch):
    """D.2 : le modèle absent fait échouer le démarrage."""
    import joblib
    # On simule un fichier introuvable en forçant joblib.load à lever une exception
    monkeypatch.setattr(joblib, "load", lambda path: (_ for _ in ()).throw(FileNotFoundError("Modèle introuvable")))
    
    # On vide le cache pour forcer un rechargement
    charger_modele.cache_clear()
    
    with pytest.raises(FileNotFoundError):
        charger_modele()

# D.3 : Modèle non chargé
def test_modele_non_charge():
    """D.3 : si le modèle est retiré de app.state, l'API répond 503."""
    with TestClient(app) as client:
        # On sauvegarde l'état actuel
        modele_sauvegarde = app.state.classifier
        del app.state.classifier
        
        r_health = client.get("/health")
        assert r_health.status_code == 503
        
        r_predict = client.post("/predict", json={"text": "Bonjour"})
        assert r_predict.status_code == 503
        
        # On remet le modèle en place
        app.state.classifier = modele_sauvegarde

# D.4 : Modèle en panne
def test_panne_du_modele_runtimeerror(monkeypatch):
    """D.4 : une panne RuntimeError répond 500."""
    class ModeleEnPanne:
        def predict(self, text):
            raise RuntimeError("bug interne")
            
    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", ModeleEnPanne())
        r = client.post("/predict", json={"text": "Bonjour"})
        assert r.status_code == 500
        assert "bug interne" not in r.text

def test_panne_du_modele_valueerror(monkeypatch):
    """D.4 : une panne ValueError répond aussi 500 (depuis D.5)."""
    class ModeleEnPanne:
        def predict(self, text):
            raise ValueError("bug interne")
            
    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", ModeleEnPanne())
        r = client.post("/predict", json={"text": "Bonjour"})
        assert r.status_code == 500
        assert "bug interne" not in r.text