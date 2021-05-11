import os

import pytest

from app.main import (
    detect_language,
    dialog_prepare,
    dialog_sentiment_analyzer,
    phrases_sentiment_analyser,
    phrases_tones_for_display,
)

os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    ("arg", "res"),
    [
        ("Привет", "ru"),
        ("Hello", "en"),
        ("ПриветHello", "ru"),
        ("", "en"),
        ("123", "en"),
        (
            "If there is any russian letter it would be russian. For example here is ф",
            "ru",
        ),
    ],
)
def test_detect_language(arg, res):
    actual_result = detect_language(arg)
    assert actual_result == res


def test_dialog_prepare_without_delimiter():
    arg = """- a
    - b
    - c
    - d
    - e"""
    actual_result = dialog_prepare(arg)
    assert actual_result == ["a", "b", "c", "d", "e"]


def test_dialog_prepare_with_delimiter():
    delimiter = "Albert:"
    delimier2 = "Teacher:"
    arg = """Albert: Hello! Here is my HW
    Teacher: Hi. It is bullshit!
    Albert: OKE"""
    actual_result = dialog_prepare(arg, delimiter=delimiter, delimiter2=delimier2)
    assert actual_result == ["Hello! Here is my HW", "Hi. It is bullshit!", "OKE"]


@pytest.mark.parametrize(
    ("arg", "res"),
    [
        (["Hello", "Hi"], ["NEUTRAL", "NEUTRAL"]),
        (["Hate", "What?", "Very tried"], ["NEGATIVE", "NEUTRAL", "NEUTRAL"]),
        (["Today I am very happy"], ["POSITIVE"]),
    ],
)
def test_phrases_sentiment_analyser(arg, res):
    tones = phrases_sentiment_analyser(arg)
    actual_result = [label for label, _ in tones]
    assert actual_result == res


@pytest.mark.parametrize(
    ("arg", "res"),
    [
        (
            [("NEUTRAL", 100), ("POSITIVE", 80), ("NEUTRAL", 79)],
            ["NEUTRAL", "POSITIVE", "POSITIVE"],
        ),
        ([], ["NEUTRAL", "NEUTRAL", "NEUTRAL"]),
        ([("POSITIVE", 100), ("NEGATIVE", 100)], ["POSITIVE", "NEGATIVE", "NEUTRAL"]),
    ],
)
def test_dialog_sentiment_analyzer(arg, res):
    actual_result = dialog_sentiment_analyzer(arg)
    assert list(actual_result) == res


def test_phrases_tones_for_display():
    dlg_list = ["Hi", "Hello"]
    tones = [("NEUTRAL", 100), ("NEUTRAL", 100)]
    actual_result = phrases_tones_for_display(dlg_list, tones)
    assert actual_result == "Hi NEUTRAL 100<br />Hello NEUTRAL 100"
