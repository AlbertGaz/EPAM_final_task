"""EPAM FINAL TASK.

Write dialog sentiment analysis web API.
"""
import os
import pickle
import re
from typing import Iterator, List, Optional, Tuple

from flask import Flask, Markup
from flask import redirect, render_template, request, url_for

app = Flask(__name__)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_EN_DIR = os.path.join(DIR_PATH, "model_cardiffnlp_en.bin")
MODEL_RU_DIR = os.path.join(DIR_PATH, "model_blanchefort_ru.bin")

EN = "en"
RU = "ru"

RU_LETTERS = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"

NEG = "NEGATIVE"
POS = "POSITIVE"
NEU = "NEUTRAL"
LABL0 = "LABEL_0"
LABL1 = "LABEL_1"
LABL2 = "LABEL_2"

MODELS = {}

with open(MODEL_EN_DIR, "rb") as f_in:
    MODELS[EN] = pickle.load(f_in)

with open(MODEL_RU_DIR, "rb") as f_in:
    MODELS[RU] = pickle.load(f_in)


def detect_language(dialog: str) -> str:
    """Detect language of dialog."""
    dialog = set(dialog)
    ru_letters = RU_LETTERS
    if len(dialog.intersection(ru_letters)):
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


def phrases_tones_for_display(dlg_list: List, tones: List) -> str:
    """Prepare display of phrases and tones on page."""
    tones_for_display = []
    for phrase, tone in zip(dlg_list, tones):
        tones_for_display.append(f"{phrase} {tone[0]} {round(tone[1], 2)}")

    out = "<br />".join(tones_for_display)
    return Markup(out)


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    """Home page."""
    if request.method == "POST":
        dlg = request.form["dialog"]
        delimiter = request.form["delimiter"]
        delimiter2 = request.form["delimiter2"]
        return redirect(
            url_for("res", dlg=dlg, delimiter=delimiter, delimiter2=delimiter2)
        )
    return render_template("home.html", title="Home")


@app.route("/<dlg>")
def res(dlg: str) -> str:
    """Page of sentiment analysis result."""
    delimiter = request.args.get("delimiter")
    delimiter = r"- " if not delimiter else delimiter

    delimiter2 = request.args.get("delimiter2")
    delimiter2 = None if not delimiter2 else delimiter2

    dlg_list = dialog_prepare(dlg, delimiter=delimiter, delimiter2=delimiter2)

    tones = phrases_sentiment_analyser(dlg_list)
    usr1_tone, usr2_tone, dlg_tone = dialog_sentiment_analyzer(tones)

    out = phrases_tones_for_display(dlg_list, tones)

    return render_template(
        "res.html", res=out, usr1_tone=usr1_tone, usr2_tone=usr2_tone, dlg_tone=dlg_tone
    )


if __name__ == "__main__":
    app.run()
