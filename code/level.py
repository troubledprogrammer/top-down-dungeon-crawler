import pygame as pg
from pathlib import Path

from code.settings import LEVEL_PATH, DEBUG, WINDOW_X, WINDOW_Y
from code.tiles import TileFactory
from code.entities import EntityType, EntityFactory
from code.player import Player
from code.window import Window
from code.UI import UI


def load_csv(fp):
    with open(fp, "r") as f:
        level = [[int(n) for n in line.split(",")] for line in f.readlines()]
    return level


# noinspection PyTypeChecker
class Level:
    def __init__(self, level_id: int, window: Window):
        # display
        self.window = window

        # level
        self.level_id = level_id

        # tiles
        self.walls_collidable = pg.sprite.Group()
        self.walls_non_collidable = pg.sprite.Group()
        self.floor = pg.sprite.Group()
        self._create_tile_groups()

        # entities
        self.player = pg.sprite.GroupSingle()
        self.enemies = pg.sprite.Group()
        self._setup_entities(Path(LEVEL_PATH.format(level_id=0, layer_type="info")))

        # ui
        self.ui = pg.sprite.GroupSingle(UI(self.player.sprite))

        # shift
        self.world_shift = pg.Vector2()
        self._center_player()
        self._update_sprites()  # repositions sprites with world after player has been centered

    def _create_tile_group_from_path(self, layer_type: str):
        collidable = []
        non_collidable = []
        p = LEVEL_PATH.format(level_id=self.level_id, layer_type=layer_type)
        tilemap = load_csv(p)
        for ri, row in enumerate(tilemap):
            for ci, tile_type in enumerate(row):
                t = TileFactory.create_tile(tile_type, layer_type, ci, ri)
                if t is not None:
                    if t.tile_info.collidable:
                        collidable.append(t)
                    else:
                        non_collidable.append(t)
        return collidable, non_collidable

    def _create_tile_groups(self):
        collidable, non_collidable = self._create_tile_group_from_path("Walls")
        self.walls_collidable.add(collidable)
        self.walls_non_collidable.add(non_collidable)

        collidable, non_collidable = self._create_tile_group_from_path("WallsDeco")
        self.walls_collidable.add(collidable)
        self.walls_non_collidable.add(non_collidable)

        collidable, non_collidable = self._create_tile_group_from_path("Floor")
        self.floor.add(non_collidable)

    def _setup_entities(self, path: Path):
        entitymap = [[EntityType(c) for c in r] for r in load_csv(path)]
        for ri, row in enumerate(entitymap):
            for ci, entity_type in enumerate(row):
                e = EntityFactory.create_entity(entity_type, ci, ri)
                if entity_type == EntityType.PLAYER:
                    self.player.add(e)
                if entity_type == EntityType.ENEMY:
                    self.enemies.add(e)

    def _center_player(self):
        player = self.player.sprite
        player_x, player_y = player.pos
        window_center_x, window_center_y = WINDOW_X // 2, WINDOW_Y // 2
        self.world_shift.x, self.world_shift.y = window_center_x - player_x, window_center_y - player_y

    def _run_tile_collisions_x(self, player: Player):
        collidable_sprites = self.walls_collidable.sprites()  # + ...

        for s in collidable_sprites:
            if s.rect.colliderect(player.collide_rect):
                # x
                if player.velocity.x < 0 and s.rect.left <= player.collide_rect.left <= s.rect.right:
                    player.collide_rect.left = s.rect.right
                elif player.velocity.x > 0 and s.rect.left <= player.collide_rect.right <= s.rect.right:
                    player.collide_rect.right = s.rect.left
                else:
                    print(f"Player clipped inside {s} ({s.rect=})")

    def _run_tile_collisions_y(self, player: Player):
        collidable_sprites = self.walls_collidable.sprites()  # + ...

        for s in collidable_sprites:
            if s.rect.colliderect(player.collide_rect):
                # y
                if player.velocity.y < 0 and s.rect.top <= player.collide_rect.top <= s.rect.bottom:
                    player.collide_rect.top = s.rect.bottom
                elif player.velocity.y > 0 and s.rect.top <= player.collide_rect.bottom <= s.rect.bottom:
                    player.collide_rect.bottom = s.rect.top
                else:
                    print(f"Player clipped inside {s} ({s.rect=})")

    def _move_player_x(self):
        player = self.player.sprite
        start_x = player.collide_rect.x
        player.collide_rect.x += player.velocity.x
        self._run_tile_collisions_x(player)
        end_x = player.collide_rect.x
        self.world_shift.x += start_x - end_x

    def _move_player_y(self):
        player = self.player.sprite
        start_y = player.collide_rect.y
        player.collide_rect.y += player.velocity.y
        self._run_tile_collisions_y(player)
        end_y = player.collide_rect.y
        self.world_shift.y += start_y - end_y

    def _update_sprites(self):
        self.floor.update(self.world_shift)
        self.walls_collidable.update(self.world_shift)
        self.walls_non_collidable.update(self.world_shift)
        self.enemies.update(self.world_shift, self.window)

    def _update_player(self):
        # movement
        self.player.update(self.window)
        self._move_player_x()
        self._move_player_y()
        self.player.sprite.reset_collide_rect_pos()

        # enemy collision
        self.player.sprite.update_enemy_collision(self.enemies, self.window.deltatime)

    def _draw(self):
        self.floor.draw(self.window.display)
        self.enemies.draw(self.window.display)
        self.player.draw(self.window.display)
        self.walls_collidable.draw(self.window.display)
        self.walls_non_collidable.draw(self.window.display)
        self.ui.draw(self.window.display)

        if DEBUG:
            pg.draw.rect(self.window.display, "green", self.player.sprite.collide_rect, 2)
            for e in self.enemies.sprites():
                pg.draw.rect(self.window.display, "red", e.collide_rect, 1)

    def tick(self):
        self._update_player()
        self._update_sprites()
        self.ui.update()
        self._draw()
