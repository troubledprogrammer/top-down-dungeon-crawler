import pygame as pg
from typing import Tuple

from code.settings import DEBUG, WINDOW_X, WINDOW_Y

class Camera:
    def __init__(self, window: pg.Surface):
        self.world_shift = pg.Vector2()
        self.window = window
    
    def render_sprites(self, sprites: pg.sprite.Group | pg.sprite.GroupSingle):
        for s in sprites:
            pos = pg.Rect(s.rect.left + self.world_shift.x,
                          s.rect.top + self.world_shift.y,
                          s.rect.width,
                          s.rect.height)
            self.window.display.blit(s.image, pos)

            if DEBUG:
                hitbox_pos = pg.Rect(
                    s.collide_rect.left + self.world_shift.x,
                    s.collide_rect.top + self.world_shift.y,
                    s.collide_rect.width,
                    s.collide_rect.height
                )
                self.window.display.blit(s.hitbox, hitbox_pos)

    def center_at_point(self, point: Tuple[int, int]):
        self.world_shift.x = -point[0] + WINDOW_X // 2
        self.world_shift.y = -point[1] + WINDOW_Y // 2
