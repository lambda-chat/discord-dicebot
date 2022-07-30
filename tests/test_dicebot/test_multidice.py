from collections.abc import Callable

import pytest

from dicebot.multidice import (
    parse,
    parse_explode,
    roll,
    roll_by_expr,
    roll_explode,
    roll_explode_by_expr,
)


@pytest.mark.parametrize(
    ("num", "face", "condition"),
    [
        (1, 1, lambda res: 1 <= res <= 1),
        (31, 1, lambda res: 31 <= res <= 31),
        (1, 2, lambda res: 1 <= res <= 2),
        (10, 20, lambda res: 10 <= res <= 200),
    ],
)
def test_roll(num: int, face: int, condition: Callable[[int], bool]) -> None:
    assert condition(roll(num, face))


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2d6", (2, 6)),
        ("17D3", (17, 3)),
        ("74d22", (74, 22)),
        ("8D26", (8, 26)),
    ],
)
def test_parse(expr: str, expected: tuple[int, int]) -> None:
    assert parse(expr) == expected


@pytest.mark.parametrize(
    ("expr", "condition"),
    [
        ("1D1", lambda res: 1 <= res <= 1),
        ("1d2", lambda res: 1 <= res <= 2),
        ("25D1", lambda res: 25 <= res <= 25),
        ("20d10", lambda res: 20 <= res <= 200),
    ],
)
def test_roll_by_expr(expr: str, condition: Callable[[int], bool]) -> None:
    assert condition(roll_by_expr(expr))


@pytest.mark.parametrize(
    ("num", "face", "condition"),
    [
        (2, 6, lambda res: 2 <= res),
        (31, 3, lambda res: 31 <= res),
        (1, 2, lambda res: 1 <= res),
        (10, 20, lambda res: 10 <= res),
    ],
)
def test_roll_explode(num: int, face: int, condition: Callable[[int], bool]) -> None:
    assert condition(roll_explode(num, face))


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("2d6e", (2, 6)),
        ("17D3e", (17, 3)),
        ("74d22E", (74, 22)),
        ("8D26E", (8, 26)),
    ],
)
def test_parse_explode(expr: str, expected: tuple[int, int]) -> None:
    assert parse_explode(expr) == expected


@pytest.mark.parametrize(
    ("expr", "condition"),
    [
        ("2D6e", lambda res: 2 <= res),
        ("1d2E", lambda res: 1 <= res),
        ("25D2E", lambda res: 25 <= res),
        ("20d10e", lambda res: 20 <= res),
    ],
)
def test_roll_explode_by_expr(expr: str, condition: Callable[[int], bool]) -> None:
    assert condition(roll_explode_by_expr(expr))
