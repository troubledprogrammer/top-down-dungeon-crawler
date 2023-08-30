"""
Handles the logic for levels
"""
from __future__ import annotations

import pygame as pg
from typing import Tuple

from _code.player import Player
from _code.window import Window
from _code.sprite import Sprite


def load_csv(fp):
    with open(fp) as f:
        level = [line.split(",") for line in f.readlines()]
    return level


class WallTile(Sprite):
    def __init__(self, display: pg.Surface, level: Level, map_offset_start: Tuple[int, int] | pg.Vector2,
                 map_pos: Tuple[int, int] | pg.Vector2) -> None:
        img = pg.Surface((50, 50))
        img.fill("blue")
        super().__init__(display, level, img, map_offset_start, map_pos)

    def _draw(self):
        self.display.blit(self.img, self.rect)

    def update(self) -> None:
        self._update_rect_pos()
        self._draw()


class Level:
    tile_size = 50

    def __init__(self, window: Window) -> None:
        self.window = window

        self.walls = pg.sprite.Group()
        self.player = None
        self.offset = pg.Vector2()

        self._load_tiles()

    def _load_tiles(self):
        data = load_csv("data/levels/tilemap.csv")
        [start_x, start_y] = [int(c) for c in data[0]]
        tilemap = data[1:]

        start_pos = start_x * self.tile_size, start_y * self.tile_size

        win_size_x, win_size_y = self.window.display.get_size()
        center = pg.Vector2(win_size_x // 2, win_size_y // 2)

        self.offset = center + (-start_pos[0], -start_pos[1])

        for yi, row in enumerate(tilemap):
            for xi, val in enumerate(row):
                map_pos = xi * self.tile_size, yi * self.tile_size
                if val == "1":
                    s = WallTile(self.window.display, self, self.offset, map_pos)
                    self.walls.add(s)
                if val == "-1":
                    self.player = Player(self.window.display, self, center, start_pos)

    def _update_input(self):
        dist_to_move = round(self.player.speed * self.window.deltatime, 2)
        # print(dist_to_move, self.player.speed * self.window.deltatime)

        if self.window.keys[pg.K_d]:
            self.player.pos_on_map.x += dist_to_move
            collided_sprite = pg.sprite.spritecollideany(self.player, self.walls)
            if collided_sprite is not None:
                self.player.pos_on_map.right = collided_sprite.rect.left
        if self.window.keys[pg.K_a]:
            self.player.pos_on_map.x -= dist_to_move
            if pg.sprite.spritecollideany(self.player, self.walls):
                self.player.pos_on_map.x += dist_to_move + 0.2
        if self.window.keys[pg.K_s]:
            self.player.pos_on_map.y += dist_to_move
            if pg.sprite.spritecollideany(self.player, self.walls):
                self.player.pos_on_map.y -= dist_to_move
        if self.window.keys[pg.K_w]:
            self.player.pos_on_map.y -= dist_to_move
            if pg.sprite.spritecollideany(self.player, self.walls):
                self.player.pos_on_map.y += dist_to_move

    def update(self):
        self._update_input()

        self.walls.update()
        self.player.update()
