# -*- coding: utf-8 -*-
import typing as t


__version__ = "0.2.0"

PickInstruction = t.Dict[str, t.Union[int, bool]]
DiceInstruction = t.Dict[str, int]
RollInstruction = t.Tuple[PickInstruction, DiceInstruction, int]


QUANTITY_GROUP: int = 1
DIE_GROUP: int = 3
MODIFIER_GROUP: int = 7
QUANTITY_DEFAULT: int = 1
MODIFIER_DEFAULT: int = 0
QUOTA_GROUP: int = 6
QUALITY_GROUP: int = 5
PICK_GROUP: int = 4
QUANTITY: str = "quantity"
DIE: str = "die"
MODIFIER: str = "modifier"
ROLLS: str = "rolls"
QUOTA: str = "quota"
BEST: str = "best"
PICK_DEFAULT: int = {BEST: True, QUOTA: 0}
PICKS: str = "picks"
BEST: str = "best"
VALUE: str = "value"
INSTRUCTION: str = "instruction"
