import inspect
import math
import random
import sys

from pygame.locals import *

import weapon
from support import *


def load_character_images(char_name, mob_dict, character_classes_dict):
    #    global character, animation_list, animation, path, y, x
    fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
    animation_types = ["idle", "run", "attack", "death"]
    start_time = pygame.time.get_ticks()
    number_of_images_loaded = 0

    character = character_classes_dict[char_name]
    if constants.DEBUG_LEVEL:
        start_time = pygame.time.get_ticks()

        print("Character={}".format(character['name']), end="")

    # reset temporary list of images
    animation_list = []

    match character['name']:
        case "Bear":  # edited
            for animation in animation_types:
                temp_list = []

                match animation:
                    case "run":
                        file_prefix = "bear_run"
                    case "idle":
                        file_prefix = "bear_idle"
                    case "attack":
                        file_prefix = "bear_attack"
                    case "death":
                        file_prefix = "bear_die"
                    case _:
                        file_prefix = ""

                num_images = character[animation] + 1
                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)
                    path = f"assets/images/characters/{character['name']}/{animation}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    # crops off wasted space around images, new_x, new_y, new width, new height
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Crocodile Warrior":  # tilesheet, done
            path = "assets/images/characters/Crocodile Warrior"
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
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Crab Monster":  # Tilesheet, done
            path = "assets/images/characters/Crab Monster"
            for animation in animation_types:
                temp_list = []
                scale = character['scale']

                match animation:
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
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(f"{path}/Idle2.png", 512, 320, 8, 5)
                        trim_rect = character['trim_rect']
                    case _:
                        images = ""

                for y in range(images.rows):
                    for x in range(images.cols):
                        img = images.get_tile(x, y)

                        width = img.get_width() - (trim_rect[0] + trim_rect[1])
                        height = img.get_height() - (trim_rect[2] + trim_rect[3])
                        new_region = (trim_rect[0], trim_rect[2], width, height)
                        cropped_img = img.subsurface(new_region)

                        cropped_img = pygame.transform.flip(cropped_img, character['flip_image'], False)

                        if scale != 1:
                            cropped_img = scale_img(cropped_img, scale)
                        temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)

        case "Cyclops1" | "Cyclops2" | "Cyclops3":
            scale = character['scale']
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation]

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if scale != 1:
                        cropped_img = scale_img(cropped_img, scale)

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Deer":  # Done
            for animation in animation_types:

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

                num_images = character[animation] + 1
                temp_list = []

                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Dragon1" | "Dragon2" | "Dragon3":
            for animation in animation_types:

                match animation:
                    case "run":
                        file_prefix = "Flight"
                    case "idle":
                        file_prefix = "Idle"
                    case "attack":
                        file_prefix = "Attack"
                    case "death":
                        file_prefix = "Dead"
                    case _:
                        file_prefix = ""

                temp_list = []
                scale = character['scale']

                num_images = character['fly'] if animation == "run" else character[animation] - 1

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    if scale != 1:
                        img = scale_img(img, scale)

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Little Demon":  # Done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                match animation:
                    case "run":
                        file_prefix = "Walk"
                    case "idle":
                        file_prefix = "Idle"
                    case "attack":
                        file_prefix = "Attack"
                    case "death":
                        file_prefix = "Death"
                    case _:
                        file_prefix = ""

                for image_num in range(1, num_images):
                    file_index = "{}".format(image_num)

                    path = f"assets/images/characters/Little Demon/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Little Dragon":  # Done
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

                match animation:
                    case "run":
                        file_prefix = "Walk"
                    case "idle":
                        file_prefix = "Idle"
                    case "attack":
                        file_prefix = "Attack"
                    case "death":
                        file_prefix = "Death"
                    case _:
                        file_prefix = ""

                for image_num in range(1, num_images):
                    file_index = "{}".format(image_num)

                    path = f"assets/images/characters/Little Dragon/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Eagle":  # done, edited
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation] + 1
                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Elemental1" | "Elemental2" | "Elemental3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

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

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Gaerron":  # Tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip']

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_idle1.png", 128,
                                           128, 4, 3, 0)  # 3 images, row 4
                        flip = character['flip_image']
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/MasterGaerron/MasterGaerron_MVsv_alt_attack2.png",
                            128, 128, 1, 3, 0)  # 3 images, row 4
                        flip = True
                    case "death":
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_dead.png", 128,
                                           128, 4, 3, 3)  # 3 images, row 4
                    case "run":
                        images = Tilesheet("assets/images/characters/MasterGaerron/MasterGaerron_walking.png", 128,
                                           128, 4, 8, 2)  # 8 images, row 3
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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Goat":  # done
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation] + 1
                for image_num in range(0, num_images):

                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Goblin1" | "Goblin2" | "Goblin3":
            for animation in animation_types:
                temp_list = []
                num_images = character[animation]

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

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/Goblin/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "GHOST1" | "GHOST2" | "GHOST3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

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
                        at = "ERROR"
                        file_prefix = ""

                for image_num in range(0, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Golem1" | "Golem2" | "Golem3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

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

                for image_num in range(0, num_images):
                    # num_images = character[animation]

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                    number_of_images_loaded += 1

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

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                            # angle = "180"
                            file_prefix = "R_Idle"
                        case "attack":
                            at = "R_Slash_1"
                            file_prefix = "R_Slash_1"
                        case "death":
                            at = "R_Death_Backward"
                            file_prefix = "R_Death_Backward"
                        case _:
                            file_prefix = ""

                    path = "assets/images/characters/{}/Animations_Frames_512x512/{}/{}_{}.png". \
                        format(character['name'], at, file_prefix, file_index)

                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                    case _:
                        images = ""

                for x in range(images.cols):
                    img = images.get_tile(x, 0)

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    # crops off wasted space around images, new_x, new_y, new width, new height
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    cropped_img = pygame.transform.flip(cropped_img, flip, False)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)

                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                    number_of_images_loaded += 1

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

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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

                    if scale != 1:
                        img = scale_img(img, scale)

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Panther":
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation] + 1
                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_idle1.png", 512,
                            512,
                            4, 3, 0)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_MVsv_alt_attack2.png",
                            512, 512, 1, 3, 0)  # 3 images, row 1
                        flip = True
                    case "death":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_ko.png", 512, 512,
                            4,
                            3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet(
                            "assets/images/characters/PrinceTaerron/Medieval_Bosses_PrinceTaerron_running.png", 512,
                            512, 4, 8, 2)  # 3 images, row 1
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Red Demon":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                trim_rect = character['trim_rect']
                flip = character['flip_image']

                match animation:
                    case "run":
                        images = Tilesheet("assets/images/characters/red demon/Walk Body 090.png", 256, 256, 5, 4)
                    case "idle":
                        images = Tilesheet("assets/images/characters/red demon/Idle Body 180.png", 256, 256, 4, 6)
                    case "attack":
                        images = Tilesheet("assets/images/characters/red demon/Attack1 Body 090.png", 256, 256, 5,
                                           4)
                    case "death":
                        images = Tilesheet("assets/images/characters/red demon/Death Body 090.png", 256, 256, 5, 6)
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Reptile Warrior":  # done, edited
            for animation in animation_types:
                num_images = character[animation] + 1
                temp_list = []

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

                for image_num in range(0, num_images - 1):
                    file_index = "{:04}".format(image_num + 1)

                    path = "assets/images/characters/{0}/{1}/Body/{2}/{3}_{2}_{4}.png". \
                        format(character['name'], at, angle, file_prefix, file_index)

                    img = pygame.image.load(path).convert_alpha()
                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Saurial":
            for animation in animation_types:
                temp_list = []
                match animation:
                    case "run":
                        # we just want the 3rd row of images, so we use start_index of 2
                        # 8 cols, 4 rows, select 3rd row
                        images = Tilesheet("assets/images/characters/Saurial/Saurial_running.png", 200, 200, 4, 8,
                                           2)
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

                    # crops off wasted space around demon images
                    region = (10, 10, img.get_width() - 15, img.get_height() - 15)
                    cropped_img = img.subsurface(region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Skeleton":  # tilesheet, done
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                trim_rect = character['trim_rect']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(
                            "assets/images/characters/Skeleton/x240p_Spritesheets/Idle_Lookup_Right.png",
                            320, 240, 5, 6)
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/Skeleton/x240p_Spritesheets/Attack_Combo_Left.png",
                            320, 240, 6, 7)
                        flip = True
                    case "death":
                        images = Tilesheet(
                            "assets/images/characters/Skeleton/x240p_Spritesheets/Death_Backward_Left.png",
                            320, 240, 6, 4)
                    case "run":
                        images = Tilesheet("assets/images/characters/Skeleton/x240p_Spritesheets/Walk_Right.png",
                                           320, 240, 5, 4)
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Skeleton2" | "Skeleton3" | "Skeleton4":
            for animation in animation_types:
                temp_list = []
                num_images = character[animation]
                for image_num in range(0, num_images - 1):

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

                    if character['scale'] != 1:
                        img = scale_img(img, character['scale'])

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Small Dragon":  # Done, edited
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                match animation:
                    case "run":
                        file_prefix = "Walk"
                    case "idle":
                        file_prefix = "Idle"
                    case "attack":
                        file_prefix = "Attack"
                    case "death":
                        file_prefix = "Death"
                    case _:
                        file_prefix = ""

                for image_num in range(1, num_images):
                    file_index = "{}".format(image_num)

                    path = f"assets/images/characters/Small Dragon/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Snake":  # done
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation] + 1
                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/Sprites/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_MVsv.png",
                                           512,
                                           512, 6, 9, 1)  # 3 images, row 1
                        flip = True
                    case "death":
                        images = Tilesheet("assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_ko.png",
                                           512,
                                           512, 4, 3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet(
                            "assets/images/characters/SunkenGod/Medieval_Bosses_SunkenGod_running.png",
                            512, 512, 4, 8, 2)  # 3 images, row 1
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "TheOldKing":  # Tilesheet, Done
            for animation in animation_types:
                temp_list = []

                flip = character['flip_image']
                trim_rect = character['trim_rect']

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(
                            "assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_idle.png",
                            512, 512, 4, 3, 1)  # 3 images, row 1
                        flip = True
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_MVsv.png",
                            512, 512, 6, 9, 1)  # 3 images, row 1
                    case "death":
                        images = Tilesheet("assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_ko.png",
                                           512, 512, 4, 3, 1)  # 3 images, row 1
                    case "run":
                        images = Tilesheet(
                            "assets/images/characters/TheOldKing/Medieval_Bosses_TheOldKing_walking.png",
                            512, 512, 4, 8, 2)  # 3 images, row 1
                        flip = False
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "TheTriplets":  # tilesheet, done
            animation_list.append(char_name)
            for animation in animation_types:
                temp_list = []
                flip = character['flip_image']
                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet(
                            "assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_idle1.png",
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
                            "assets/images/characters/TheTriplets/Medieval_Bosses_TheTriplets_running.png", 512,
                            512, 4,
                            8, 2)  # 3 images, row 1
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1

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
                            # angle = "180"
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

                    drx = left_crop_pixels
                    dry = top_crop_pixels
                    drw = img.get_width() - (left_crop_pixels + right_crop_pixels)
                    drh = img.get_height() - (top_crop_pixels + bottom_crop_pixels)
                    new_region = (drx, dry, drw, drh)  # crops off wasted space around images
                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Troll1" | "Troll2" | "Troll3":
            # animation_list.append(char_name)
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

                for image_num in range(0, num_images - 1):

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

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

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

                for image_num in range(1, num_images):

                    file_index = "{:03}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{prefix}_{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)
        case "Warrior":  # player
            for animation in animation_types:
                temp_list = []
                if constants.DEBUG_LEVEL > 1:
                    print(" MAIN.PY, line={}, character['name']={}, animation={}".
                          format(line_numb(), character['name'], animation))

                # at = animation
                num_images = character[animation] + 1

                match animation:
                    case "run":
                        # at = animation.capitalize()
                        file_prefix = "Armature_Walk"
                    case "idle":
                        file_prefix = "Armature_idle"
                    case "attack":
                        file_prefix = "Armature_Attack"
                    case "death":
                        file_prefix = "Armature_Death"
                    case _:
                        file_prefix = ""

                for image_num in range(0, num_images):
                    file_index = "{:02}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{animation}/{file_prefix}_{file_index}.png"

                    img = pygame.image.load(path).convert_alpha()

                    if animation == "attack":
                        drx = 260
                        dry = 310
                        drw = img.get_width() - drx
                        drh = img.get_height() - dry
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images

                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'], use_global_scale=False)

                        temp_list.append(cropped_img)
                        number_of_images_loaded += 1

                    elif animation == "death":
                        drx = 65
                        dry = 45
                        drw = img.get_width() - drx
                        drh = img.get_height() - dry
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images

                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'], use_global_scale=False)

                        temp_list.append(cropped_img)
                        number_of_images_loaded += 1

                    else:
                        left_crop_pixels = 0  # trims off
                        right_crop_pixels = 25
                        top_crop_pixels = 0  # trims off from top
                        bottom_crop_pixels = 0

                        drx = left_crop_pixels
                        dry = top_crop_pixels
                        drw = img.get_width() - (left_crop_pixels + right_crop_pixels)
                        drh = img.get_height() - (top_crop_pixels + bottom_crop_pixels)
                        new_region = (drx, dry, drw, drh)  # crops off wasted space around images
                        cropped_img = img.subsurface(new_region)
                        cropped_img = scale_img(cropped_img, character['scale'], use_global_scale=False)
                        temp_list.append(cropped_img)
                        number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Witch":
            for animation in animation_types:
                temp_list = []

                match animation:
                    case "idle":
                        # (filename, width, height, rows, cols, start_row_index= 0)
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_idle1.png", 512,
                                           512, 4, 3)  # 3 images, row 1
                    case "attack":
                        images = Tilesheet(
                            "assets/images/characters/Witch/Medieval_Bosses_Witch_MVsv_alt_attack2.png",
                            512, 512, 1, 3)  # 3 images, row 1
                    case "death":
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_dead.png", 512,
                                           512, 1, 3)  # 3 images, row 1
                    case "run":
                        images = Tilesheet("assets/images/characters/Witch/Medieval_Bosses_Witch_running.png", 512,
                                           512, 4, 8, 2)  # 3 images, row 1
                    case _:
                        images = ""

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
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Wolf":  # done, edited
            for animation in animation_types:
                temp_list = []

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

                num_images = character[animation] + 1
                for image_num in range(0, num_images):
                    file_index = "{:04}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{at}/{file_prefix}_{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)

                    cropped_img = img.subsurface(new_region)
                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case "Wraith1" | "Wraith2" | "Wraith3":
            for animation in animation_types:
                temp_list = []
                scale = character['scale']

                match animation:
                    case "run":
                        file_prefix = "move"
                    case "idle":
                        file_prefix = "Idle"
                    case "attack":
                        file_prefix = "Attack"
                    case "death":
                        file_prefix = "Dead"
                    case _:
                        file_prefix = ""

                num_images = character[animation] + 1
                for image_num in range(1, num_images):

                    file_index = "{:01}".format(image_num)

                    path = f"assets/images/characters/{character['name']}/{file_prefix}/{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    if scale != 1:
                        img = scale_img(img, scale)

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])

                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)
                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1

                animation_list.append(temp_list)

        case "Zombie1" | "Zombie2" | "Zombie3":
            for animation in animation_types:
                num_images = character[animation]
                temp_list = []

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

                for image_num in range(1, num_images):

                    file_index = str(image_num)

                    path = f"assets/images/characters/Zombie/{character['name']}/Animation/{file_prefix}{file_index}.png"
                    img = pygame.image.load(path).convert_alpha()

                    width = img.get_width() - (character['trim_rect'][0] + character['trim_rect'][1])
                    height = img.get_height() - (character['trim_rect'][2] + character['trim_rect'][3])
                    new_region = (character['trim_rect'][0], character['trim_rect'][2], width, height)
                    cropped_img = img.subsurface(new_region)

                    if character['scale'] != 1:
                        cropped_img = scale_img(cropped_img, character['scale'])

                    temp_list.append(cropped_img)
                    number_of_images_loaded += 1
                animation_list.append(temp_list)
        case _:
            print(f"\n  *ERROR: Failed loading images for {character['name']}")
            print(f"   MAIN.PY, F:{fn}, line={line_numb()}")
            if constants.DEBUG_LEVEL == 0:
                pygame.quit()
                sys.exit()

    end_time = pygame.time.get_ticks()
    if constants.DEBUG_LEVEL:
        print(" Load time={}".format(end_time - start_time))

    # final_list = char_name, animation_list
    mob_dict[char_name] = {"name": char_name, "images": animation_list}
    return number_of_images_loaded


def line_numb():
    '''Returns the current line number in our program'''
    return inspect.currentframe().f_back.f_lineno


def draw_health_bar(surf, rect, border_color, back_color, health_color, progress):
    size = rect.size
    pos = rect.topleft

    # shape_surf = surf.copy()

    # TODO to make status bar opaque, need to use SRCALPHA on surface.
    # def draw_rect_alpha(surface, color, rect):
    #     shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    #     pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    #     surface.blit(shape_surf, rect)

    # shape_surf = pygame.Surface(size, pygame.SRCALPHA)

    # pygame.draw.rect(shape_surf, back_color, (*pos, *size))
    # pygame.draw.rect(shape_surf, border_color, (*pos, *size), 1)
    # pygame.draw.rect(shape_surf, health_color, shape_surf.get_rect())

    # draw red background
    pygame.draw.rect(surf, back_color, (*pos, *size))

    # draw border
    pygame.draw.rect(surf, border_color, (*pos, *size), 1)
    # pygame.draw.rect(shape_surf, health_color, rect, 1)
    # surf.blit(shape_surf, rect)

    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(surf, health_color, rect)
    # pygame.draw.rect(shape_surf, back_color, shape_surf.get_rect())


class Character(pygame.sprite.Sprite):
    # def __init__(self, x, y, mob_dict, char_name, character_classes_dict, enemy_stats_sprite_group):
    def __init__(self, x, y, mob_dict, char_name, character_classes_dict):
        pygame.sprite.Sprite.__init__(self)
        fn = ""
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"

        if constants.DEBUG_LEVEL:
            print(f" CHAR.PY, F:{fn}, line:{line_numb()}, Creating new Character: {char_name}")

        # TODO: Need to on using centerx, centery to place objects NOT x,y due to stutter when switching from idle to attack.
        self.x = x
        self.y = y
        self.name = char_name

        if self.name not in character_classes_dict.keys():
            print("\nERROR: CHAR.PY: FN:{}, LN:{}, self.name={} does not exist in dict".format(fn, line_numb(),
                                                                                               self.name))
            pygame.quit()
            sys.exit()

        # set the special attack if avail, else None
        # TODO: why is a misssing attribute causing a crash?  Troll2 doesn't have the special attack, troll1 does
        self.special_attack = character_classes_dict[char_name]['Special_Attack']
        self.score = 0
        self.flip = False
        self.level_complete = False
        self.ghost = False
        self.health_potions = 3 if self.name == "player" else 0
        self.mana_potions = 3 if self.name == "player" else 0
        self.poison_potions = 3 if self.name == "player" else 0
        self.use_health_potion = False
        self.use_mana_potion = False
        self.use_poison_potion = False
        self.fading_counter = 0
        self.mana = 100
        self.poison = 0
        self.rank = 1

        # assign initial hitbox info
        self.hitbox = (0, 0, 0, 0)
        self.character_classes_dict = character_classes_dict

        if self.name == "player" and constants.DEBUG_GHOST_MODE_ON:
            self.ghost = True

        if self.name == "player" or self.name in character_classes_dict:
            pass
        else:
            print(
                "CHAR.PY, F:{}, line:{}, self.name={}\n\n  ERROR: object ({}) from map is not found in "
                "character_classes_dict dictionary\n".format(
                    fn, line_numb(), self.name, self.name))
            print(
                "Check the spelling of the item_name property on Tiled map object compared to the character classes "
                "array\n")
            pygame.quit()
            sys.exit()

        # if images for this character are not already loaded, load them
        if self.name in mob_dict:
            pass
        else:
            load_character_images(self.name, mob_dict, character_classes_dict)

        if constants.DEBUG_LEVEL:
            print(" CHAR.PY, F:{}, LN:{}".format(fn, line_numb()), end="")
            print(" self.name={}\nmob_dict[self.name]={}".format(self.name, mob_dict[self.name]))

        self.animation_list = mob_dict[self.name]['images']

        self.frame_index = random.randrange(0,
                                            len(self.animation_list[0]) - 1)  # randomly choose a frame from idle list
        # self.frame_index = random.randrange(0, len(self.animation_list) - 1)  # randomly choose a frame from idle list
        self.action = 0  # 0:idle, 1:run, 2:attack, 3:die
        self.update_time = pygame.time.get_ticks()
        self.running = False
        if constants.DEBUG_ENEMY_HEALTH_DRAIN:
            self.health = 10
        else:
            self.health = character_classes_dict[self.name]['hp']
        if "max_health" in character_classes_dict[self.name]:
            self.max_health = character_classes_dict[self.name]['max_health']
        else:
            self.max_health = self.health
        self.alive = True
        self.dying = False
        self.death_cooldown = 0
        self.animation_cooldown = character_classes_dict[self.name]['animation_cooldown']
        self.hit = False
        self.attacking = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False
        self.size = 1
        self.exp = 0  # experience points

        if self.name == "Exit Portal" and self.action == 0:
            self.image = self.animation_list[self.frame_index]
        else:
            self.image = self.animation_list[self.action][self.frame_index]

        image_width = self.image.get_width()
        image_height = self.image.get_height()

        self.rect = pygame.Rect(0, 0, image_width, image_height)
        self.rect.center = (x, y)

        if constants.DEBUG_LEVEL > 1:
            print("CHAR.PY, F:{}, L:{}, name={}".format(fn, line_numb(), self.name))
            print("  rect={}".format(self.rect))

        if constants.DEBUG_LEVEL > 1:
            print(" F: {}, line:{}\n  rect: {}\n  self.name={}".
                  format(fn, line_numb(), self.rect, self.name))
            print("   self.image={}".format(self.image))
            print("   self.rect={}".format(self.rect))
            print("")

    def draw_health(self, surf):
        health_rect = pygame.Rect(0, 0, self.image.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.top

        health_percentage = self.health / self.max_health
        if not self.fading_counter:
            if health_percentage <= 0:
                self.fading_counter = 1
        else:
            self.fading_counter += 1

        if self.health:
            draw_health_bar(surf, health_rect,
                            (0, 0, 0, 127), (255, 0, 0, 127), (0, 255, 0, 127), self.health / self.max_health)

    def move(self, dx, dy, obstacle_tiles, time_delta, exit_tile=None):
        fn = ""
        if constants.DEBUG_LEVEL:
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            ln = inspect.getframeinfo(inspect.currentframe())[1]
            if constants.DEBUG_LEVEL > 1 and (dx != 0 or dy != 0):
                print(" CHARACTER.PY, F:[{}], ticks={}, line={}, self.name={}, dx={}, dy={}".
                      format(fn, pygame.time.get_ticks(), ln, self.name, dx, dy))
                print("  self.rect={}".format(self.rect))

        screen_scroll = [0, 0]
        level_complete = False
        self.running = False

        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # control diagonal speed
        diagonal_speed_multiplier = math.sqrt(2) / 2
        if dx != 0 and dy != 0:
            dx *= diagonal_speed_multiplier
            dy *= diagonal_speed_multiplier

        # check for collision with map in x direction
        self.rect.x += dx

        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right

        self.rect.y += dy

        # check for collision with map in y direction
        for obstacle in obstacle_tiles:
            # check for collision
            if obstacle[1].colliderect(self.rect):
                # check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        if constants.DEBUG_LEVEL > 1:
            print(" CHAR.PY, F: {}, line:{}\n  rect: {}\n  self.name={}".
                  format(fn, line_numb(), self.rect, self.name))
            print("   self.image={}".format(self.image))
            print("   self.rect={}".format(self.rect))
            print("")

        # EXIT LADDER logic only applicable to player, NOT enemies
        if self.name == "player":
            # check collision with exit ladder
            if exit_tile[1].colliderect(self.rect):
                # ensure player is close to the center of the exit ladder
                exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) +
                                      ((self.rect.centery - exit_tile[1].centery) ** 2))
                self.level_complete = level_complete = True
                # exit_dist = self.rect.centerx - exit_tile[1].centerx
                # exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) +
                # (self.rect.centery - exit_tile[1].centery) **2)

                # player attack options are triggered here
                # player attack options are triggered here

                # player attack options are triggered here
                # player attack options are triggered here

                if constants.DEBUG_LEVEL:
                    print("   exit_dist={}".format(exit_dist))
                    print("   self.rect=         {}, self.rect.centerx={}".
                          format(self.rect, self.rect.centerx))
                    print("   exit_tile[1].rect= {}, centerx = {}, centery= {}".
                          format(exit_tile[1], exit_tile[1].centerx, exit_tile[1].centery))
                    pygame.quit()
                    sys.exit()
                if exit_dist < 20:
                    level_complete = True

            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH

            # move camera up and down
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH

            if constants.DEBUG_LEVEL > 1:
                print(" CHARACTER.PY, F: {}, line={}, self.name={}".format(fn, line_numb(), self.name))

            hitbox_percent = constants.PLAYER_HITBOX
            hby = self.rect.width * hitbox_percent
            hbx = self.rect.height * hitbox_percent
            hbw = self.rect.width * (hitbox_percent + hitbox_percent)
            hbh = self.rect.height * (hitbox_percent + hitbox_percent)

            self.hitbox = (self.rect.x + hbx, self.rect.y + hby, self.rect.width - hbw, self.rect.h - hbh)
        else:
            # reposition based on screen scroll
            if constants.DEBUG_LEVEL and screen_scroll[0] and screen_scroll[1]:
                print("CHARACTER.PY, F:{}, line:{}, self.name={}, self.alive={}, self.dying={}, screen_scroll={}".
                      format(fn, line_numb(), self.name, self.alive, self.dying, screen_scroll))
            self.rect.x += screen_scroll[0] + time_delta
            self.rect.y += screen_scroll[1] + time_delta

        return screen_scroll, level_complete

    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image, lightning_image, character_classes_dict,
           time_delta):
        fn = ""
        if constants.DEBUG_LEVEL > 0:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"

        clipped_line = ()
        stun_cooldown = 0
        ai_dx = 0
        ai_dy = 0
        fireball = None
        lightning = None

        # reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # using time_delta causes characters to move on screen when off screen :(
        # self.rect.x += screen_scroll[0] + time_delta
        # self.rect.y += screen_scroll[1] + time_delta

        character = character_classes_dict[self.name]
        if constants.ENEMY_SPEED_1:
            speed = 2
        else:
            speed = character['speed']

        if self.name == "Crab Monster" and self.action == 1:  # use the trim 320 settings
            subtract_width = character['trim_hitbox_320'][0] + character['trim_hitbox_320'][1]
            subtract_height = character['trim_hitbox_320'][2] + character['trim_hitbox_320'][3]
        else:
            subtract_width = character['trim_hitbox'][0] + character['trim_hitbox'][1]
            subtract_height = character['trim_hitbox'][2] + character['trim_hitbox'][3]

        # update hitbox with new coords

        # TODO: many characters have animations that are different sizes.  Orcs / Dragons / Golems / Zombies
        #  all have attacks that are different sized than Idle.   Need to accommodate that here

        if self.name not in character_classes_dict.keys():
            print("\nERROR: CHAR.PY: FN:{}, LN:{}, self.name={} does not exist in dict".
                  format(fn, line_numb(), self.name))
            pygame.quit()
            sys.exit()

        if self.name == "Crab Monster":
            if self.action == 1:  # attack action uses 320 pixels instead of 512 so different hitbox and rect
                trim_hitbox = character['trim_hitbox_320']
            else:
                trim_hitbox = character['trim_hitbox']

            self.hitbox = (self.rect.x + trim_hitbox[0], self.rect.y + trim_hitbox[2],
                           self.rect.width - subtract_width, self.rect.height - subtract_height)
        else:
            self.hitbox = (self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                           self.rect.width - subtract_width, self.rect.height - subtract_height)

        # create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        if constants.DEBUG_ENEMY_MOTION_OFF:
            if constants.DEBUG_LEVEL > 1:
                print(" F:{}, line: {}, self.name={}, speed={}, enemy motion is OFF"
                      .format(fn, line_numb(), self.name, speed))
            speed = 0  # stop enemies from moving towards player

        # check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        # check distance to player
        dist = math.sqrt(
            ((self.rect.centerx - player.rect.centerx) ** 2) + ((self.rect.centery - player.rect.centery) ** 2))
        if not clipped_line and dist > constants.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -speed
            if self.rect.centerx < player.rect.centerx:
                ai_dx = speed
            if self.rect.centery > player.rect.centery:
                ai_dy = -speed
            if self.rect.centery < player.rect.centery:
                ai_dy = speed

        if constants.DEBUG_LEVEL > 1 and self.dying:
            print(" CHAR.PY, F:{}, line:{}, dying={}, name={}".format(fn, line_numb(), self.dying, self.name))

        # hitbox of some characters is not symmetrical and has to be flipped when direction changes
        # make adjustments for asymmetrical hitbox
        if not character['is_Hitbox_Symmetrical']:
            match self.name:
                case "Panther" | "Meerkat" | "Crocodile Warrior" | "Insect":
                    if ai_dx < 0:
                        nhbx = self.rect.x + ((self.rect.x + self.rect.width) - (self.hitbox[0] + self.hitbox[2]))
                        self.hitbox = (nhbx, self.rect.y + character['trim_hitbox'][2],
                                       self.rect.width - subtract_width, self.rect.height - subtract_height)
                    elif ai_dx >= 0:
                        self.hitbox = (
                            self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                            self.rect.width - subtract_width, self.rect.height - subtract_height)
                    else:
                        self.hitbox = (
                            self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                            self.rect.width - subtract_width, self.rect.height - subtract_height)
                case "Crab Monster":
                    if ai_dx < 0:
                        nhbx = self.rect.x + ((self.rect.x + self.rect.width) - (self.hitbox[0] + self.hitbox[2]))
                        if self.action == 1:  # if using 320 pixel images use trim_hitbox_320
                            self.hitbox = (nhbx, self.rect.y + character['trim_hitbox_320'][2],
                                           self.rect.width - (
                                                   character['trim_hitbox_320'][0] + character['trim_hitbox_320'][1]),
                                           self.rect.height - (
                                                   character['trim_hitbox_320'][2] + character['trim_hitbox_320'][3]))
                        else:
                            self.hitbox = (nhbx, self.rect.y + character['trim_hitbox'][2],
                                           self.rect.width - subtract_width, self.rect.height - subtract_height)
                    else:  # ai_dx >= 0:
                        if self.action == 1:
                            self.hitbox = (self.rect.x + character['trim_hitbox_320'][0],
                                           self.rect.y + character['trim_hitbox_320'][2],
                                           self.rect.width - (
                                                   character['trim_hitbox_320'][0] + character['trim_hitbox_320'][1]),
                                           self.rect.height - (
                                                   character['trim_hitbox_320'][2] + character['trim_hitbox_320'][3]))
                        else:
                            self.hitbox = (
                                self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                                self.rect.width - subtract_width, self.rect.height - subtract_height)
                case _:
                    if ai_dx >= 0:
                        nhbx = self.rect.x + ((self.rect.x + self.rect.width) - (self.hitbox[0] + self.hitbox[2]))
                        self.hitbox = (nhbx, self.rect.y + character['trim_hitbox'][2],
                                       self.rect.width - subtract_width, self.rect.height - subtract_height)
                    else:  # ai_dx < 0:
                        self.hitbox = (
                            self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                            self.rect.width - subtract_width, self.rect.height - subtract_height)

        # if alive, move towards player, if player is ghost, skip so enemies don't see or move
        if self.alive and not self.dying and not player.ghost:
            if not self.stunned:
                # move towards player
                if ai_dx != 0 or ai_dy != 0:
                    self.move(ai_dx, ai_dy, obstacle_tiles, time_delta)

                hitbox = Rect(self.hitbox)

                # check for collision between hitboxes of player and this enemy
                if hitbox.colliderect(player.hitbox) and not player.hit:
                    if constants.DEBUG_LEVEL > 1:
                        print("  F: {}, line: {}, player.rect={}, self.rect={}".format(fn, line_numb(), player.rect,
                                                                                       self.rect))
                    new_damage = random.randrange(5, 15)  # random hit of between 5 and 15 damage.
                    player.health -= new_damage
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                    if constants.DEBUG_SHOW_HIT_DAMAGE:
                        print("  {} inflicts {} damage to you.  Health reduced to {}".format(self.name, new_damage,
                                                                                             player.health))
                    self.attacking = True
                    self.running = False
                else:
                    if not player.hit:
                        self.attacking = False

                # boss enemies shoot fireballs and Lightning. delay recharge between shots
                fireball_cooldown = constants.FIREBALL_RECHARGE
                lightning_cooldown = constants.LIGHTNING_RECHARGE

                if self.special_attack != "None":
                    if dist < constants.BOSS_VIEW_DISTANCE:  # range the boss can see the player
                        match self.special_attack:
                            case "Fireball":
                                if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                                    # fireballs shoot closer, lightning farther
                                    fireball = weapon.Fireball(fireball_image, self.rect.centerx, self.rect.centery,
                                                               player.rect.centerx, player.rect.centery, self, ai_dx,
                                                               ai_dy)
                                    self.last_attack = pygame.time.get_ticks()
                            case "Lightning":
                                if pygame.time.get_ticks() - self.last_attack >= lightning_cooldown:
                                    # fireballs shoot closer, lightning farther
                                    lightning = weapon.Lightning(lightning_image, self.rect.centerx, self.rect.centery,
                                                                 player.rect.centerx, player.rect.centery, self, ai_dx,
                                                                 ai_dy)
                                    self.last_attack = pygame.time.get_ticks()
                            case _:
                                if constants.DEBUG_LEVEL:
                                    print(
                                        "CHAR.PY, F:{}, line:{}\n ERROR: special attack not found for self.name={}".format(
                                            fn, line_numb(), self.name))
                                pygame.quit()
                                sys.exit()

        # check if hit
        if self.hit and not self.dying:
            self.hit = False
            self.last_hit = pygame.time.get_ticks()
            self.stunned = True
            self.running = False

            if not self.attacking:  # 0:idle, 1:run, 2:attack, 3:die
                if self.dying:
                    self.update_action(3)  # dying
                else:
                    self.update_action(0)  # idle
            else:
                self.update_action(2)  # attack

        if constants.DEBUG_LEVEL > 1 and self.dying:
            print(
                "CHARACTER>PY, F:{}, line:{}, self.name={}, self.alive={}, self.dying={}, self.health={}, "
                "frame_index={}".
                format(fn, line_numb(), self.name, self.alive, self.dying, self.health, self.frame_index))

        if pygame.time.get_ticks() - self.last_hit > stun_cooldown:
            self.stunned = False

        return fireball, lightning

    def update(self, player):
        fn = ""
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = inspect.getframeinfo(inspect.currentframe())[2]
            if constants.DEBUG_LEVEL > 1:
                print("[{},ln={}]: self.name={}, self.image={}".
                      format(fn, line_numb(), self.name, self.image))

        # check if character has died
        if self.health <= 0:
            self.health = 0
            if self.alive:
                if not self.dying:
                    # add enemy's exp to player
                    player.exp += self.character_classes_dict[self.name]['exp']
                    if player.exp >= 1000:
                        rank = player.exp // 1000
                        player.rank = rank
                self.dying = True
                self.running = False

            if constants.DEBUG_LEVEL > 1:
                print("CHARACTER.PY, F:[{}], line:{}, name={}".format(fn, line_numb(), self.name))

        # timer to reset character taking a hit
        hit_cooldown = constants.PLAYER_HIT_COOLDOWN
        if self.name == "player":
            if self.hit and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False

        # animation_cooldown = 150
        animation_cooldown = self.animation_cooldown

        # check what action the character is performing
        # default to idle
        if not self.running and not self.dying and not self.attacking:
            self.update_action(0)  # 0:idle
        if self.attacking:
            self.running = False
            self.update_action(2)  # attack action
        if self.running:
            self.update_action(1)  # 1:run
        #            animation_cooldown = 75
        if self.dying:
            self.attacking = False
            self.running = False
            self.update_action(3)  # death action

        # update image
        if constants.DEBUG_LEVEL > 1:
            print("  CHAR.PY, F: {}, line:{}, self.name={}".format(fn, line_numb(), self.name))

        match self.name:
            case "exit portal":  # exit
                self.image = self.animation_list[self.frame_index]
            case _:  # default
                self.image = self.animation_list[self.action][self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # if constants.DEBUG_LEVEL:
        #     l = len(self.animation_list[self.action])

        # check if the animation has finished
        if self.name == "exit portal":
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        elif self.frame_index >= len(self.animation_list[self.action]):
            if self.dying:
                self.alive = False
            if self.attacking:
                self.frame_index = 0
            else:
                self.frame_index = 0
                if self.dying:
                    self.alive = False

        if constants.DEBUG_LEVEL:  # just for debugging, doing a no-opt to allow a breakpoint before function returns
            self.frame_index = self.frame_index

    def update_action(self, new_action):
        if constants.DEBUG_LEVEL > 1:  # get the function name for debugging
            fn = inspect.getframeinfo(inspect.currentframe())[2]
            print("[{},line={}]: self.name={}, self.image={}".format(fn, line_numb(), self.name, self.image))

        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if constants.DEBUG_LEVEL > 1:  # get the function name for debugging
            fn = inspect.getframeinfo(inspect.currentframe())[2]
            print("CHAR.PY, [{},line={}]: self.name={}, self.image={}".format(fn, line_numb(), self.name, self.image))

        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
        if constants.DEBUG_SPRITE_RECT_ON:
            pygame.draw.rect(surface, constants.GREEN, self.rect, 1)
            # draw enemy hitbox rect
            pygame.draw.rect(surface, constants.RED, self.hitbox, 2)
