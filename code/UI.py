from __future__ import annotations

import pygame as pg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code.player import Player
from code.settings import *


# MAYBE REFACTOR THIS INTO OWN FILE AS CAN BE USED BY OTHER SPRITES
def _load_and_scale(filepath: str, height: int):
    img = pg.image.load(filepath)
    ar = img.get_width() / img.get_height()
    img = pg.transform.scale(img, (ar * height, height))
    return img


class UI(pg.sprite.Sprite):
    def __init__(self, player: Player):
        super().__init__()
        # parent
        self.player = player

        # textures
        self.health_bar = _load_and_scale(ASSETS_PATH_UI + "healthbar.png", HEATH_BAR_HEIGHT)
        self.dash_bar = _load_and_scale(ASSETS_PATH_UI + "dash_bar.png", DASH_BAR_HEIGHT)
        self.health_bar_inner_texture = _load_and_scale(ASSETS_PATH_UI + "healthbar_inner.png", HEATH_BAR_INNER_HEIGHT)
        self.dash_bar_inner_texture = _load_and_scale(ASSETS_PATH_UI + "dash_bar_inner.png", DASH_BAR_INNER_HEIGHT)
        self.health_bar_inner_width = self.health_bar_inner_texture.get_width()
        self.dash_bar_inner_width = self.dash_bar_inner_texture.get_width()

        # render
        self.image = pg.Surface(WINDOW_SIZE)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def _draw(self):
        self.image.blit(self.health_bar, HEATH_BAR_POS)
        self.image.blit(self.health_bar_inner, HEATH_BAR_INNER_POS)

        self.image.blit(self.dash_bar, DASH_BAR_POS)
        self.image.blit(self.dash_bar_inner, DASH_BAR_INNER_POS)

    def _update_dash_bar(self):
        ratio = 1 - self.player.dash_cooldown_ms / DASH_COOLDOWN
        self.dash_bar_inner = pg.transform.scale(self.dash_bar_inner_texture,
                                                 (self.dash_bar_inner_width * ratio, DASH_BAR_INNER_HEIGHT))

    def _update_health_bar(self):
        ratio = self.player.health / PLAYER_MAX_HEALTH
        if ratio <= 0: # health is negative
            print("Health went negative: cannot draw the health bar")
            self.health_bar_inner = pg.Surface((0,0))
            return
        self.health_bar_inner = pg.transform.scale(self.health_bar_inner_texture,
                                                   (self.health_bar_inner_width * ratio, HEATH_BAR_INNER_HEIGHT))

    def update(self):
        self._update_dash_bar()
        self._update_health_bar()
        self._draw()
