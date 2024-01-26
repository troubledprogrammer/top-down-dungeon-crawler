from enum import Enum

from code.settings import TILE_X, TILE_Y
from code.player import Player
from code.enemies import Enemy


class EntityType(Enum):
    NULL = -1
    PLAYER = 0
    ENEMY = 1


class EntityFactory:
    @staticmethod
    def create_entity(entity_type: EntityType, xind: int, yind: int):
        pos = xind*TILE_X + TILE_X // 2, yind*TILE_Y + TILE_Y//2
        match entity_type:
            case EntityType.PLAYER:
                return Player(pos, EntityType.PLAYER)
            case EntityType.ENEMY:
                return Enemy(pos, EntityType.ENEMY)
