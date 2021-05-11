import pytest

from app.main import detect_language, dialog_prepare


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


def test_dialog_prepare():
    dlg = """- a
    - b
    - c"""
    actual_result = dialog_prepare(dlg)
    assert actual_result == ["a", "b", "c"]
