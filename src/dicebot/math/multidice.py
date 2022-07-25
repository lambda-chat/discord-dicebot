from random import randrange
from re import fullmatch


def roll(num: int, face: int) -> int:
    return sum(randrange(1, face + 1) for _ in range(num))


def parse(expr: str) -> tuple[int, int]:
    match = fullmatch(r"(?P<num>[0-9]+)d(?P<face>[0-9]+)", expr)

    if match:
        num = int(match.group("num"))
        face = int(match.group("face"))
        return num, face
    else:
        raise ValueError(expr)


def roll_by_str(expr: str) -> int:
    num, face = parse(expr)
    return roll(num, face)
