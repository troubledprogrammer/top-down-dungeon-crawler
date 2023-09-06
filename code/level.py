import pygame as pg
from pathlib import Path

from code.settings import LEVEL_PATH, PLAYER_SPEED, PLAYER_LOCK_X_MIN, PLAYER_LOCK_X_MAX, PLAYER_LOCK_Y_MIN, \
    PLAYER_LOCK_Y_MAX, WINDOW_X, WINDOW_Y
from code.tiles import TileFactory
from code.entities import EntityType, EntityFactory
from code.window import Window


def load_csv(fp):
    with open(fp, "r") as f:
        level = [[int(n) for n in line.split(",")] for line in f.readlines()]
    return level


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
        self._setup_entities(Path(LEVEL_PATH.format(level_id=0, layer_type="info")))

        # shift
        self.world_shift = pg.Vector2()
        self._center_player()

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

    def _center_player(self):
        player = self.player.sprite
        player_x, player_y = player.rect.center
        window_center_x, window_center_y = WINDOW_X // 2, WINDOW_Y // 2
        self.world_shift.x, self.world_shift.y = window_center_x - player_x, window_center_y - player_y
        player.rect.center = window_center_x, window_center_y

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
        collided_sprite = pg.sprite.spritecollideany(player, self.walls_collidable)
        if collided_sprite is not None:
            # if player.velocity.x < 0:
            #     player.rect.left = collided_sprite.rect.right
            # elif player.velocity.x > 0:
            #     player.rect.right = collided_sprite.rect.left
            player.rect.x -= player.velocity.x

    def _do_vertical_collisions(self):
        player = self.player.sprite
        player.update_movement_y()
        collided_sprite = pg.sprite.spritecollideany(player, self.walls_collidable)
        if collided_sprite is not None:
            # if player.velocity.y < 0:
            #     player.rect.top = collided_sprite.rect.bottom
            # elif player.velocity.y > 0:
            #     player.rect.bottom = collided_sprite.rect.top
            player.rect.y -= player.velocity.y

    def _update_sprites(self):
        self.floor.update(self.world_shift)
        self.walls_collidable.update(self.world_shift)
        self.walls_non_collidable.update(self.world_shift)

    def _update_player(self):
        self.player.update(self.window.deltatime)
        self._do_horizontal_collisions()
        self._do_vertical_collisions()

    def _draw(self):
        self.floor.draw(self.window.display)
        self.player.draw(self.window.display)
        self.walls_collidable.draw(self.window.display)
        self.walls_non_collidable.draw(self.window.display)

    def tick(self):
        self._update_sprites()
        self._scroll(self.window.deltatime)
        self._update_player()
        self._draw()
