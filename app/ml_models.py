"""ML MODEL IMPORT."""

from transformers import pipeline


bert_base = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"
)
rurewiew = pipeline(
    "sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment-rurewiews"
)

EN = "en"
RU = "ru"

EN_MODELS = {"nlptown_bert_base": bert_base}
RU_MODELS = {"blanchefort_rurewiews": rurewiew}
MODELS = {EN: EN_MODELS, RU: RU_MODELS}
