from typing import Dict
from client.move import Move
from client.helper_classes import Map, Unit, Units
import enum


class Action(enum.Enum):
    Up = 'Up'
    Down = 'Down'
    Left = 'Left'
    Right = 'Right'
    Mine = 'Mine'
    Attack = 'Attack'
    Breed = 'Breed'
    Stun = ' Stun'


class EvalFns:
    @staticmethod
    def up(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resources: int, turnsLeft: int, paths: Dict, foodPaths: Dict) -> int:
        return 0


evalFns = {
    Action.Up: EvalFns.up
}


class GridPlayer:

    def __init__(self):
        self.bfs = {}
        self.paths

    def validMove(self, unit: Unit, map: Map):

    def evalFn(self, game_map: Map, unit: Unit, action: Action, myUnits: Units, enemyUnits: Units, resources: int, turnsLeft: int):
        # start with mining I guess
        switch

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:
        return [None]
