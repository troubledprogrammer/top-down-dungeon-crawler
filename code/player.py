import pygame as pg
from typing import Tuple

from code.settings import PLAYER_SIZE, PLAYER_SPEED, WINDOW_X, WINDOW_Y, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_OFFSET_X, \
    PLAYER_HITBOX_OFFSET_Y, DASH_FRICTION, DASH_POWER


class Player(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int] | pg.Vector2):
        super().__init__()
        self.image = pg.image.load("assets/characters/angel/angel_idle_anim_f0.png")
        self.image = pg.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(center=(WINDOW_X // 2, WINDOW_Y // 2))
        self.collide_rect = pg.Rect(0, 0, *PLAYER_HITBOX_SIZE)
        self.reset_collide_rect_pos()

        self.velocity = pg.Vector2()
        self.dash_vector = pg.Vector2()
        self.dash_cooldown_ms = 0
        self.pos = pg.Vector2(pos)
        self.lock_x = self.lock_y = False

    def _update_input_key(self, dt):
        keys = pg.key.get_pressed()

        self.velocity.x = 0
        if keys[pg.K_a]:
            self.velocity.x += -PLAYER_SPEED * dt
        if keys[pg.K_d]:
            self.velocity.x += PLAYER_SPEED * dt

        self.velocity.y = 0
        if keys[pg.K_w]:
            self.velocity.y += -PLAYER_SPEED * dt
        if keys[pg.K_s]:
            self.velocity.y += PLAYER_SPEED * dt

    def _update_input_mouse(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.dash_cooldown_ms == 0:
                mouse_pos = pg.Vector2(pg.mouse.get_pos())
                self.dash_vector = (mouse_pos - pg.Vector2(self.rect.center)).normalize() * DASH_POWER
                self.dash_cooldown_ms = 1000

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

    def update(self, window):
        self._update_input_key(window.deltatime)
        self._update_input_mouse(window.events)
        self._update_dash_friction(window.deltatime)
