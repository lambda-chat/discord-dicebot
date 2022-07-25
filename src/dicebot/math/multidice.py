from random import randrange


def roll(face: int, num: int) -> int:
    return sum(randrange(1, face + 1) for _ in range(num))


def roll_by_str(rep: str) -> int:
    raise NotImplementedError
