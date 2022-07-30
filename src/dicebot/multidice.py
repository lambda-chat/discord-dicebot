from random import randrange
from re import fullmatch


def roll(num: int, face: int) -> int:
    """いくつかのダイスを振り，出目の和を返す関数

    Args:
        num (int): ダイスを振る個数
        face (int): ダイスの面の数

    Returns:
        int: ダイスの出目の和
    """
    return sum(randrange(1, face + 1) for _ in range(num))


def parse(expr: str) -> tuple[int, int]:
    """ダイスを振る個数とダイスの面の数を返す関数

    Args:
        expr (str): 標準ダイス表記

    Raises:
        ValueError: 標準ダイス表記に従っていない場合

    Returns:
        tuple[int, int]: ダイスを振る個数，ダイスの面の数
    """
    if match := fullmatch(r"(?P<num>[0-9]+)[dD](?P<face>[0-9]+)", expr):
        num = int(match.group("num"))
        face = int(match.group("face"))
        return num, face
    else:
        raise ValueError(expr)


def roll_by_expr(expr: str) -> int:
    """いくつかのダイスを振り，出目の和を返す関数

    Args:
        expr (str): 標準ダイス表記

    Returns:
        int: ダイスの出目の和
    """
    num, face = parse(expr)
    return roll(num, face)


def roll_exclamation(num: int, face: int, life: int) -> int:
    """いくつかのダイスを振り，最大値が出た場合には追加のダイスを補充し，出目の和を返す関数

    Args:
        num (int): ダイスを振る個数
        face (int): ダイスの面の数
        life (int): 追加されるダイスの最大値

    Returns:
        int: ダイスの出目の和
    """
    result: list = []
    while num > 0:
        new: int = randrange(1, face + 1)
        result.append(new)
        if new == face:
            liferemain: int = life
            while liferemain > 0:
                new = randrange(1, face + 1)
                result.append(new)
                if new == face:
                    liferemain = life
                else:
                    liferemain -= 1
        num -= 1
    print(result)
    return sum(result)


def parse_exclamation(expr: str) -> tuple[int, int]:
    raise NotImplementedError


def roll_exclamation_by_expr(expr: str) -> int:
    raise NotImplementedError
