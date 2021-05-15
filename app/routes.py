"""APP ROUTES."""
import os

from flask import Markup
from flask import redirect, render_template, request, send_from_directory, url_for

from app import app
from app.dialog_parser import *


def phrases_tones_for_display(dlg_list: List, tones: List) -> str:
    """Prepare display of phrases and tones on page."""
    tones_for_display = []
    for phrase, tone in zip(dlg_list, tones):
        tones_for_display.append(f"{phrase} {tone[0]} {round(tone[1], 2)}")

    out = "<br />".join(tones_for_display)
    return Markup(out)


@app.route("/favicon.ico")
def favicon() -> str:
    """Browser get favicon."""
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    """Home page."""
    if request.method == "POST":
        dlg = request.form["dialog"]
        delimiter = request.form["delimiter"]
        delimiter2 = request.form["delimiter2"]
        model_en = request.form["model_en"]
        model_ru = request.form["model_ru"]
        return redirect(
            url_for(
                "res",
                dlg=dlg,
                delimiter=delimiter,
                delimiter2=delimiter2,
                model_en=model_en,
                model_ru=model_ru,
            )
        )
    return render_template(
        "home.html", title="Home", EN_MODELS=EN_MODELS, RU_MODELS=RU_MODELS
    )


@app.route("/<dlg>")
def res(dlg: str) -> str:
    """Page of sentiment analysis result."""
    delimiter = request.args.get("delimiter")
    delimiter = r"- " if not delimiter else delimiter

    delimiter2 = request.args.get("delimiter2")
    delimiter2 = None if not delimiter2 else delimiter2

    model_en = request.args.get("model_en")
    model_ru = request.args.get("model_ru")
    model_keys = {EN: model_en, RU: model_ru}

    dlg_list = dialog_prepare(dlg, delimiter=delimiter, delimiter2=delimiter2)

    tones = phrases_sentiment_analyser(dlg_list, model_keys=model_keys)
    usr1_tone, usr2_tone, dlg_tone = dialog_sentiment_analyzer(tones)

    out = phrases_tones_for_display(dlg_list, tones)

    return render_template(
        "res.html", res=out, usr1_tone=usr1_tone, usr2_tone=usr2_tone, dlg_tone=dlg_tone
    )
