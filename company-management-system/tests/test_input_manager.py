from utils.input_manager import Input
from pytest import MonkeyPatch
import pytest


def test_type_float(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("builtins.input", lambda _: "5")
    key = "n"
    input_manager = Input(key, float, float, "")
    assert input_manager.try_till_get().get(key) == float("5")


def test_quit(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    im = Input("number", int, int, "")

    with pytest.raises(SystemExit) as e:
        im.try_till_get(True)
        assert e.type == SystemExit


def test_trying_on_wrong_data(monkeypatch: MonkeyPatch):
    data = ["name", 8]
    monkeypatch.setattr("builtins.input", lambda _: data.pop(0))
    im = Input("number", int, int, "")
    assert im.try_till_get().get("number") == 8
