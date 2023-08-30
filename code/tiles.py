import pygame as pg
from typing import Tuple
from enum import Enum

from code.settings import TILE_SIZE, TILE_X, TILE_Y


class TileType(Enum):
    EMPTY = 0
    WALL = 1
    START = -1


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type: TileType, image: pg.Surface, pos: Tuple[int, int] | pg.Vector2) -> None:
        super().__init__()

        self.type = tile_type

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.pos_on_map = pg.Vector2(pos)

    def update(self, shift: pg.Vector2) -> None:
        self.rect.topleft = self.pos_on_map + shift


class WallTile(Tile):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2) -> None:
        img = pg.Surface(TILE_SIZE)
        img.fill("blue")

        super().__init__(TileType.WALL, img, pos)


class TileFactory:
    @staticmethod
    def create_tile(tile_type: TileType, xind: int, yind: int):
        match tile_type:
            case TileType.WALL:
                return WallTile((xind*TILE_X, yind*TILE_Y))
