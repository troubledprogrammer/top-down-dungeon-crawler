import pygame as pg
from typing import Tuple

from code.settings import TILE_X, TILE_Y, DEBUG
from code.tiletypes import *


class Tile(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, pos: Tuple[int, int] | pg.Vector2, tile_info: TileInfo) -> None:
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.pos_on_map = pg.Vector2(pos)

        self.tile_info = tile_info

        if DEBUG and self.tile_info.collidable:
            pg.draw.rect(self.image, "blue", pg.Rect(0, 0, *self.rect.size), 1)

    def update(self, shift: pg.Vector2) -> None:
        self.rect.topleft = self.pos_on_map + shift


class StaticTile(Tile):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2, tile_info: TileInfo) -> None:
        img = pg.image.load(TileTexturePaths[tile_info.tile_type] + tile_info.texture_name + ".png")
        x, y = img.get_size()
        ratio = y / x
        img = pg.transform.scale(img, (TILE_X, TILE_Y*ratio))
        if ratio != 1.0:
            x, y = pos
            pos = x, y - TILE_Y*(ratio-1)

        super().__init__(img, pos, tile_info)


class TileFactory:
    @staticmethod
    def create_tile(tile_id: int, layer_type: str, xind: int, yind: int):
        pos = xind * TILE_X, yind * TILE_Y

        # get info
        if layer_type == "Walls":
            tile_info = WallBasicTypes[tile_id]
        elif layer_type == "WallsDeco":
            tile_info = WallDecoTypes[tile_id]
        elif layer_type == "Floor":
            tile_info = FloorTypes[tile_id]
        else:
            tile_info = TileInfo(TileType.Empty, -1, False, "")

        # create tile
        if tile_info.tile_type == TileType.WallBasic:
            return StaticTile(pos, tile_info)
        elif tile_info.tile_type == TileType.WallDeco:
            return StaticTile(pos, tile_info)
        elif tile_info.tile_type == TileType.Floor:
            return StaticTile(pos, tile_info)
