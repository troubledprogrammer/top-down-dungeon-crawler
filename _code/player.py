"""
File for player logic
"""

import pygame as pg
from typing import Tuple


class Player(pg.sprite.Sprite):
    """
    Class for player sprite
    """
    speed = 5

    def __init__(self, display: pg.Surface, level, window_pos: Tuple[int, int] | pg.Vector2,
                 level_pos: Tuple[int, int] | pg.Vector2) -> None:
        """
        Constructor for player
        :param pg.Surface display: surface sprite blits to
        :param Level level: a reference to the level containing the player
        :param Tuple[int, int] | pg.Vector2 window_pos: position in the window
        :param Tuple[int, int] | pg.Vector2 window_pos: position on the map
        """
        super().__init__()
        self.display = display

        self.level = level

        self.img = pg.Surface((10, 10))
        self.img.fill((255, 0, 0, 255))
        self.rect = self.img.get_rect(topleft=window_pos)
        self.pos_on_map = pg.Rect(*level_pos, *self.rect.size)

    def _update_screen_pos(self) -> None:
        """
        Moves the player to the right screen pos based on map pos
        """
        pos = self.pos_on_map.topleft + self.level.offset

        self.rect.topleft = pos

    def _draw(self) -> None:
        """
        Draws the player to the screen
        :return:
        """
        self.display.blit(self.img, self.rect)

    def update(self) -> None:
        """
        Pygame sprite default method: called every tick
        """
        self._update_screen_pos()
        self._draw()
