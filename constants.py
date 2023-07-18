# TODO Frame rate is not independent of FPS.  Need to add per frame adjustment with Delta time
FPS = 60
FPS_MONITOR = True

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
GLOBAL_SCALE = 1

DEBUG_LEVEL = 1
DEBUG_ENEMY_MOTION_OFF = True
DEBUG_ENEMY_HEALTH_DRAIN = True
DEBUG_SPRITE_RECT_ON = False
DEBUG_GHOST_MODE_ON = False
DEBUG_SHOW_HIT_DAMAGE = True    # prints out damage info
DEBUG_FAST_TRAVEL = True

# CHEATS / CODES
GOD_MODE = True
# PLAYER_START_HEALTH = 100
PLAYER_MAX_HEALTH = 200

ENEMY_SPEED_1 = True
SOUND_FX = False
MUSIC = False
# PLAYER_SCALE = .75  # .75 places player in mid of rect and hitbox.
PLAYER_HITBOX = .05  # .05 is normal
ENEMY_HITBOX = .05  # .05 is normal

BUTTON_SCALE = 1
WEAPON_SCALE = 1.5
HEALTHBAR_SCALE = 3
POTION_SCALE = .35
FIREBALL_SCALE = 1
LIGHTNING_SCALE = .25
GOLD_COIN_SCALE = .5
GOLD_PILE_SCALE = .5

HERO_TYPE = 8
# PLAYER_SPEED = 10  # player speed
PLAYER_HIT_COOLDOWN = 150
DEATH_COOLDOWN = 5

LOOT_MAXIMUM = 5

ARROW_SPEED = 15
ARROW_MIN_DAMAGE = 5
ARROW_MAX_DAMAGE = 50
ARROW_COOLDOWN = 300

SWORD_SPEED = 15
SWORD_MIN_DAMAGE = 5
SWORD_MAX_DAMAGE = 50
SWORD_COOLDOWN = 100

FIREBALL_SPEED = 7
FIREBALL_RECHARGE = 1000
FIREBALL_MIN_DAMAGE = 10
FIREBALL_MAX_DAMAGE = 25

LIGHTNING_SPEED = 12
LIGHTNING_RECHARGE = 800
LIGHTNING_MIN_DAMAGE = 5
LIGHTNING_MAX_DAMAGE = 10

ENEMY_SPEED = 4
ENEMY_HP = 100
# OFFSET = 12 # adjusts character image to align with image.rect
X_OFFSET = -20  # adjusts character image to align with image.rect
Y_OFFSET = 0  # adjusts character image to align with image.rect

# TILE_SIZE = 16 * SCALE
TILE_SIZE = 256
TILE_TYPES = 19  # change this if you add more enemies!
ROWS = 50  # size of map files
COLS = 50  # size of map files
SCROLL_THRESH = 200  # smaller area that player can walk in before camera moves
RANGE = 50
ATTACK_RANGE = 60
BOSS_VIEW_DISTANCE = 750

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (40, 25, 25)
MENU_BG = (130, 0, 0)
PANEL = (50, 50, 50)
