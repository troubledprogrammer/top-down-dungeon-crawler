from __future__ import annotations

import pygame as pg
from typing import Tuple, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from code.window import Window
    from code.entities import EntityType

from code.settings import ASSETS_PATH_ENEMY, ENEMY_SIZE, ENEMY_SPEED, ENEMY_HITBOX_OFFSET_X, \
    ENEMY_HITBOX_OFFSET_Y, ENEMY_HITBOX_SIZE, ANIMATION_MS_PER_FRAME


class EnemyState(Enum):
    Idle = 0,
    Run = 1,


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2, entity_type: EntityType.ENEMY):
        # super
        super().__init__()
        self.entity_type = entity_type

        # visual
        self.textures = {}
        self._load_textures()
        self.image = self.textures[EnemyState.Idle][0]
        self.animation_time_ms = 0

        # collisions
        self.rect = self.image.get_rect()
        self.collide_rect = pg.Rect(*pos, *ENEMY_HITBOX_SIZE)
        self.hitbox = pg.Surface(self.collide_rect.size, pg.SRCALPHA)
        pg.draw.rect(self.hitbox, "red", pg.Rect(0, 0, *ENEMY_HITBOX_SIZE), 1)
        self.reset_rect_pos()

        # movement
        self.velocity = pg.Vector2(ENEMY_SPEED, ENEMY_SPEED)

        # damage
        self.damage_value = 5

    def _load_textures(self):
        self.textures = {
            EnemyState.Idle: [
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_idle_anim_f0.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_idle_anim_f1.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_idle_anim_f2.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_idle_anim_f3.png"), ENEMY_SIZE),
            ],
            EnemyState.Run: [
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_run_anim_f0.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_run_anim_f1.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_run_anim_f2.png"), ENEMY_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_ENEMY + "wogol_run_anim_f3.png"), ENEMY_SIZE),
            ],
        }

    def _get_state(self):
        if self.velocity.magnitude() > 0:
            return EnemyState.Run
        else:
            return EnemyState.Idle

    def _animate(self, dt):
        self.animation_time_ms += dt
        self.animation_time_ms %= ANIMATION_MS_PER_FRAME * 4  # number of frames in animation loop
        animation_frame = self.animation_time_ms // ANIMATION_MS_PER_FRAME
        state = self._get_state()

        self.image = self.textures[state][animation_frame]

    def _update_movement(self, dt: int):
        self.collide_rect.topleft += self.velocity * dt

    def reset_rect_pos(self):
        self.rect.x = self.collide_rect.x - ENEMY_HITBOX_OFFSET_X
        self.rect.y = self.collide_rect.y - ENEMY_HITBOX_OFFSET_Y

    def update(self, window: Window) -> None:
        self._update_movement(window.deltatime)
        self.reset_rect_pos()
        self._animate(window.deltatime)
