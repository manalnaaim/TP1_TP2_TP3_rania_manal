"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de sentiment_app, qui charge models/sentiment.joblib une seule fois.
"""
from typing import TypedDict

from api.schemas import Label
from sentiment_app.predict import charger_modele
from sentiment_app.predict import predict as _predict

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
        
        import sentiment_app.predict as predict_module
        if hasattr(predict_module, "MODELE") and hasattr(predict_module.MODELE, "classes_"):
            classes_attendues = {"pos", "neg"}
            classes_modele = set(predict_module.MODELE.classes_)
            if not classes_modele.issubset(classes_attendues):
                raise ValueError(f"Le modèle contient des classes inattendues : {classes_modele}")

    def predict(self, text: str) -> Resultat:
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