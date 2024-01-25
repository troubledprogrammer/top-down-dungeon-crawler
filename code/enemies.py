from __future__ import annotations

import pygame as pg
from typing import Tuple, TYPE_CHECKING
from enum import Enum
if TYPE_CHECKING:
    from code.window import Window

from code.settings import ASSETS_PATH_ENEMY, ENEMY_SIZE, ENEMY_SPEED, ENEMY_HITBOX_OFFSET_X, \
    ENEMY_HITBOX_OFFSET_Y, ENEMY_HITBOX_SIZE, ANIMATION_MS_PER_FRAME

class EnemyState(Enum):
    Idle = 0,
    Run = 1,

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        # super
        super().__init__()

        # visual
        self.textures = {}
        self._load_textures()
        self.image = self.textures[EnemyState.Idle][0]
        self.animation_time_ms = 0

        # collisions
        self.rect = self.image.get_rect(topleft=pos)
        self.collide_rect = pg.Rect(*pos, *ENEMY_HITBOX_SIZE)
        self.reset_collide_rect_pos()

        # movement
        self.velocity = pg.Vector2(ENEMY_SPEED, ENEMY_SPEED)
        self.pos_on_map = pg.Vector2(pos)

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
        self.pos_on_map += self.velocity * dt
    
    def reset_collide_rect_pos(self):
        self.collide_rect.x = self.rect.x + ENEMY_HITBOX_OFFSET_X
        self.collide_rect.y = self.rect.y + ENEMY_HITBOX_OFFSET_Y

    def update(self, shift: pg.Vector2, window: Window) -> None:
        self._update_movement(window.deltatime)
        self.rect.topleft = self.pos_on_map + shift
        self.reset_collide_rect_pos()
        self._animate(window.deltatime)