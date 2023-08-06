# -*- coding: utf-8 -*-
import random
import re
import typing as t

from . import (
    BEST,
    DIE,
    DIE_GROUP,
    MODIFIER,
    MODIFIER_DEFAULT,
    MODIFIER_GROUP,
    PICKS,
    PICK_DEFAULT,
    PICK_GROUP,
    QUALITY_GROUP,
    QUANTITY,
    QUANTITY_DEFAULT,
    QUANTITY_GROUP,
    QUOTA,
    QUOTA_GROUP,
    ROLLS,
    RollInstruction,
)


# def pick_instruction_parser(match: re.Match):
def pick_instruction_parser(match: re.Match):
    """Conditional parse of the instruction string's pick section.

    :param match: regular expression match of instruction string
    :type match: re.Match
    :raises ValueError: pick > dices to be rolled
    :return: quality (best or worst) roll and quota
    :rtype: Dict[str, Union[str, int]]
    """
    print(type(match))
    if match.group(PICK_GROUP) is None:
        return PICK_DEFAULT
    if int(match.group(QUOTA_GROUP)) > int(
        match.group(QUANTITY_GROUP) or QUANTITY_DEFAULT
    ):
        raise ValueError("Pick quota cannot be greater than roll quantity")
    return {
        BEST: match.group(QUALITY_GROUP).lower() == BEST[0],
        QUOTA: int(match.group(QUOTA_GROUP)),
    }


# TODO: conditional re for quota
def instruction_parser(instruction: str) -> RollInstruction:
    """Parse a Dungeons and Drangons (DnD) DiceRoll instruction into its individual components.

    :param instruction: DnD roll instruction
    :type instruction: str
    :return: {roll:{quantity, die}, pick:{best, quota}, modifier}
    :rtype: Tuple[Dict[str, Union[int, bool]], Dict[str, int], int]
    """
    pattern: str = r"^(\d+)?([dD](4|6|8|100|10|12|20))(([bB]|[wW])(\d+))?([+-]\d+)?$"
    if match := re.match(pattern=pattern, string=instruction):
        return (
            {
                QUANTITY: int(match.group(QUANTITY_GROUP) or QUANTITY_DEFAULT),
                DIE: int(match.group(DIE_GROUP)),
            },
            pick_instruction_parser(match=match),
            int(match.group(MODIFIER_GROUP) or MODIFIER_DEFAULT),
        )
    raise ValueError(f"'{instruction}' is not an applicable dice roll instruction")


def __roll_100() -> str:
    return int("".join(map(str, roll_dices(quantity=2, die=9, zero=True)))) or 100


def roll_dices(*, quantity: int, die: int, zero: bool = False) -> t.List[int]:
    """Roll a dice type quantity amount of time

    Given an dice with certian amount of sides,
    with each side representing a unique integer value
    ranging from 1 to the die side amount.
    Randomly pick a side, Do this N amount of times.

    :param quantity: the amount of dice to roll.
    :type quantity: int
    :param die: what sided dice to roll
    :type die: int
    :param zero: allow a value side in a dice, defaults to False
    :type zero: bool, Optional
    :return: all dice roll values
    :rtype: List[int]
    """
    return [
        __roll_100() if die == 100 else random.randint(0 if zero else 1, die)
        for _ in range(quantity)
    ]


def cherrypick_roll(*, rolls: t.List[int], best: bool, quota: int) -> tuple:
    """Given a list dice roll results, order and cherrypick them.

    If quota is the same as the list dice roll results, than return ordered form of the list.

    :param rolls: List of dice roll values
    :type rolls: List[int]
    :param best: Cherrypick the best values?
    :type best: bool
    :param quota: how many values will be cherrypicked
    :type quota: int
    :return: cherrypicked values
    :rtype: tuple
    """
    if quota > len(rolls):
        raise ValueError(f"Quota > len(rolls) -> {quota} > {rolls}")
    if not rolls:
        raise ValueError("Cannot cherrypick from an empty list")

    total_rolls: int = len(rolls)

    if not quota:
        quota = total_rolls

    if total_rolls <= 2:
        return tuple(rolls[:quota])

    ordered_dice_rolls: t.List[int] = sorted(rolls, reverse=best)
    return tuple(ordered_dice_rolls[:quota])
