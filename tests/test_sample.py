import pytest  # NOQA

from dicebot.sample import hello


def test_hello() -> None:
    assert hello() == "Hello World!"
