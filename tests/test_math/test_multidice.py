from collections.abc import Callable

import pytest

from dicebot.math.multidice import roll, roll_by_str


@pytest.mark.parametrize(
    ("num", "face", "condition"),
    [
        (1, 1, lambda res: 1 <= res <= 1),
        (31, 1, lambda res: 31 <= res <= 31),
        (1, 2, lambda res: 1 <= res <= 2),
        (10, 20, lambda res: 10 <= res <= 200),
    ],
)
def test_roll(num: int, face: int, condition: Callable[[int], bool]):
    assert condition(roll(num, face))


@pytest.mark.parametrize(
    ("rep", "condition"),
    [
        ("1d1", lambda res: 1 <= res <= 1),
        ("1d2", lambda res: 1 <= res <= 2),
        ("25d1", lambda res: 25 <= res <= 25),
        ("20d10", lambda res: 20 <= res <= 200),
    ],
)
def test_roll_by_str(rep: str, condition: Callable[[int], bool]):
    assert condition(roll_by_str(rep))
