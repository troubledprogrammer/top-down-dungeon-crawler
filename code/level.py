import pygame as pg
from pathlib import Path

from code.settings import LEVEL_FILE_PATH, PLAYER_SPEED, PLAYER_LOCK_X_MIN, PLAYER_LOCK_X_MAX, PLAYER_LOCK_Y_MIN, PLAYER_LOCK_Y_MAX
from code.tiles import TileType, TileFactory
from code.entities import EntityType, EntityFactory
from code.window import Window


def load_csv(fp: Path):
    with fp.open("r") as f:
        level = [[int(n) for n in line.split(",")] for line in f.readlines()]
    return level


class Level:
    def __init__(self, level_id: int, window: Window):
        # display
        self.window = window

        # tiles
        self.walls = pg.sprite.Group()
        self._setup_tiles(Path(f"{LEVEL_FILE_PATH}/{level_id}"))

        # entities
        self.player = pg.sprite.GroupSingle()
        self._setup_entities(Path(f"{LEVEL_FILE_PATH}/{level_id}"))

        # shift
        self.world_shift = pg.Vector2()

    def _setup_tiles(self, path: Path):
        tilemap = [[TileType(c) for c in r] for r in load_csv(path / "tilemap.csv")]
        for ri, row in enumerate(tilemap):
            for ci, tile_type in enumerate(row):
                t = TileFactory.create_tile(tile_type, ci, ri)
                if tile_type == TileType.WALL:
                    self.walls.add(t)

    def _setup_entities(self, path: Path):
        entitymap = [[EntityType(c) for c in r] for r in load_csv(path / "entitymap.csv")]
        for ri, row in enumerate(entitymap):
            for ci, entity_type in enumerate(row):
                e = EntityFactory.create_entity(entity_type, ci, ri)
                if entity_type == EntityType.PLAYER:
                    self.player.add(e)

    def _scroll(self, dt):
        player = self.player.sprite

        # x
        player_x = player.rect.centerx
        direction_x = player.velocity.x
        if player_x < PLAYER_LOCK_X_MIN and direction_x < 0:
            self.world_shift.x += PLAYER_SPEED * dt
            player.lock_x = True
        elif player_x > PLAYER_LOCK_X_MAX and direction_x > 0:
            self.world_shift.x += -PLAYER_SPEED * dt
            player.lock_x = True
        else:
            player.lock_x = False
        
        # y
        player_y = player.rect.centery
        direction_y = player.velocity.y
        if player_y < PLAYER_LOCK_Y_MIN and direction_y < 0:
            self.world_shift.y += PLAYER_SPEED * dt
            player.lock_y = True
        elif player_y > PLAYER_LOCK_Y_MAX and direction_y > 0:
            self.world_shift.y += -PLAYER_SPEED * dt
            player.lock_y = True
        else:
            player.lock_y = False

    def _do_horizontal_collisions(self):
        player = self.player.sprite
        player.update_movement_x()
        collided_sprite = pg.sprite.spritecollideany(player, self.walls)
        if collided_sprite is not None:
            if player.velocity.x < 0:
                player.rect.left = collided_sprite.rect.right
            elif player.velocity.x > 0:
                player.rect.right = collided_sprite.rect.left
    
    def _do_vertical_collisions(self):
        player = self.player.sprite
        player.update_movement_y()
        collided_sprite = pg.sprite.spritecollideany(player, self.walls)
        if collided_sprite is not None:
            if player.velocity.y < 0:
                player.rect.top = collided_sprite.rect.bottom
            elif player.velocity.y > 0:
                player.rect.bottom = collided_sprite.rect.top

    def _draw(self):
        self.walls.draw(self.window.display)
        self.player.draw(self.window.display)

    def tick(self):
        self.walls.update(self.world_shift)
        self._scroll(self.window.deltatime)
        self.player.update(self.window.deltatime)
        self._do_horizontal_collisions()
        self._do_vertical_collisions()
        self._draw()
