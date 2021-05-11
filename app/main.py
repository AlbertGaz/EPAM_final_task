"""EPAM FINAL TASK.

Write dialog sentiment analysis web API.
"""
import os
import pickle
import re
from typing import List, Optional

from flask import Flask, Markup
from flask import redirect, render_template, request, url_for

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
model_en = os.path.join(dir_path, "model_cardiffnlp_en.bin")
model_ru = os.path.join(dir_path, "model_blanchefort_ru.bin")

with open(model_en, "rb") as f_in:
    classifier_en = pickle.load(f_in)

with open(model_ru, "rb") as f_in:
    classifier_ru = pickle.load(f_in)


def detect_language(dialog: str) -> str:
    """Detect language of dialog."""
    dialog = set(dialog)
    ru_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    if len(dialog.intersection(ru_letters)):
        return "ru"
    return "en"


def dialog_prepare(
    dialog: str, delimiter: str = "- ", delimiter2: Optional[str] = None
) -> List:
    """Separate dialogue by exchanges (replica)."""
    dialog = re.split(f"{delimiter}|{delimiter2}", dialog)
    return [exchange.strip() for exchange in dialog if exchange]


def sentiment_analyzer(tones: List) -> str:
    """Count tonality from list of tonalities."""
    mapping = {"NEGATIVE": -1, "NEUTRAL": 0, "POSITIVE": 1}
    exchange_tone = 0
    for label, score in tones:
        label = mapping[label]
        exchange_tone += label * score if score >= 0.7 else 0
    return (
        "POSITIVE"
        if exchange_tone > 0
        else "NEGATIVE"
        if exchange_tone != 0
        else "NEUTRAL"
    )


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
    delimiter2 = request.args.get("delimiter2")

    if not delimiter:
        delimiter = r"- "
    if not delimiter2:
        delimiter2 = None

    model_result = {"en": classifier_en, "ru": classifier_ru}

    dlg_list = dialog_prepare(dlg, delimiter=delimiter, delimiter2=delimiter2)

    tones = []
    tones_out = []
    mapping = {
        "LABEL_0": "NEGATIVE",
        "LABEL_1": "NEUTRAL",
        "LABEL_2": "POSITIVE",
        "NEGATIVE": "NEGATIVE",
        "NEUTRAL": "NEUTRAL",
        "POSITIVE": "POSITIVE",
    }
    for exchange in dlg_list:
        tone = model_result[detect_language(exchange)](exchange)
        label, score = tone[0]["label"], tone[0]["score"]
        label = mapping.get(label)
        tones.append((label, score))
        tones_out.append(
            f"{exchange} <span style='color': ##808000;'>{label}</span> {round(score, 2)}"
        )

    out = "<br />".join(map(str, tones_out))
    out = Markup(out)

    usr1 = tones[::2]
    usr2 = tones[1::2]

    usr1_tone = sentiment_analyzer(usr1)
    usr2_tone = sentiment_analyzer(usr2)
    dlg_tone = sentiment_analyzer(tones)

    return render_template(
        "res.html", res=out, usr1_tone=usr1_tone, usr2_tone=usr2_tone, dlg_tone=dlg_tone
    )


if __name__ == "__main__":
    app.run()
