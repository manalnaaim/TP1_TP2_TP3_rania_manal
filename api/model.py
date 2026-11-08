"""Raccord entre l'API et le modèle entraîné au TP2."""
import sys
from pathlib import Path
from typing import TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))

from predict import charger_modele  # noqa: E402
from predict import predict as _predict  # noqa: E402
from api.schemas import Label  # noqa: E402

# Le seuil d'abstention (TP4, étape C.4)
SEUIL_ABSTENTION = 0.60

class Resultat(TypedDict):
    label: Label
    score: float
    text: str

class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""
    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        charger_modele()
        
        # E.3 : Vérification des classes du modèle au démarrage
        import src.predict as predict_module
        if hasattr(predict_module, "MODELE") and hasattr(predict_module.MODELE, "classes_"):
            classes_attendues = {"pos", "neg"}
            classes_modele = set(predict_module.MODELE.classes_)
            if not classes_modele.issubset(classes_attendues):
                raise ValueError(f"Le modèle contient des classes inattendues : {classes_modele}")

    def predict(self, text: str) -> Resultat:
        """Renvoie un résultat typé."""
        r = _predict(text)
        
        label_brut = r["label"].lower()
        if label_brut in ("pos", "positive"):
            label: Label = "POSITIVE"
        elif label_brut in ("neg", "negative"):
            label = "NEGATIVE"
        else:
            label = "INDETERMINE"
            
        score = r["score"]
        if score < SEUIL_ABSTENTION:
            label = "INDETERMINE"

        return {"label": label, "score": score, "text": text[:100]}

def load_model() -> SentimentClassifier:
    return SentimentClassifier()