"""PARSE DIALOG."""
import re
from typing import Dict, Iterator, List, Optional, Tuple

from app.ml_models import *

RU_PATTERN = "[а-яА-Я]"

NEG = "NEGATIVE"
POS = "POSITIVE"
NEU = "NEUTRAL"
LABL0 = "LABEL_0"
LABL1 = "LABEL_1"
LABL2 = "LABEL_2"


def detect_language(dialog: str) -> str:
    """Detect language of dialog."""
    if re.search(RU_PATTERN, dialog):
        return RU
    return EN


def dialog_prepare(
    dialog: str, delimiter: str = "- ", delimiter2: Optional[str] = None
) -> List:
    """Separate dialogue by exchanges (replica)."""
    dialog = re.split(f"{delimiter}|{delimiter2}", dialog)
    return [exchange.strip() for exchange in dialog if exchange]


def phrases_sentiment_analyser(
    dlg_list: List[str], model_keys: Dict
) -> Optional[List[Tuple]]:
    """Sentiment analysis of every phrase in dialog."""
    tones = []

    for phrase in dlg_list:
        language = detect_language(phrase)
        model = MODELS[language][model_keys[language]]
        tone = model.analyze(phrase)
        label, score = tone[0]["label"], tone[0]["score"]
        label = model.mapping.get(label)
        tones.append((label, score))
    return tones


def float_to_tone(sentiment_number: int) -> str:
    """Convert float number to sentiment class."""
    if not sentiment_number:
        return NEU

    return POS if sentiment_number > 0 else NEG


def dialog_sentiment_analyzer(tones: List) -> Iterator:
    """Count tonality from list of tonalities."""
    mapping = {NEG: -1, NEU: 0, POS: 1}

    sentiment_weights = [
        mapping[label] * score if label in [POS, NEG] and score >= 0.6 else 0
        for label, score in tones
    ]

    usr1_tone = sum(sentiment_weights[::2])
    usr2_tone = sum(sentiment_weights[1::2])
    dlg_tone = sum(sentiment_weights)

    return map(float_to_tone, [usr1_tone, usr2_tone, dlg_tone])
