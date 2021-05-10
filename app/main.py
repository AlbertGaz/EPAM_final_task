"""EPAM FINAL TASK.

Write dialogue sentiment analysis web API.
"""
import pickle
from typing import Tuple

from flask import Flask
from flask import redirect, render_template, request, url_for


app = Flask(__name__)

with open("model_en.bin", "rb") as f_in:
    classifier_en = pickle.load(f_in)

with open("model_ru.bin", "rb") as f_in:
    classifier_ru = pickle.load(f_in)


def detect_language(dialog: str) -> str:
    """Detect language of dialogue."""
    dialog = set(dialog)
    ru_letters = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
    if len(dialog.intersection(ru_letters)):
        return "ru"
    return "en"


def dialog_separator(dialog: str, delimiter: str = "\n") -> Tuple:
    """Separate dialogue by exchanges (replica)."""
    dialog = dialog.split(delimiter)
    first = [
        exchange.strip() for i, exchange in enumerate(dialog) if i % 2 != 0 and exchange
    ]
    second = [
        exchange.strip() for i, exchange in enumerate(dialog) if i % 2 == 0 and exchange
    ]
    return first, second


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    """Home page."""
    if request.method == "POST":
        dlg = request.form["dialog"]
        return redirect(url_for("res", dlg=dlg))
    return render_template("home.html", title="Home")


@app.route("/<dlg>")
def res(dlg: str) -> str:
    """Page of sentiment analysis result."""
    model_result = {"en": classifier_en, "ru": classifier_ru}
    dlg = dialog_separator(dlg)
    all_dlg = dlg[0] + dlg[1]
    tones = []
    for exch in all_dlg:
        tone = model_result[detect_language(exch)](exch)
        tones.append((tone[0]["label"], tone[0]["score"]))
    return render_template("res.html", res=str(list(zip(all_dlg, tones))))


if __name__ == "__main__":
    app.run()
