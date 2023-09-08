from enum import Enum

from code.settings import ASSETS_PATH_FLOOR, ASSETS_PATH_WALL_BASIC, ASSETS_PATH_WALL_DECO


class TileType(Enum):
    Empty = 0
    WallBasic = 1
    WallDeco = 2
    Floor = 3


TileTexturePaths = {
    TileType.WallBasic: ASSETS_PATH_WALL_BASIC,
    TileType.WallDeco: ASSETS_PATH_WALL_DECO,
    TileType.Floor: ASSETS_PATH_FLOOR,
}


class TileInfo:
    __slots__ = ["tile_type", "tile_id", "collidable", "texture_name"]

    def __init__(self, tile_type: TileType, tile_id: int, collidable: bool, texture_name: str):
        self.tile_type = tile_type
        self.tile_id = tile_id
        self.collidable = collidable
        self.texture_name = texture_name


WallBasicTypes = {
    -1: TileInfo(TileType.Empty, -1, False, ""),
    0: TileInfo(TileType.WallBasic, 0, True, "wall_edge_bottom_left"),
    1: TileInfo(TileType.WallBasic, 1, True, "wall_edge_bottom_right"),
    2: TileInfo(TileType.WallBasic, 2, True, "wall_edge_left"),
    5: TileInfo(TileType.WallBasic, 5, True, "wall_edge_right"),
    3: TileInfo(TileType.WallBasic, 3, True, "wall_edge_mid_left"),
    4: TileInfo(TileType.WallBasic, 4, True, "wall_edge_mid_right"),
    6: TileInfo(TileType.WallBasic, 6, False, "wall_edge_top_left"),
    7: TileInfo(TileType.WallBasic, 7, False, "wall_edge_top_right"),
    8: TileInfo(TileType.WallBasic, 8, True, "wall_edge_t_shape_bottom_left"),
    9: TileInfo(TileType.WallBasic, 9, True, "wall_edge_t_shape_bottom_right"),
    10: TileInfo(TileType.WallBasic, 10, True, "wall_edge_t_shape_left"),
    11: TileInfo(TileType.WallBasic, 11, True, "wall_edge_t_shape_right"),
    12: TileInfo(TileType.WallBasic, 12, True, "wall_left"),
    13: TileInfo(TileType.WallBasic, 13, True, "wall_mid"),
    20: TileInfo(TileType.WallBasic, 20, True, "wall_right"),
    14: TileInfo(TileType.WallBasic, 14, False, "wall_outer_front_left"),
    15: TileInfo(TileType.WallBasic, 15, False, "wall_outer_front_right"),
    16: TileInfo(TileType.WallBasic, 16, True, "wall_outer_mid_left"),
    17: TileInfo(TileType.WallBasic, 17, True, "wall_outer_mid_right"),
    18: TileInfo(TileType.WallBasic, 18, False, "wall_outer_top_left"),
    19: TileInfo(TileType.WallBasic, 19, False, "wall_outer_top_right"),
    21: TileInfo(TileType.WallBasic, 21, False, "wall_top_left"),
    22: TileInfo(TileType.WallBasic, 22, False, "wall_top_mid"),
    23: TileInfo(TileType.WallBasic, 23, False, "wall_top_right"),
}

WallDecoTypes = {
    -1: TileInfo(TileType.Empty, -1, False, ""),
    23: TileInfo(TileType.WallDeco, 23, True, "wall_hole_1"),
    24: TileInfo(TileType.WallDeco, 24, True, "wall_hole_2"),
    25: TileInfo(TileType.WallDeco, 25, False, "column"),
}

FloorTypes = {
    -1: TileInfo(TileType.Empty, -1, False, ""),
    0: TileInfo(TileType.Floor, 0, False, "floor_1"),
    1: TileInfo(TileType.Floor, 1, False, "floor_2"),
    2: TileInfo(TileType.Floor, 2, False, "floor_3"),
    3: TileInfo(TileType.Floor, 3, False, "floor_4"),
    4: TileInfo(TileType.Floor, 4, False, "floor_5"),
    5: TileInfo(TileType.Floor, 5, False, "floor_6"),
    6: TileInfo(TileType.Floor, 6, False, "floor_7"),
    7: TileInfo(TileType.Floor, 7, False, "floor_8"),
}
