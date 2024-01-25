from __future__ import annotations

import pygame as pg
from typing import Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from code.window import Window

from code.settings import PLAYER_SIZE, PLAYER_SPEED, WINDOW_X, WINDOW_Y, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_OFFSET_X, \
    PLAYER_HITBOX_OFFSET_Y, DASH_FRICTION, DASH_POWER, DASH_COOLDOWN, ANIMATION_MS_PER_FRAME, ASSETS_PATH_PLAYER, \
    PLAYER_MAX_HEALTH, DAMAGE_COOLDOWN
from enum import Enum


class PlayerState(Enum):
    Idle = 0,
    Run = 1,
    Dash = 2,


class Player(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        # super
        super().__init__()

        # visual
        self.textures = {}
        self._load_textures()
        self.image = self.textures[PlayerState.Idle][0]
        self.animation_time_ms = 0

        # collisions
        self.rect = self.image.get_rect(center=(WINDOW_X // 2, WINDOW_Y // 2))
        self.collide_rect = pg.Rect(0, 0, *PLAYER_HITBOX_SIZE)
        self.reset_collide_rect_pos()

        # movement
        self.velocity = pg.Vector2()
        self.dash_vector = pg.Vector2()
        self.dash_cooldown_ms = 0
        self.pos = pg.Vector2(pos)

        # health
        self.health = PLAYER_MAX_HEALTH
        self.damage_cooldown = 0


    def _load_textures(self):
        self.textures = {
            PlayerState.Idle: [
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_idle_anim_f0.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_idle_anim_f1.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_idle_anim_f2.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_idle_anim_f3.png"), PLAYER_SIZE),
            ],
            PlayerState.Run: [
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_run_anim_f0.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_run_anim_f1.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_run_anim_f2.png"), PLAYER_SIZE),
                pg.transform.scale(pg.image.load(ASSETS_PATH_PLAYER + "angel_run_anim_f3.png"), PLAYER_SIZE),
            ],
        }

    def _get_state(self):
        if self.dash_vector.magnitude() > 0:
            return PlayerState.Dash
        elif self.velocity.magnitude() > 0:
            return PlayerState.Run
        else:
            return PlayerState.Idle

    def _animate(self, dt):
        self.animation_time_ms += dt
        self.animation_time_ms %= ANIMATION_MS_PER_FRAME * 4  # number of frames in animation loop
        animation_frame = self.animation_time_ms // ANIMATION_MS_PER_FRAME
        state = self._get_state()
        if state == PlayerState.Dash:
            state = PlayerState.Run

        self.image = self.textures[state][animation_frame]

    def _update_input_key(self, dt):
        keys = pg.key.get_pressed()

        self.velocity.x = 0
        if keys[pg.K_a]:
            self.velocity.x += -1
        if keys[pg.K_d]:
            self.velocity.x += 1

        self.velocity.y = 0
        if keys[pg.K_w]:
            self.velocity.y += -1
        if keys[pg.K_s]:
            self.velocity.y += 1
        
        if self.velocity.magnitude() != 0:
            self.velocity = self.velocity.normalize()
            self.velocity *= PLAYER_SPEED * dt

    def _update_input_mouse(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.dash_cooldown_ms == 0:
                mouse_pos = pg.Vector2(pg.mouse.get_pos())
                self.dash_vector = (mouse_pos - pg.Vector2(self.rect.center)).normalize() * DASH_POWER
                self.dash_cooldown_ms = DASH_COOLDOWN

    def _update_dash_friction(self, dt):
        self.velocity += self.dash_vector

        if self.dash_vector.magnitude() < 0.1:
            self.dash_vector = pg.Vector2()
        else:
            self.dash_vector *= DASH_FRICTION ** dt

        if self.dash_cooldown_ms > 0:
            self.dash_cooldown_ms -= dt
            # keep non negative
            if self.dash_cooldown_ms < 0:
                self.dash_cooldown_ms = 0

    def reset_collide_rect_pos(self):
        self.collide_rect.x = self.rect.x + PLAYER_HITBOX_OFFSET_X
        self.collide_rect.y = self.rect.y + PLAYER_HITBOX_OFFSET_Y

    def update_enemy_collision(self, enemies: pg.sprite.Group, dt: int):
        if self.damage_cooldown <= 0:
            for e in enemies:
                if e.collide_rect.colliderect(self.collide_rect):
                    print(f"took damage from {id(e)}")
                    self.damage_cooldown = DAMAGE_COOLDOWN
                    self.health -= e.damage_value
        else:
            self.damage_cooldown -= dt

    def update(self, window: Window):
        self._update_input_key(window.deltatime)
        self._update_input_mouse(window.events)
        self._update_dash_friction(window.deltatime)
        self._animate(window.deltatime)
