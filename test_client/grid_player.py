from typing import Dict, List
from move import Move
from helper_classes import Map, Unit, Units
import enum
import random

# GENERAL HELPERS


class Action(enum.Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    MINE = 'MINE'
    ATK = 'ATK'
    BREED_WORKER = 'BREED_WORKER'
    BREED_WARRIOR = 'BREED_WARRIOR'
    STUN = 'STUN'


DIRECTIONS = {Action.UP: (0, -1),
              Action.DOWN: (0, 1),
              Action.RIGHT: (1, 0),
              Action.LEFT: (-1, 0)}


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def unitsInFOV(unit: Unit,  myUnits: Units, enemyUnits: Units):
    workers = []
    warriors = []
    enemyWarriors = []
    enemyWorkers = []
    for worker in myUnits.get_all_unit_of_type('worker'):
        dist = distance(unit.position(), worker.position())
        if dist <= 4 and dist != 0:
            workers.append(worker)
    for warrior in myUnits.get_all_unit_of_type('melee'):
        dist = distance(unit.position(), warrior.position())
        if dist <= 4:
            warriors.append(warrior)
    for evilWorker in enemyUnits.get_all_unit_of_type('worker'):
        if distance(unit.position(), evilWorker.position()) <= 4:
            enemyWorkers.append(evilWorker)
    for evilWarrior in enemyUnits.get_all_unit_of_type('melee'):
        if distance(unit.position(), evilWarrior.position()) <= 4:
            enemyWarriors.append(evilWarrior)
    return workers, warriors, enemyWorkers, enemyWarriors


def closestUntapped(unit: Unit, resources: List, myUnits: Units, foodPaths: Dict, bfs, offset=0, inverse=False):
    sortedFood = []
    if unit.position() in foodPaths:
        sortedFood = foodPaths[unit.position()]
    else:
        sortedFood = sorted(resources, key=lambda position: bfs(
            position, unit.position()), reverse=inverse)
        foodPaths[unit.position()] = sortedFood
    workers = myUnits.get_all_unit_of_type('worker')
    for food in sortedFood:
        isBusy = False
        for worker in workers:
            if not distance(food, worker.position()):
                isBusy = True
                break
        if (not isBusy) and not offset:
            return food
        elif (not isBusy) and offset:
            offset -= 1
    return sortedFood[0]


# WORKER STUFF
class EvalFnsWorker:
    @staticmethod
    def up(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
           turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            closestMine = closestUntapped(
                unit, resources, myUnits, foodPaths, bfs)
            newPos = (unit.position()[0], unit.position()[1] - 1)
            if not len(nearbyEnemyWorkers):
                return bfs(closestMine, newPos)
            else:
                myDis = bfs(closestMine, newPos)
                for enemy in nearbyEnemyWorkers:
                    if myDis > bfs(enemy.position(), closestMine):
                        return bfs(closestUntapped(unit, resources, myUnits, foodPaths, bfs, 1), newPos)
                return myDis

        else:
            return 10005
            # engage expectimax

    @staticmethod
    def down(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            closestMine = closestUntapped(
                unit, resources, myUnits, foodPaths, bfs)
            newPos = (unit.position()[0], unit.position()[1] + 1)
            if not len(nearbyEnemyWorkers):
                return bfs(closestMine, newPos)
            else:
                myDis = bfs(closestMine, newPos)
                for enemy in nearbyEnemyWorkers:
                    if myDis > bfs(enemy.position(), closestMine):
                        return bfs(closestUntapped(unit, resources, myUnits, foodPaths, bfs, 1), newPos)
                return myDis

        else:
            return 10004
            # engage expectimax

    @staticmethod
    def right(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
              turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            closestMine = closestUntapped(
                unit, resources, myUnits, foodPaths, bfs)
            newPos = (unit.position()[0]+1, unit.position()[1])
            if not len(nearbyEnemyWorkers):
                return bfs(closestMine, newPos)
            else:
                myDis = bfs(closestMine, newPos)
                for enemy in nearbyEnemyWorkers:
                    if myDis > bfs(enemy.position(), closestMine):
                        return bfs(closestUntapped(unit, resources, myUnits, foodPaths, bfs, 1), newPos)
                return myDis

        else:
            return 10006
            # engage expectimax

    @staticmethod
    def left(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            closestMine = closestUntapped(
                unit, resources, myUnits, foodPaths, bfs)
            newPos = (unit.position()[0]-1, unit.position()[1])
            if not len(nearbyEnemyWorkers):
                return bfs(closestMine, newPos)
            else:
                myDis = bfs(closestMine, newPos)
                for enemy in nearbyEnemyWorkers:
                    if myDis > bfs(enemy.position(), closestMine):
                        return bfs(closestUntapped(unit, resources, myUnits, foodPaths, bfs, 1), newPos)
                return myDis
        else:
            return 10001
            # engage expectimax

    @staticmethod
    def mine(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            return -35
        else:
            return 10002
            # engage expectimax

    @staticmethod
    def breedWorker(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
                    turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            if len(myUnits.get_all_unit_of_type('worker')) > len(myUnits.get_all_unit_of_type('melee')):
                return 1000
            return -50
        else:
            return 10003
            # engage expectimax

    @staticmethod
    def breedWarrior(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
                     turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        if not len(nearbyEnemyWarriors):
            if len(myUnits.get_all_unit_of_type('worker')) < len(myUnits.get_all_unit_of_type('melee')):
                return 1000
            return -100
        else:
            return 10004
            # engage expectimax


evalFnsWorker = {
    Action.UP: EvalFnsWorker.up,
    Action.DOWN: EvalFnsWorker.down,
    Action.LEFT: EvalFnsWorker.left,
    Action.RIGHT: EvalFnsWorker.right,
    Action.BREED_WORKER: EvalFnsWorker.breedWorker,
    Action.BREED_WARRIOR: EvalFnsWorker.breedWarrior,
    Action.MINE: EvalFnsWorker.mine
}
actionToMove = {
    Action.UP: lambda unit: unit.move('UP'),
    Action.DOWN: lambda unit: unit.move('DOWN'),
    Action.LEFT: lambda unit: unit.move('LEFT'),
    Action.RIGHT: lambda unit: unit.move('RIGHT'),
    Action.BREED_WORKER: lambda unit: unit.duplicate(['UP', 'DOWN', 'LEFT', 'RIGHT'][random.randint(0, 3)], 'worker'),
    Action.BREED_WARRIOR: lambda unit: unit.duplicate(['UP', 'DOWN', 'LEFT', 'RIGHT'][random.randint(0, 3)], 'melee'),
    Action.MINE: lambda unit: unit.mine(),
}

# MELEE STUFF


class EvalFnsWarrior:
    @staticmethod
    def up(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
           turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        newPos = (unit.position()[0], unit.position()[1]-1)
        if not (len(nearbyEnemyWarriors) + len(nearbyEnemyWorkers)):
            if unit.id in ongoingGoal:
                myDist = bfs(ongoingGoal[unit.id], newPos)
                if myDist < 4:
                    del ongoingGoal[unit.id]
                    return 100
                else:
                    return myDist
            else:
                allPlaces = map.find_all_resources()
                randomMine = allPlaces[random.randint(0, len(allPlaces)-1)]
                ongoingGoal[unit.id] = randomMine
                return bfs(randomMine, newPos)
        else:
            if len(nearbyEnemyWarriors):
                # assume the closest baddie for now, should be smarter tho
                return -20 + bfs(nearbyEnemyWarriors[0], newPos) + 30*(bfs(nearbyEnemyWarriors[0], newPos) % 2)
            else:
                return -20 + bfs(nearbyEnemyWorkers[0], newPos)
            # engage expectimax

    @staticmethod
    def down(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        newPos = (unit.position()[0], unit.position()[1]+1)
        if not (len(nearbyEnemyWarriors) + len(nearbyEnemyWorkers)):
            if unit.id in ongoingGoal:
                myDist = bfs(ongoingGoal[unit.id], newPos)
                if myDist < 4:
                    del ongoingGoal[unit.id]
                    return 100
                else:
                    return myDist
            else:
                allPlaces = map.find_all_resources()
                randomMine = allPlaces[random.randint(0, len(allPlaces)-1)]
                ongoingGoal[unit.id] = randomMine
                return bfs(randomMine, newPos)
        else:
            if len(nearbyEnemyWarriors):
                # assume the closest baddie for now, should be smarter tho
                return -20 + bfs(nearbyEnemyWarriors[0], newPos) + 30*(bfs(nearbyEnemyWarriors[0], newPos) % 2)
            else:
                return -20 + bfs(nearbyEnemyWorkers[0], newPos)
            # engage expectimax

    @staticmethod
    def right(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
              turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        newPos = (unit.position()[0]+1, unit.position()[1])
        if not (len(nearbyEnemyWarriors) + len(nearbyEnemyWorkers)):
            if unit.id in ongoingGoal:
                myDist = bfs(ongoingGoal[unit.id], newPos)
                if myDist < 4:
                    del ongoingGoal[unit.id]
                    return 100
                else:
                    return myDist
            else:
                allPlaces = map.find_all_resources()
                randomMine = allPlaces[random.randint(0, len(allPlaces)-1)]
                ongoingGoal[unit.id] = randomMine
                return bfs(randomMine, newPos)
        else:
            if len(nearbyEnemyWarriors):
                # assume the closest baddie for now, should be smarter tho
                return -20 + bfs(nearbyEnemyWarriors[0], newPos) + 30*(bfs(nearbyEnemyWarriors[0], newPos) % 2)
            else:
                return -20 + bfs(nearbyEnemyWorkers[0], newPos)
            # engage expectimax

    @staticmethod
    def left(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        nearbyWorkers, nearbyWarriors, nearbyEnemyWorkers, nearbyEnemyWarriors = unitsInFOV(
            unit, myUnits, enemyUnits)
        newPos = (unit.position()[0]-1, unit.position()[1])
        if not (len(nearbyEnemyWarriors) + len(nearbyEnemyWorkers)):
            if unit.id in ongoingGoal:
                myDist = bfs(ongoingGoal[unit.id], newPos)
                if myDist < 4:
                    del ongoingGoal[unit.id]
                    return 100
                else:
                    return myDist
            else:
                allPlaces = map.find_all_resources()
                randomMine = allPlaces[random.randint(0, len(allPlaces)-1)]
                ongoingGoal[unit.id] = randomMine
                return bfs(randomMine, newPos)
        else:
            if len(nearbyEnemyWarriors):
                # assume the closest baddie for now, should be smarter tho
                return -20 + bfs(nearbyEnemyWarriors[0], newPos) + 30*(bfs(nearbyEnemyWarriors[0], newPos) % 2)
            else:
                return -20 + bfs(nearbyEnemyWorkers[0], newPos)
            # engage expectimax

    @staticmethod
    def attack(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
               turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        # just so its aggressive
        return -100

    @staticmethod
    def stun(map: Map, unit: Unit, myUnits: Units, enemyUnits: Units, resourceCount: int,
             turnsLeft: int, resources: List, paths: Dict, foodPaths: Dict, ongoingGoal: Dict, bfs) -> int:
        # dont see where stunning is useful yet
        return 20


actionToMoveWarrior = {
    Action.UP: lambda unit, dir: unit.move('UP'),
    Action.DOWN: lambda unit, dir: unit.move('DOWN'),
    Action.LEFT: lambda unit, dir: unit.move('LEFT'),
    Action.RIGHT: lambda unit, dir: unit.move('RIGHT'),
    Action.ATK: lambda unit, dir: unit.attack(dir[0][1]),
    Action.STUN: lambda unit, dir: unit.stun(dir[0][1])
}
evalFnsWarrior = {
    Action.UP: EvalFnsWarrior.up,
    Action.DOWN: EvalFnsWarrior.down,
    Action.LEFT: EvalFnsWarrior.left,
    Action.RIGHT: EvalFnsWarrior.right,
    Action.ATK: EvalFnsWarrior.attack,
    Action.STUN: EvalFnsWarrior.stun,
}


class GridPlayer:

    def __init__(self):
        self.foodPaths = {}
        self.pathWeights = {}
        self.resources = []
        self.pathingMem = {}

    def validMoves(self, unit: Unit, map: Map, resources: int, enemies: Units) -> List:
        validActions = []
        for dir in DIRECTIONS:
            newCoord = (unit.position()[0] + DIRECTIONS[dir]
                        [0], unit.position()[1] + DIRECTIONS[dir][1])
            if not map.is_wall(*newCoord):
                validActions.append(dir)
        if len(unit.can_attack(enemies)):
            validActions.append(Action.ATK)
        if unit.can_mine(map) and unit.type == 'worker':
            validActions.append(Action.MINE)
        if unit.can_duplicate(resources, 'worker'):
            validActions.append(Action.BREED_WORKER)
        if unit.can_duplicate(resources, 'melee'):
            validActions.append(Action.BREED_WARRIOR)
        if len(unit.can_stun(enemies)):
            validActions.append(Action.STUN)
        return validActions

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:
        # init calls
        def bfsDistance(p1, p2):
            if (p1, p2) in self.pathWeights:
                return self.pathWeights[(p1, p2)]
            elif (p2, p1) in self.pathWeights:
                return self.pathWeights[(p2, p1)]
            else:
                path = game_map.bfs(p1, p2)
                if path == None:
                    return 0 if distance(p1, p2) == 0 else 100000
                for i in range(len(path)):
                    self.pathWeights[(path[i], p2)] = len(path)-i
                return len(path)

        if not len(self.resources):
            self.resources = game_map.find_all_resources()
        workers = your_units.get_all_unit_of_type('worker')
        moves = []
        for worker in workers:
            moveValues = []
            for action in self.validMoves(worker, game_map, resources, enemy_units):
                moveValues.append((evalFnsWorker[action](
                    game_map, worker, your_units, enemy_units, resources, turns_left, self.resources, self.pathWeights, self.foodPaths, bfsDistance),
                    actionToMove[action](worker)))
            moves.append(
                sorted(moveValues, key=lambda x: x[0], reverse=True).pop()[1])
        warriors = your_units.get_all_unit_of_type('melee')
        for warrior in warriors:
            moveValues = []
            for action in self.validMoves(warrior, game_map, resources, enemy_units):
                moveValues.append((evalFnsWarrior[action](
                    game_map, warrior, your_units, enemy_units, resources,
                    turns_left, self.resources, self.pathWeights, self.foodPaths, self.pathingMem, bfsDistance),
                    actionToMoveWarrior[action](warrior, warrior.can_attack(enemy_units))))
            moves.append(
                sorted(moveValues, key=lambda x: x[0], reverse=True).pop()[1])

        return moves
