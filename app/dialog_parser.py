"""PARSE DIALOG."""
import re
from typing import Iterator, List, Optional, Tuple

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


def phrases_sentiment_analyser(dlg_list: List[str]) -> List[Tuple]:
    """Sentiment analysis of every phrase in dialog."""
    tones = []
    mapping = {
        LABL0: NEG,
        LABL1: NEU,
        LABL2: POS,
        NEG: NEG,
        NEU: NEU,
        POS: POS,
    }
    for phrase in dlg_list:
        tone = MODELS[detect_language(phrase)](phrase)
        label, score = tone[0]["label"], tone[0]["score"]
        label = mapping.get(label)
        tones.append((label, score))
    return tones


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

    return map(
        lambda x: POS if x > 0 else NEG if x != 0 else NEU,
        [usr1_tone, usr2_tone, dlg_tone],
    )
