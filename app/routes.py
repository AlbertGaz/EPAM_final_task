"""APP ROUTES."""
from flask import Markup
from flask import redirect, render_template, request, url_for

from app import app
from app.dialog_parser import *


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
