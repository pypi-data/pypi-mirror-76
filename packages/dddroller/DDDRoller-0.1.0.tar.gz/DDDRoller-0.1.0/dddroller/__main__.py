#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing as t

from .parser import DDDiceRollerParser
from .roller import DiceRoll

args = DDDiceRollerParser().args
try:
    from pprint import pprint

    for roll in list(map(DiceRoll, args.instructions)):
        roll()
        pprint(
            {
                "instruction": roll.instruction,
                "rolls": roll.rolls,
                "picks": roll.picks,
                "modifier": roll.modifier,
                "value": roll.value,
            },
            indent=2,
        )
except ValueError as ve:
    print(ve)

    # <dice type> example: d6
    # <dice type><modifier> example: d6-1
    # <dice quantity><dice type> example: 2d6
    # <dice quantity><dice type><modifier> example: 2d6-1
    # <dice quantity><dice type><(best|worst)pick> example: 4d6b3
    # <dice quantity><dice type><(best|worst)pick><modifier> example: 4d6w3+1
