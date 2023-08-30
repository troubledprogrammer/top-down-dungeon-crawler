"""
Class for basic sprite
"""

import pygame as pg
from typing import Tuple


class Sprite(pg.sprite.Sprite):
    def __init__(self, display: pg.Surface, level, image: pg.Surface,
                 map_offset_start: Tuple[int, int] | pg.Vector2, map_pos: Tuple[int, int] | pg.Vector2) -> None:
        """
        Constructor for a sprite
        :param pg.Surface display: display to draw onto
        :param Level level: reference to level containing the sprite
        :param pg.Surface image: image to draw onto display
        :param Tuple[int, int] | pg.Vector2 map_offset_start: starting offset of the map (map topleft pos)
        :param Tuple[int, int] | pg.Vector2 map_pos: position on map
        """
        super().__init__()

        self.display = display

        self.level = level

        self.img = image
        self.rect = self.img.get_rect(topleft=map_pos + map_offset_start)

        self.pos_on_map = pg.Rect(*map_pos, *self.rect.size)

    def _update_rect_pos(self) -> None:
        """
        Updates pos on screen AFTER map pos has been updated
        :return: None
        """
        self.rect.topleft = self.pos_on_map.topleft + self.level.offset

