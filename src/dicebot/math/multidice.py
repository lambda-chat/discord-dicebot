from random import randrange


def roll(face: int, num: int) -> int:
    multiroll = 0

    for _ in range(num):
        singleroll = randrange(1, face + 1)
        multiroll += singleroll

    return multiroll


def roll_by_str(rep: str) -> int:
    raise NotImplementedError
