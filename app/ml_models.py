"""ML MODEL IMPORT."""

from typing import Tuple

from transformers import pipeline


EN = "en"
RU = "ru"


class MLModel:
    """This is a parent class that is intended to be inherited by other classes."""

    def analyze(self, dlg: str) -> Tuple:
        """Sentiment analyzer."""
        raise NotImplementedError


class ML1(MLModel):
    """Cardiffnlp twitter model."""

    def __init__(self):
        self.bert_base = pipeline(
            "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
        )
        self.mapping = {
            "LABEL_0": "NEGATIVE",
            "LABEL_1": "NEUTRAL",
            "LABEL_2": "POSITIVE",
        }

    def analyze(self, dlg: str) -> Tuple:
        """Sentiment analyzer."""
        return self.bert_base(dlg)


class ML2(MLModel):
    """Blanchefort rereviews sentiment model."""

    def __init__(self):
        self.rurewiew = pipeline(
            "sentiment-analysis",
            model="blanchefort/rubert-base-cased-sentiment-rurewiews",
        )
        self.mapping = {
            "NEGATIVE": "NEGATIVE",
            "NEUTRAL": "NEUTRAL",
            "POSITIVE": "POSITIVE",
        }

    def analyze(self, dlg: str) -> Tuple:
        """Sentiment analyzer."""
        return self.rurewiew(dlg)


EN_MODELS = {"nlptown_bert_base": ML1()}
RU_MODELS = {"blanchefort_rurewiews": ML2()}

MODELS = {EN: EN_MODELS, RU: RU_MODELS}
