# ------------------------------------Visual--------------------------------------#
# WINDOW
WINDOW_SIZE = WINDOW_X, WINDOW_Y = 1200, 800

# TILE
TILE_SIZE = TILE_X, TILE_Y = 50, 50

# PLAYER
PLAYER_SIZE = PLAYER_X, PLAYER_Y = 40, 40
PLAYER_HITBOX_SIZE = PLAYER_HITBOX_SIZE_X, PLAYER_HITBOX_SIZE_Y = 20, 25
PLAYER_HITBOX_OFFSET = PLAYER_HITBOX_OFFSET_X, PLAYER_HITBOX_OFFSET_Y = 15, 15

# ANIMATION
ANIMATION_MS_PER_FRAME = 150

# UI
HEATH_BAR_HEIGHT = 30
HEATH_BAR_INNER_HEIGHT = int(HEATH_BAR_HEIGHT / 3)
DASH_BAR_HEIGHT = 30
DASH_BAR_INNER_HEIGHT = int(DASH_BAR_HEIGHT / 3)
HEATH_BAR_POS = 15, 15
HEATH_BAR_INNER_POS = HEATH_BAR_POS[0] + 17, HEATH_BAR_POS[1] + HEATH_BAR_INNER_HEIGHT
DASH_BAR_POS = 15, 50
DASH_BAR_INNER_POS = DASH_BAR_POS[0] + 17, DASH_BAR_POS[1] + DASH_BAR_INNER_HEIGHT

# ------------------------------------Gameplay------------------------------------#
# PLAYER
PLAYER_SPEED = 0.2
DASH_POWER = 10
DASH_FRICTION = 0.99
DASH_COOLDOWN = 4000
PLAYER_MAX_HEALTH = 100

# ------------------------------------Project-------------------------------------#
# LEVEL
LEVEL_PATH = "data/levels/{level_id}/{level_id}_{layer_type}.csv"
ASSETS_PATH_WALL_BASIC = "assets/wall/basic/"
ASSETS_PATH_WALL_DECO = "assets/wall/deco/"
ASSETS_PATH_FLOOR = "assets/floor/"
ASSETS_PATH_PLAYER = "assets/characters/angel/"
ASSETS_PATH_UI = "assets/gui/"

# ------------------------------------Debug---------------------------------------#
# DEBUG
DEBUG = False
