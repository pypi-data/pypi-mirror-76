# -*- coding: utf-8 -*-
from argparse import ArgumentParser

from snregales.classes.abstract.parser import AbstractParser


class DDDiceRollerParser(AbstractParser):
    """Dungeons and Dragons Dice Roller Parser,

    only args and parser properties are publicly accessable,
    property value parser can be called to retrieve the DDDiceRoller argparse.ArgumentParser
    property value args can be called to retrieve parsed sys.args
    """

    def __init__(self) -> None:
        super(DDDiceRollerParser, self).__init__(
            prog="dddice_roller",
            usage="Dice roller for Dungeon and Dragons",
            description="Given an DnD dice instruction set, 'dddice_roller' will return a dice roll result set",
            epilog="4d6b3+1 -> { 'instruction': '4d6b3+1', 'modifier': 1, 'picks': (5,5,4), 'rolls': [4,1,5,5], 'value': 15 }",
        )

    def _required_arguments(self, group) -> None:
        group.add_argument(
            "instructions",
            nargs="+",
            help="dice roll instructions example: 4d6b3+2 -> roll 4 6 sided dice choose the best 3 and modify roll by 2",
        )
