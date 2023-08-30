from enum import Enum

from code.settings import TILE_X, TILE_Y
from code.player import Player


class EntityType(Enum):
    NULL = 0
    PLAYER = 1


class EntityFactory:
    @staticmethod
    def create_entity(entity_type: EntityType, xind: int, yind: int):
        match entity_type:
            case EntityType.PLAYER:
                return Player((xind*TILE_X, yind*TILE_Y))
