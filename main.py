import sys

# import pytmx
from pytmx.util_pygame import *
from pygame import mixer
import constants
from weapon import Weapon
from items import Item
from world import World
from button import Button
from tilesheet import Tilesheet
from colordict import *
import inspect
from pathlib import Path
import pygame
import os
from character_classes import *


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        #        print(pygame.font.get_fonts())
        self.text = "0"

    def render(self, display, level: str):
        self.text = "level: {} - FPS:{:.0f}".format(level, self.clock.get_fps())

        pygame.display.set_caption(self.text)
        display.blit(self.font.render(self.text, True, green), ((constants.SCREEN_WIDTH / 2) - 250, 12))


def line_numb():
    ''' Returns the current line number in our program
    '''
    return inspect.currentframe().f_back.f_lineno


game_title = "End of Civ"

if constants.DEBUG_LEVEL:
    print("\n\n{} starting\nPath {}\n".format(game_title, Path(__file__)))

# load music (has to be done before pygame.init for perf reasons)
mixer.init()
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.2)

# play background music only if SOUND_FX True
if constants.MUSIC:
    pygame.mixer.music.play(-1, 0.0, 5000)

if constants.SOUND_FX == False:
    volume = 0.0
else:
    volume = .5

pygame.init()

if constants.DEBUG_LEVEL:
    print("[pygame.mixer] init")
    print("[pygame.mixer.music] loaded, volume is {}".format(volume))

# minimum game screen width / height
if constants.SCREEN_WIDTH <= 680:
    constants.SCREEN_WIDTH = 680
if constants.SCREEN_HEIGHT <= 480:
    constants.SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
# screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption(game_title)

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 1
god_mode = constants.GOD_MODE
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
colors = ColorDict()
black = colors['black']
white = colors['white']
green = colors['green']
indigo = colors['indigo']
cyan = colors['cyan']


# helper function to scale image
def scale_img(image, scale, smooth=False):
    w = image.get_width()
    h = image.get_height()
    if smooth:
        if scale == 2:
            return pygame.transform.scale2x(image)
        else:
            return pygame.transform.smoothscale(image, (w * scale, h * scale))
    else:
        return pygame.transform.scale(image, (w * scale, h * scale))


def load_gold_images(coin_images, gold_images):
    # Load gold COIN images
    # (filename, width, height, rows, cols, start_row_index= 0)  3270 / 496    15x 2
    tiles = Tilesheet("assets/images/items/GoldCoin_v1.1/64/spritesheet/GoldCoin.png", 64, 64, 1, 30,
                      0)  # 3 images, row 1
    for x in range(0, tiles.cols, 2):  # skip
        img = tiles.get_tile(x, 0)
        img = scale_img(img, constants.GOLD_COIN)
        coin_images.append(img)

    if constants.DEBUG_LEVEL:
        print("MAIN.PY, line: {}. Coin images loaded, {} total".format(line_numb(), tiles.cols))

    # load piles of gold
    gold = {"gold1": "gold-big_no_glow.png",
            "gold2": "gold-big-2_no_glow.png",
            "gold3": "gold-big-2.png",
            "gold4": "gold-big.png",
            "gold5": "gold-mid_no_glow.png",
            "gold6": "gold-mid-2_no_glow.png",
            "gold7": "gold-mid-2.png",
            "gold8": "gold-mid.png",
            "gold9": "gold-small_no_glow.png",
            "gold10": "gold-small-2_no_glow.png",
            "gold11": "gold-small-2.png",
            "gold12": "gold-small.png",
            }

    for x, item in enumerate(gold):
        if constants.DEBUG_LEVEL > 1:
            print(" x={}, item={}, file={}".format(x, item, gold[item]))
        img = pygame.image.load(
            "assets/images/environment/Sprites/PNG/gold piles/{}".format(gold[item])).convert_alpha()
        gold_images.append(img)


def load_potions():
    # load potion images
    red_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-red-new.png").convert_alpha(),
                           constants.POTION_SCALE)
    blue_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-blue-new.png").convert_alpha(),
                            constants.POTION_SCALE)
    green_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-green-new.png").convert_alpha(),
                             constants.POTION_SCALE)

    if constants.DEBUG_LEVEL:
        print(" line: {}. Potion images loaded".format(line_numb()))

    return red_potion, blue_potion, green_potion


shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(volume)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(volume)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(volume)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(volume)

if constants.DEBUG_LEVEL:
    print("action sounds loaded")

# load button images
start_img = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(),
                      constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(),
                        constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(),
                       constants.BUTTON_SCALE)

# load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow-new.png").convert_alpha(), constants.WEAPON_SCALE)
sword_image = scale_img(pygame.image.load("assets/images/weapons/sword.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),
                           constants.FIREBALL_SCALE)
lightning_image = scale_img(pygame.image.load("assets/images/weapons/red-lightning.png").convert_alpha(),
                            constants.LIGHTNING_SCALE)

# load coin images
coin_images = []
gold_images = []
load_gold_images(coin_images, gold_images)

# load image for exit portal
filename = 'assets/images/environment/Sprites/PNG/doors 2 type/portal-new.png'
exit_portal = pygame.image.load(filename).convert_alpha()

red_potion, blue_potion, green_potion = load_potions()

# group all items together
item_images = [coin_images, red_potion, blue_potion, green_potion, exit_portal, gold_images]

if constants.DEBUG_LEVEL:
    print(" line: {}. weapon images loaded".format(line_numb()))

# load character images (char_type)
mob_animations = []

# TODO combine mob_animations and image_dict, using just the image dict...

animation_types = ["idle", "run", "attack", "death"]
animation_list = []


def search_character_classes(name):
    for i, char in enumerate(character_classes):
        if char["name"] == name:
            return i
    return -1  # Return -1 if character not found


if constants.DEBUG_LEVEL > 1:
    print(" MAIN.PY, line: {}\n  Processing {} Characters".format(line_numb(), len(character_classes)))
    for character in character_classes:
        print("   character: {}".format(character['name']))


def load_files(directory, prefix, file_array):
    count = 0
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith(".png"):
            try:
                number = int(filename[4:8])
                file_path = os.path.join(directory, filename)
                file_array.append(file_path)
                count += 1
            except ValueError:
                if constants.DEBUG_LEVEL:
                    print(" MAIN.PY, F:load_files, line:{} Skipping {}".format(line_numb(), filename))
                pass  # ignore files with invalid number format
    return count


start_time = pygame.time.get_ticks()
# Load all character images (player and enemies)
if constants.DEBUG_LEVEL:
    print(" MAIN.PY, line: {}\n  Loading Character images".format(line_numb()))

for i, character in enumerate(character_classes):
    if constants.DEBUG_LEVEL:
        new_time = pygame.time.get_ticks()
        if i:
            print(new_time - start_time)
        if constants.DEBUG_LEVEL > 1:
            print("line={}, i={}, character={}".format(line_numb(), i, character))
        else:
            print("   Character={}, Load Time= ".format(character['name']), end="")
        # print("\t\tStart time= {}".format(start_time), end="")
        start_time = pygame.time.get_ticks()

    # reset temporary list of images
    temp_list = []
    animation_list = []

    match character['name']:
        case "Bear":
            for animation in animation_types:
                at = animation
                temp_list = []

                num_images = character[animation] + 1

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    match animation:
                        case "run":
                            at = animation.capitalize()
                            file_prefix = "bear_run"
                        case "idle":
                            file_prefix = "bear_idle"
                        case "attack":
                            file_prefix = "bear_attack"
                        case "death":
                            file_prefix = "bear_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{animation}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    # crops off wasted space around images, new_x, new_y, new width, new height
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Crocodile Warrior":  # tilesheet, done
            path = "assets/images/characters/Crocodile Warrior/x320_Spritesheets"
            for animation in animation_types:
                temp_list = []

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(f"{path}/Idle1_L.png", 600, 320, 5, 4)
                    case "attack":
                        images = Tilesheet(f"{path}/Attack1_L.png", 600, 320, 5, 4)
                    case "death":
                        images = Tilesheet(f"{path}/Death1_L.png", 600, 320, 6, 4)
                    case "run":
                        images = Tilesheet(f"{path}/Walk_Forward_L.png", 600, 320, 5, 4)
                    case _:
                        images = ""

                trim_rect = character['trim_rect']

                for y in range(images.rows):
                    for x in range(images.cols):
                        img = images.get_tile(x, y)

                        width = img.get_width() - (trim_rect[0] + trim_rect[1])
                        height = img.get_height() - (trim_rect[2] + trim_rect[3])
                        new_region = (trim_rect[0], trim_rect[2], width, height)
                        cropped_img = img.subsurface(new_region)

                        cropped_img = pygame.transform.flip(cropped_img, character['flip_image'], False)

                        if character['scale'] != 1:
                            cropped_img = scale_img(cropped_img, character['scale'])
                        temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Crab Monster":  # Tilesheet, done
            path = "assets/images/characters/Crab Monster/x320p_Spritesheets"
            for animation in animation_types:
                temp_list = []
                scale = character['scale']

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(f"{path}/Idle2.png", 512, 320, 8, 5)
                        trim_rect = character['trim_rect']
                    case "attack":
                        images = Tilesheet(f"{path}/Attack1.png", 320, 200, 5, 4)
                        trim_rect = character['trim_rect_320']
                        scale = 1.5  # needed to size up the 320 pixel images
                    case "death":
                        images = Tilesheet(f"{path}/Death1.png", 512, 320, 6, 5)
                        trim_rect = character['trim_rect']
                    case "run":
                        images = Tilesheet(f"{path}/Walk_Forward.png", 512, 320, 4, 5)
                        trim_rect = character['trim_rect']

                for y in range(images.rows):
                    for x in range(images.cols):
                        img = images.get_tile(x, y)

                        width = img.get_width() - (trim_rect[0] + trim_rect[1])
                        height = img.get_height() - (trim_rect[2] + trim_rect[3])
                        new_region = (trim_rect[0], trim_rect[2], width, height)
                        cropped_img = img.subsurface(new_region)

                        cropped_img = pygame.transform.flip(cropped_img, character['flip_image'], False)

                        if character['scale'] != 1:
                            cropped_img = scale_img(cropped_img, character['scale'])
                        temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Cyclops1" | "Cyclops2" | "Cyclops3":
            for animation in animation_types:
                temp_list = []
                scale = character['scale']
                num_images = character[animation] - 1

                for image_num in range(1, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                            scale = .3
                        case "idle":
                            file_prefix = "Idle"
                            scale = .3
                        case "attack":
                            file_prefix = "Attack"
                            scale = .3
                        case "death":
                            file_prefix = "Dead"
                            scale = .3
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    w = img.get_width()
                    h = img.get_height()

                    if scale != 1:
                        img = scale_img(img, scale)
                    nw = img.get_width()
                    nh = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Deer":  # Done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation.capitalize()

                    match animation:
                        case "run":
                            file_prefix = "deer_run"
                        case "idle":
                            file_prefix = "deer_idle"
                        case "attack":
                            file_prefix = "deer_attack"
                        case "death":
                            at = "Die"
                            file_prefix = "deer_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Dragon1" | "Dragon2" | "Dragon3":
            for animation in animation_types:
                num_images= character[animation] -1
                if animation == "run":
                    num_images = character['fly']
                temp_list = []
                scale = character['scale']
                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Flight"
                            scale = .3
                        case "idle":
                            file_prefix = "Idle"
                            scale = .3
                        case "attack":
                            file_prefix = "Attack"
                            scale = .3
                        case "death":
                            file_prefix = "Dead"
                            scale = .3
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    w = img.get_width()
                    h = img.get_height()

                    if scale != 1:
                        img = scale_img(img, scale)
                    nw = img.get_width()
                    nh = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Little Demon":  # Done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(1, num_images):
                    file_index = "{}".format(image_num)
                    at = animation.capitalize()

                    match animation:
                        case "run":
                            file_prefix = "Walk"
                        case "idle":
                            file_prefix = "Idle"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            at = "Die"
                            file_prefix = "Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/Little Demon/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Eagle":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation
                    match animation:
                        case "run":
                            at = "Fly"
                            file_prefix = "eagle_fly"
                        case "idle":
                            file_prefix = "eagle_idle"
                        case "attack":
                            file_prefix = "eagle_attack"
                        case "death":
                            at = "die"
                            file_prefix = "eagle_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Elemental1" | "Elemental2" | "Elemental3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "3_FLY"
                        case "idle":
                            file_prefix = "1_IDLE"
                        case "attack":
                            file_prefix = "5_ATTACK"
                        case "death":
                            file_prefix = "7_DIE"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Fox":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):

                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "fox_run"
                        case "idle":
                            file_prefix = "fox_idle"
                        case "attack":
                            file_prefix = "fox_attack"
                        case "death":
                            at = "die"
                            file_prefix = "fox_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Gaerron":  # Tilesheet, done
            for animation in animation_types:
                temp_list = []

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_idle1.png", 128, 128,
                                           4, 3, 0)  # 3 images, row 4
                        flip = character['flip_image']
                    case "attack":
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_MVsv_alt_attack2.png",
                                           128, 128, 1, 3, 0)  # 3 images, row 4
                        flip = True
                    case "death":
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_dead.png", 128, 128, 4,
                                           3, 3)  # 3 images, row 4
                    case "run":
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_walking.png", 128, 128,
                                           4, 8, 2)  # 8 images, row 3
                    case _:
                        images = ""

                trim_rect = character['trim_rect']

                for x in range(images.cols):
                    img = images.get_tile(x, 0)

                    width = img.get_width() - (trim_rect[0] + trim_rect[1])
                    height = img.get_height() - (trim_rect[2] + trim_rect[3])
                    new_region = (trim_rect[0], trim_rect[2], width, height)
                    cropped_img = img.subsurface(new_region)

                    cropped_img = pygame.transform.flip(cropped_img, flip, False)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Goat":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):

                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "goat_run"
                        case "idle":
                            file_prefix = "goat_idle"
                        case "attack":
                            file_prefix = "goat_attack"
                        case "death":
                            at = "die"
                            file_prefix = "goat_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Goblin1" | "Goblin2" | "Goblin3":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []
                num_images= character[animation]

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                        case "idle":
                            file_prefix = "Idle"
                            # file_prefix = "Attack1"
                        case "attack":
                            file_prefix = "Attack1"
                        case "death":
                            file_prefix = "Dead"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/Goblin/PNG/{character['name']}/Animation/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "GHOST1" | "GHOST2" | "GHOST3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                            at = "RUN"
                        case "idle":
                            file_prefix = "IDLE"
                            at = "IDLE"
                        case "attack":
                            file_prefix = "ATTACK1"
                            at = "ATTACK1"
                        case "death":
                            file_prefix = "DIE"
                            at = "DIE"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Golem1" | "Golem2" | "Golem3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(0, num_images):
                    num_images = character[animation]

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                        case "idle":
                            file_prefix = "Idle"
                            # file_prefix = "Attack1"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            file_prefix = "Dead"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    w = img.get_width()
                    h = img.get_height()

                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])
                    w = img.get_width()
                    h = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Insect":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images - 1):
                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Fly"
                            file_prefix = "Fly"
                        case "idle":
                            at = "Fly"
                            file_prefix = "Fly"
                        case "attack":
                            at = "Attack1"
                            file_prefix = "Attack1"
                        case "death":
                            at = "Death"
                            file_prefix = "Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/512x512/{at}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Jinn":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(1, num_images):

                    file_index = "{:01}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Flight"
                        case "idle":
                            file_prefix = "Idle"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            file_prefix = "Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Knight Man":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images - 1):
                    file_index = "{:04}".format(image_num + 1)
                    at = animation

                    match animation:
                        case "run":
                            at = "R_Run"
                            file_prefix = "R_Run"
                        case "idle":
                            at = "R_Idle"
                            angle = "180"
                            file_prefix = "R_Idle"
                        case "attack":
                            at = "R_Slash_1"
                            file_prefix = "R_Slash_1"
                        case "death":
                            at = "R_Death_Backward"
                            file_prefix = "R_Death_Backward"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Animations_Frames_512x512/{at}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Lord Esther":  # Tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/lordesther/LordEsther_idle1.png", 128, 128, 4,
                                           3)  # 3 images, row 1
                        flip = False
                    case "attack":
                        images = Tilesheet("assets/images/characters/lordesther/LordEsther_MVsv_alt_attack1.png",
                                           128, 128, 1, 3)
                    case "death":
                        images = Tilesheet("assets/images/characters/lordesther/LordEsther_MVsv_alt_dead1.png",
                                           128, 128, 1, 3)
                    case "run":
                        images = Tilesheet("assets/images/characters/lordesther/LordEsther_walking.png",
                                           128, 128, 4, 8, 2)  # 8 images, row 3
                        flip = False
                for x in range(images.cols):
                    img = images.get_tile(x, 0)

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    # crops off wasted space around images, new_x, new_y, new width, new height
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    cropped_img = pygame.transform.flip(cropped_img, flip, False)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Magic Fox":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(1, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "Run"
                        case "idle":
                            at = "Idle"
                            file_prefix = "Idle"
                        case "attack":
                            at = "Attack"
                            file_prefix = "Attack"
                        case "death":
                            at = "Death"
                            file_prefix = "Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/512x512/{at}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)

                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Meerkat":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "meerkat_run"
                        case "idle":
                            file_prefix = "meerkat_idle"
                        case "attack":
                            file_prefix = "meerkat_attack"
                        case "death":
                            at = "die"
                            file_prefix = "meerkat_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Minotaur1" | "Minotaur2" | "Minotaur3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                        case "idle":
                            file_prefix = "Idle"
                            # file_prefix = "Attack1"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            file_prefix = "Dead"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Orc1" | "Orc2" | "Orc3":
            for animation in animation_types:
                temp_list = []
                scale = character['scale']
                num_images = character[animation]
                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                            scale = .3
                        case "idle":
                            file_prefix = "Idle"
                            scale = .3
                        case "attack":
                            file_prefix = "Attack"
                            scale = .3
                        case "death":
                            file_prefix = "Dead"
                            scale = .3
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    w = img.get_width()
                    h = img.get_height()

                    if scale != 1:
                        img = scale_img(img, scale)
                    nw = img.get_width()
                    nh = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Panther":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "panther_run"
                        case "idle":
                            file_prefix = "panther_idle"
                        case "attack":
                            file_prefix = "panther_attack"
                        case "death":
                            at = "die"
                            file_prefix = "panther_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "PrinceTaerron":  # Tilesheet
            for animation in animation_types:
                temp_list = []

                flip = character['flip_image']
                trim_rect = character['trim_rect']

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_idle1.png", 512, 512,
                            4, 3, 0)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_MVsv_alt_attack2.png",
                            512, 512, 1, 3, 0)  # 3 images, row 1
                        flip = True
                    case "death":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_ko.png", 512, 512, 4,
                            3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_running.png", 512,
                            512, 4, 8, 2)  # 3 images, row 1
                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    width = img.get_width() - (trim_rect[0] + trim_rect[1])
                    height = img.get_height() - (trim_rect[2] + trim_rect[3])
                    new_region = (trim_rect[0], trim_rect[2], width, height)
                    cropped_img = img.subsurface(new_region)

                    cropped_img = pygame.transform.flip(cropped_img, flip, False)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Raven":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation.capitalize()

                    match animation:
                        case "run":
                            at = "Fly"
                            file_prefix = "raven_fly"
                        case "idle":
                            file_prefix = "raven_idle"
                        case "attack":
                            file_prefix = "raven_attack"
                        case "death":
                            at = "Die"
                            file_prefix = "raven_die"
                        case _:
                            file_prefix = ""
                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Red Demon":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                trim_rect = character['trim_rect']
                match animation:
                    case "run":
                        images = Tilesheet("assets/images/characters/red demon/Walk Body 090.png", 256, 256, 5, 4)
                    case "idle":
                        images = Tilesheet("assets/images/characters/red demon/Idle Body 180.png", 256, 256, 4, 6)
                    case "attack":
                        images = Tilesheet("assets/images/characters/red demon/Attack1 Body 090.png", 256, 256, 5, 4)
                    case "death":
                        images = Tilesheet("assets/images/characters/red demon/Death Body 090.png", 256, 256, 5, 6)

                for y in range(images.rows):
                    for x in range(images.cols):
                        img = images.get_tile(x, y)
                        width = img.get_width() - (trim_rect[0] + trim_rect[1])
                        height = img.get_height() - (trim_rect[2] + trim_rect[3])
                        new_region = (trim_rect[0], trim_rect[2], width, height)
                        cropped_img = img.subsurface(new_region)

                        cropped_img = pygame.transform.flip(cropped_img, flip, False)

                        if character['scale'] != 1:
                            cropped_img = scale_img(cropped_img, character['scale'])
                        temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Reptile Warrior":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images - 1):
                    file_index = "{:04}".format(image_num + 1)
                    at = animation
                    angle = "090"

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "Run_Body"
                        case "idle":
                            at = "Idle"
                            angle = "180"
                            file_prefix = "Idle_Body"
                        case "attack":
                            at = "Attack1"
                            file_prefix = "Attack1_Body"
                        case "death":
                            at = "Death"
                            file_prefix = "Death_Body"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{at}/Body/{angle}/{file_prefix}_{angle}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Saurial":
            for animation in animation_types:
                temp_list = []
                match animation:
                    case "run":
                        # we just want the 3rd row of images so we use start_index of 2
                        # 8 cols, 4 rows, select 3rd row
                        images = Tilesheet("assets/images/characters/Saurial/Saurial_running.png", 200, 200, 4, 8, 2)
                    case "idle":
                        images = Tilesheet("assets/images/characters/Saurial/Saurial_idle.png", 200, 200, 4,
                                           3)  # 3 cols, 4 rows
                    case "attack":
                        images = Tilesheet("assets/images/characters/Saurial/Saurial_flying.png", 200, 200, 4, 8,
                                           1)  # 3 cols, 4 rows
                    case "death":
                        images = Tilesheet("assets/images/characters/Saurial/Saurial_ko.png", 200, 200, 4, 3,
                                           1)  # 3 cols, 4 rows, 2nd row
                    case _:
                        if constants.DEBUG_LEVEL:
                            print("  MAIN.PY, line:{}\n   error loading Saurial".format(line_numb()))
                        pygame.quit()
                        sys.exit()

                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])
                    right_crop_percent = .7  # trims off 27% from left of demon
                    y_crop_percent = 0  # trims off from top of demon
                    drx = 0
                    dry = 0
                    drw = img.get_width() * right_crop_percent
                    drh = img.get_height() * (1 - (2 * y_crop_percent))

                    region = (
                        10, 10, img.get_width() - 15,
                        img.get_height() - 15)  # crops off wasted space around demon images
                    cropped_img = img.subsurface(region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Skeleton":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                trim_rect = character['trim_rect']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/Skeleton/x240p_Spritesheets/Idle_Lookup_Right.png",
                                           320, 240, 5, 6)
                    case "attack":
                        images = Tilesheet("assets/images/characters/Skeleton/x240p_Spritesheets/Attack_Combo_Left.png",
                                           320, 240, 6, 7)
                        flip = True
                    case "death":
                        images = Tilesheet(
                            "assets/images/characters/Skeleton/x240p_Spritesheets/Death_Backward_Left.png",
                            320, 240, 6, 4)
                    case "run":
                        images = Tilesheet("assets/images/characters/Skeleton/x240p_Spritesheets/Walk_Right.png",
                                           320, 240, 5, 4)

                for y in range(images.rows):
                    for x in range(images.cols):
                        img = images.get_tile(x, y)

                        width = img.get_width() - (trim_rect[0] + trim_rect[1])
                        height = img.get_height() - (trim_rect[2] + trim_rect[3])
                        new_region = (trim_rect[0], trim_rect[2], width, height)
                        cropped_img = img.subsurface(new_region)

                        cropped_img = pygame.transform.flip(cropped_img, flip, False)

                        if character['scale'] != 1:
                            cropped_img = scale_img(cropped_img, character['scale'])
                        temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Skeleton2" | "Skeleton3" | "Skeleton4":
            for animation in animation_types:
                temp_list = []
                scale = character['scale']
                for image_num in range(0, num_images):
                    num_images = character[animation]

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                        case "idle":
                            file_prefix = "Idle"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            file_prefix = "Dead"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    w = img.get_width()
                    h = img.get_height()

                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])
                    nw = img.get_width()
                    nh = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Snake":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "snake_run"
                        case "idle":
                            file_prefix = "snake_idle"
                        case "attack":
                            file_prefix = "snake_attack"
                        case "death":
                            at = "die"
                            file_prefix = "snake_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "SunkenGod":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_idle1.png",
                                           512, 512, 4, 3, 0)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_MVsv.png", 512,
                                           512, 6, 9, 1)  # 3 images, row 1
                        flip = True
                    case "death":
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_ko.png", 512,
                                           512, 4, 3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_running.png",
                                           512, 512, 4, 8, 2)  # 3 images, row 1
                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    cropped_img = pygame.transform.flip(cropped_img, flip, False)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "TheOldKing":  # Tilesheet, Done
            for animation in animation_types:
                temp_list = []

                flip = character['flip_image']
                trim_rect = character['trim_rect']

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_idle.png",
                                           512, 512, 4, 3, 1)  # 3 images, row 1
                        flip = True
                    case "attack":
                        images = Tilesheet("assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_MVsv.png",
                                           512, 512, 6, 9, 1)  # 3 images, row 1
                    case "death":
                        images = Tilesheet("assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_ko.png", 512,
                                           512, 4, 3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet("assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_walking.png",
                                           512, 512, 4, 8, 2)  # 3 images, row 1
                        flip = False
                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    width = img.get_width() - (trim_rect[0] + trim_rect[1])
                    height = img.get_height() - (trim_rect[2] + trim_rect[3])
                    new_region = (trim_rect[0], trim_rect[2], width, height)
                    cropped_img = img.subsurface(new_region)

                    cropped_img = pygame.transform.flip(cropped_img, flip, False)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "TheTriplets":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_idle1.png",
                                           512, 512, 4, 3)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_MVsv_alt_attack2.png",
                            512, 512, 1, 3)  # 3 images, row 1
                        flip = True
                    case "death":
                        images = Tilesheet(
                            "assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_MVsv_alt_attack2.png",
                            512, 512, 1, 3)  # 3 images, row 1
                    case "run":
                        images = Tilesheet(
                            "assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_running.png", 512, 512, 4,
                            8, 2)  # 3 images, row 1
                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    cropped_img = pygame.transform.flip(cropped_img, flip, False)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Thief":
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images - 1):
                    file_index = "{:04}".format(image_num + 1)
                    at = animation

                    match animation:
                        case "run":
                            at = "Run"
                            file_prefix = "Run"
                        case "idle":
                            at = "Idle"
                            angle = "180"
                            file_prefix = "Idle"
                        case "attack":
                            at = "Attack1"
                            file_prefix = "Attack1"
                        case "death":
                            at = "Death"
                            file_prefix = "Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/512x512/{at}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    left_crop_pixels = 90  # trims off
                    #                    right_crop_pixels = 140
                    right_crop_pixels = 10
                    top_crop_pixels = 60  # trims off from top
                    bottom_crop_pixels = 140

                    ix = img.get_width()
                    ih = img.get_height()
                    drx = left_crop_pixels
                    dry = top_crop_pixels
                    drw = img.get_width() - (left_crop_pixels + right_crop_pixels)
                    drh = img.get_height() - (top_crop_pixels + bottom_crop_pixels)
                    new_region = (drx, dry, drw, drh)  # crops off wasted space around images
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Undead1" | "Undead2" | "Undead3":
            if character['name'] == "Undead1":
                prefix = "5_animation"
            elif character['name'] == "Undead2":
                prefix = "6_animation"
            else:
                prefix = "7_animation"

            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(1, num_images):

                    file_index = "{:03}".format(image_num)

                    match animation:
                        case "run":
                            file_prefix = "walk"
                        case "idle":
                            file_prefix = "idle"
                        case "attack":
                            file_prefix = "attack"
                        case "death":
                            file_prefix = "hurt"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{prefix}_{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Warrior":  # player
            for animation in animation_types:
                temp_list = []
                if constants.DEBUG_LEVEL > 1:
                    print(" MAIN.PY, line={}, character['name']={}, animation={}".
                          format(line_numb(), character['name'], animation))

                at = animation
                num_images = character[animation] + 1

                for image_num in range(0, num_images):
                    file_index = "{:02}".format(image_num)

                    match animation:
                        case "run":
                            at = animation.capitalize()
                            file_prefix = "Armature_Walk"
                        case "idle":
                            file_prefix = "Armature_idle"
                        case "attack":
                            file_prefix = "Armature_Attack"
                        case "death":
                            file_prefix = "Armature_Death"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/{animation}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    if animation == "attack":
                        drx = 260
                        dry = 310
                        drw = img.get_width() - drx
                        drh = img.get_height() - dry
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images

                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'])

                        temp_list.append(cropped_img)
                    elif animation == "death":
                        drx = 65
                        dry = 45
                        drw = img.get_width() - drx
                        drh = img.get_height() - dry
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images

                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'])

                        temp_list.append(cropped_img)
                    else:
                        left_crop_pixels = 0  # trims off
                        right_crop_pixels = 25
                        top_crop_pixels = 0  # trims off from top
                        bottom_crop_pixels = 0

                        ix = img.get_width()
                        ih = img.get_height()
                        drx = left_crop_pixels
                        dry = top_crop_pixels
                        drw = img.get_width() - (left_crop_pixels + right_crop_pixels)
                        drh = img.get_height() - (top_crop_pixels + bottom_crop_pixels)
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images
                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'])
                        temp_list.append(cropped_img)

                animation_list.append(temp_list)
        case "Witch":
            for animation in animation_types:
                temp_list = []

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_idle1.png", 512, 512,
                                           4, 3)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_MVsv_alt_attack2.png",
                                           512, 512, 1, 3)  # 3 images, row 1
                    case "death":
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_dead.png", 512, 512, 1,
                                           3)  # 3 images, row 1
                    case "run":
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_running.png", 512, 512,
                                           4, 8, 2)  # 3 images, row 1
                for x in range(images.cols):
                    img = images.get_tile(x, 0)
                    left_crop_pixels = 0  # trims off
                    right_crop_pixels = 0
                    top_crop_pixels = 0  # trims off from top
                    bottom_crop_pixels = 0

                    drx = left_crop_pixels
                    dry = top_crop_pixels
                    drw = img.get_width() - (left_crop_pixels + right_crop_pixels)
                    drh = img.get_height() - (top_crop_pixels + bottom_crop_pixels)
                    new_region = (drx, dry, drw, drh)  # crops off wasted space around images
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Wolf":  # done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    at = animation.capitalize()
                    match animation:
                        case "run":
                            file_prefix = "wolf_run"
                        case "idle":
                            file_prefix = "wolf_idle"
                        case "attack":
                            file_prefix = "wolf_attack"
                        case "death":
                            at = "die"
                            file_prefix = "wolf_die"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)

                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case "Zombie1" | "Zombie2" | "Zombie3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(1, num_images):

                    file_index = str(image_num)

                    match animation:
                        case "run":
                            file_prefix = "Run"
                        case "idle":
                            file_prefix = "Idle"
                            # file_prefix = "Attack1"
                        case "attack":
                            file_prefix = "Attack"
                        case "death":
                            file_prefix = "Dead"
                        case _:
                            file_prefix = ""

                    path = f"assets/images/characters/Zombie/{character['name']}/Animation/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    w = img.get_width()
                    h = img.get_height()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    w = cropped_img.get_width()
                    h = cropped_img.get_height()

                    temp_list.append(cropped_img)
                animation_list.append(temp_list)
        case _:
            print("   MAIN.PY, line={}\nFailed loading images for {}".format(line_numb(), character['name']))
            if constants.DEBUG_LEVEL == 0:
                pygame.quit()
                sys.exit()


    if (constants.DEBUG_LEVEL > 1):
        print(" line: {},  animation={}".format(line_numb(), animation))
    mob_animations.append(animation_list)

if constants.DEBUG_LEVEL:  # print the last load time stat
    print(new_time - start_time)

animation = ""
animation_list = []
if constants.DEBUG_LEVEL:
    print("\n  Images for player and {} enemies loaded\n".format(i))


def draw_character(image, x, y):
    screen.blit(image, (x, y))


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for displaying game info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    # draw lives
    half_heart_drawn = False
    health_percentage = player.health / constants.PLAYER_START_HEALTH * 100
    for i in range(5):
        if health_percentage >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (health_percentage % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    # HP
    draw_text("HP: " + str(player.health), font, constants.WHITE, 260, 15)
    # level
    draw_text("LEVEL: " + str(level), font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)

    # exp
    draw_text("EXP: " + str(player.exp), font, constants.WHITE, constants.SCREEN_WIDTH / 2 + 185, 15)

    # show score
    draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)


# function to reset level
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()
    lightning_group.empty()
    sprite_group.empty()

    # create empty tile list
    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLS
        data.append(r)

    return data


# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


# class for handling screen fade
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.colour,
                             (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (
                constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (
                0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


# load in the level data
if constants.DEBUG_LEVEL:
    # path = "assets/levels/testing.tmx"
    # path= "/Users/tomfrancis/IdeaProjects/Final_game/assets/levels/testing.tmx"
    path = "assets/levels/level1.tmx"

else:
    path = "assets/levels/level1.tmx"

if constants.DEBUG_LEVEL:
    print("MAIN.PY, line:{}, Loading TMX_MAP file: {}".format(line_numb(), path))

try:
    tmx_map = load_pygame(path)

except:
    print("MAIN.PY line:{}\n Unable to load TMX file: {}".format(line_numb(), path))
    pygame.quit()
    exit()

# start FPS monitoring

# Create World
if constants.DEBUG_LEVEL:
    if constants.FPS_MONITOR:
        fps = FPS()
    print(" MAIN.PY, line={}\n   Creating World\n".format(line_numb()))

world = World(character_classes)

# sprite_group = pygame.sprite.Group()
sprite_group = pygame.sprite.LayeredUpdates()

success = world.process_data(tmx_map, item_images, mob_animations, sprite_group)
if not success:
    print(" MAIN.PY, line:{}, world.process_data failed".format(line_numb()))
    pygame.quit()
    sys.exit()

if constants.DEBUG_LEVEL:
    print(" MAIN.PY, line={}\n   World Created".format(line_numb()))

# create player
player = world.player

# create player's weapon
bow = Weapon(bow_image, arrow_image)
# sword = Sword(sword_image)

# extract enemies from world data
enemy_list = world.character_list

# create sprite groups
damage_text_group = pygame.sprite.LayeredUpdates()
arrow_group = pygame.sprite.LayeredUpdates()
item_group = pygame.sprite.LayeredUpdates()
fireball_group = pygame.sprite.LayeredUpdates()
lightning_group = pygame.sprite.LayeredUpdates()
# damage_text_group = pygame.sprite.Group()
# arrow_group = pygame.sprite.Group()
# item_group = pygame.sprite.Group()
# fireball_group = pygame.sprite.Group()
# lightning_group = pygame.sprite.Group()

score_status = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
item_group.add(score_status)
blue_potion_status = Item(constants.SCREEN_WIDTH - 225, 23, 2, blue_potion, True)
green_potion_status = Item(constants.SCREEN_WIDTH - 300, 23, 3, green_potion, True)
item_group.add(blue_potion_status)
item_group.add(green_potion_status)

# add the items from the level data
for item in world.item_list:
    item_group.add(item)

# create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 8)
death_fade = ScreenFade(2, constants.PINK, 8)

# create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

if constants.DEBUG_LEVEL:
    print("MAIN.PY, line: {}\n\nStats:\n {} tiles\n {} objects\n {} enemies".format(line_numb(), len(world.map_tiles),
                                                                                    len(item_group), len(enemy_list)))
    print(
        "    c.rows= {}, map width= {}, c.cols={}, map height= {}".format(constants.ROWS, tmx_map.width, constants.COLS,
                                                                          tmx_map.height))
    print("\n\nSTARTING MAIN LOOP\n")

# main game loop
run = True
level_complete = False
loop_number = 0
damage_text = ""

while run:
    loop_number += 1
    # control frame rate
    clock.tick(constants.FPS)

    if constants.DEBUG_LEVEL > 1:
        print("  line: {}, loop_number={}, level_complete={}, run={}, start_game={}\n"
              "     moving_up={}, moving_down={}, moving_left={}, moving_right={}".
              format(line_numb(), loop_number, level_complete, run, start_game,
                     moving_up, moving_down, moving_left, moving_right))

    if start_game == False and constants.DEBUG_LEVEL == 0:
        screen.fill(constants.MENU_BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game:
            if constants.DEBUG_LEVEL:
                screen.fill(constants.MENU_BG)
            if resume_button.draw(screen):
                pause_game = False
            if exit_button.draw(screen):
                run = False
        else:
            screen.fill(constants.BG)

            if player.alive:
                # calculate player movement
                dx = 0
                dy = 0
                if moving_right == True:
                    dx = constants.PLAYER_SPEED
                if moving_left == True:
                    dx = -constants.PLAYER_SPEED
                if moving_up == True:
                    dy = -constants.PLAYER_SPEED
                if moving_down == True:
                    dy = constants.PLAYER_SPEED

                # move player
                screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)

                # update all objects
                world.update(screen_scroll)
                for enemy in enemy_list:
                    # TODO : why is fireball = enemy.ai run for every enemy?  How about lightning?
                    fireball, lightning = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image,
                                                   lightning_image, character_classes)
                    if fireball:
                        fireball_group.add(fireball)
                    if lightning:
                        lightning_group.add(lightning)

                    if enemy.alive:
                        enemy.update(player)

                player.update(player)
                arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:

                    damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)

                    if damage:
                        new_damage, current_health = damage.split(" : ")
                        new_damage = -(int(new_damage))
                        current_health = int(current_health)
                        # test

                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(new_damage), constants.RED)
                        damage_text_group.add(damage_text)

                        if current_health <= 0:
                            current_health = str("dead")
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y + 18, str(current_health),
                                                     constants.BLUE)
                        else:
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y + 18, str(current_health),
                                                     constants.GREEN)
                        damage_text_group.add(damage_text)
                        if constants.DEBUG_LEVEL > 1:
                            print(
                                " MAIN.PY, line:{}, Damage_text={}, damage={}".format(line_numb(), damage_text, damage))
                        hit_fx.play()

                damage_text_group.update()
                fireball_group.update(screen_scroll, player)
                lightning_group.update(screen_scroll, player)
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

                if player.level_complete:
                    level_complete = True
                    if constants.DEBUG_LEVEL:
                        print("MAIN.PY, line:{}, Level {} Completed".format(line_numb(), world.map_level))

            world.draw(screen)
            item_group.draw(screen)

            # draw player on screen
            player.draw(screen)
            bow.draw(screen)

            # draw enemies
            for enemy in enemy_list:
                if constants.DEBUG_LEVEL > 1:
                    print(" MAIN.PY, F:main loop, line={}, enemy.char_type={} ({})".
                          format(line_numb(), enemy.char_index, character_classes[enemy.char_index]['name']))
                    print("   enemy.image={}".format(enemy.image))
                enemy.draw(screen)

            # put player.draw here to have player on top of enemies, leave above for enemies to be on top.
            # player.draw(screen)

            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            for lightning in lightning_group:
                lightning.draw(screen)
            damage_text_group.draw(screen)
            draw_info()
            score_status.draw(screen)
            blue_potion_status.draw(screen)
            green_potion_status.draw(screen)

        # check level complete
        if level_complete == True:
            # print("MAIN.PY, line:{}\n Next level functionality has not been refactored".format(line_numb()))

            start_intro = True
            level += 1

            world_data = reset_level()

            path = "assets/levels/level{}.tmx".format(level)

            try:
                tmx_map = load_pygame(path)

            except:
                print("MAIN.PY line:{} Unable to load TMX file: {}".format(line_numb(), path))
                pygame.quit()
                exit()

            world = World()
            success = world.process_data(tmx_map, item_images, mob_animations, sprite_group)
            if not success:
                print("  world.process_data failed")
                pygame.quit()
                sys.exit()

            temp_hp = player.health
            temp_score = player.score
            player = world.player
            player.health = temp_hp
            player.score = temp_score
            enemy_list = world.character_list

            # add the items from the level data
            for item in world.item_list:
                item_group.add(item)

        # show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # show death screen
        if player.alive == False:
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    start_game = True
                    world_data = reset_level()

                    path = "assets/levels/level{}.tmx".format(level)
                    #            path = "assets/levels/testing.tmx"

                    try:
                        tmx_map = load_pygame(path)

                    except:
                        print("MAIN.PY line:{} Unable to load TMX file: {}".format(line_numb(), path))
                        pygame.quit()
                        exit()

                    world = World()
                    success = world.process_data(tmx_map, item_images, mob_animations, sprite_group)
                    if not success:
                        print("  world.process_data failed in MAIN.PY, line:{}".format(line_numb()))
                        pygame.quit()
                        sys.exit()

                    temp_hp = player.health
                    temp_score = player.score
                    player = world.player
                    enemy_list = world.character_list
                    score_status = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
                    item_group.add(score_status)
                    blue_potion_status = Item(constants.SCREEN_WIDTH - 225, 23, 2, blue_potion, True)
                    green_potion_status = Item(constants.SCREEN_WIDTH - 300, 23, 3, green_potion, True)
                    item_group.add(blue_potion_status)
                    item_group.add(green_potion_status)
                    # add the items from the level data
                    for item in world.item_list:
                        item_group.add(item)
                    print("")

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a:
                    moving_left = True
                case pygame.K_d:
                    moving_right = True
                case pygame.K_w:
                    moving_up = True
                case pygame.K_s:
                    moving_down = True
                case pygame.K_ESCAPE:
                    pause_game = True

        # keyboard button released

        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_a:
                    moving_left = False
                case pygame.K_d:
                    moving_right = False
                case pygame.K_w:
                    moving_up = False
                case pygame.K_s:
                    item_group.update(screen_scroll, player, coin_fx, heal_fx)

            moving_down = False

    if god_mode:
        if player and player.health < 50:
            player.health = constants.PLAYER_START_HEALTH

    # show fps
    if constants.FPS_MONITOR:
        fps.render(screen, str(level))
        fps.clock.tick(constants.FPS)

        # sort sprites by ascending _layer
    # for sprite in sorted(, key=lambda x: x._layer):
    #     # and then paint
    #     screen.blit(sprite.image, sprite.rect)

    pygame.display.update()

pygame.quit()
