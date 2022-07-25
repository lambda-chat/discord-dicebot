from collections.abc import Callable

import pytest

from dicebot.math.multidice import roll, roll_by_str


@pytest.mark.parametrize(
    ("face", "num", "condition"),
    [
        (1, 1, lambda res: 1 <= res <= 1),
        (2, 1, lambda res: 1 <= res <= 2),
    ],
)
def test_roll(face: int, num: int, condition: Callable[[int], bool]):
    assert condition(roll(face, num))


@pytest.mark.parametrize(
    ("rep", "condition"),
    [
        ("1d1", lambda res: 1 <= res <= 1),
        ("2d1", lambda res: 1 <= res <= 2),
    ],
)
def test_roll_by_str(rep: str, condition: Callable[[int], bool]):
    assert condition(roll_by_str(rep))
