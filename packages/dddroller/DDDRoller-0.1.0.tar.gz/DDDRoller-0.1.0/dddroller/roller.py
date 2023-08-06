# -*- coding: utf-8 -*-
import typing as t

from . import (
    INSTRUCTION,
    MODIFIER,
    PICKS,
    ROLLS,
    VALUE,
)
from .utilities import (
    instruction_parser,
    cherrypick_roll,
    roll_dices,
)


class DiceRoll:
    """Create a Dice roll object with a specific instruction.

    (Re)roll object by calling the DiceRoll instance object as a function.
    Publically accessable values are instruction, is_rolled, rolls, picks, modifier, value
    """

    def __init__(self, instruction: str):
        self.__str_instruction: str = instruction
        (
            self.__roll_instruction,
            self.__pick_instruction,
            self.__modifier,
        ) = instruction_parser(self.__str_instruction)

    def __call__(self) -> "DiceRoll":
        self.__rolls = roll_dices(**self.__roll_instruction)
        self.__picks = cherrypick_roll(rolls=self.__rolls, **self.__pick_instruction)
        return self

    def __str__(self) -> str:
        return f"{self.__str_instruction}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.__str__()!r})>"

    def __gt__(self, other) -> bool:
        return self.value.__gt__(self.__validate_other(other, ">"))

    def __ge__(self, other):
        return self.value.__ge__(self.__validate_other(other, ">="))

    def __lt__(self, other) -> bool:
        return self.value.__lt__(self.__validate_other(other, "<"))

    def __le__(self, other):
        return self.value.__le__(self.__validate_other(other, "<="))

    def __eq__(self, other) -> bool:
        return self.value.__eq__(self.__validate_other(other, "=="))

    def __validate_other(self, other: t.Any, message: str) -> int:
        if not (isinstance(other, self.__class__) or isinstance(other, int)):
            raise TypeError(
                f"{message} is not supported between {self.__class__} and {type(other)}"
            )
        if isinstance(other, self.__class__):
            return self.__validate_roll(other)
        return other

    def __validate_roll(self, other: "DiceRoll") -> int:
        if not other.is_rolled:
            raise ValueError(f"{other} is not rolled, please roll before comparing")
        return other.value

    @property
    def is_rolled(self) -> bool:
        return self.value > self.modifier

    @property
    def instruction(self) -> str:
        return self.__str_instruction

    @property
    def picks(self) -> tuple:
        return getattr(self, "_DiceRoll__picks", ())

    @property
    def rolls(self) -> list:
        return getattr(self, "_DiceRoll__rolls", [])

    @property
    def modifier(self) -> int:
        return getattr(self, "_DiceRoll__modifier", 0)

    @property
    def value(self) -> int:
        return sum(self.picks) + self.modifier
