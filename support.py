import json
import pygame
import constants
import os
from tilesheet import Tilesheet


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def write_code_to_json1(code, filename):
    with open(filename, 'w') as file:
        json.dump(code, file, indent=2, sort_keys=True)


def read_code_from_json(filename):
    with open(filename, 'r') as file:
        code = json.load(file)
        return code


# helper function to scale image
def scale_img(image, scale, smooth=False, use_global_scale=True):
    w = image.get_width()
    h = image.get_height()
    if use_global_scale:
        global_scale = constants.GLOBAL_SCALE * scale
    else:
        global_scale = scale
    if smooth and scale == 2:
        return pygame.transform.scale2x(image)
    else:
        return pygame.transform.scale(image, (w * global_scale, h * global_scale))


def load_gold_images(coin_images, gold_images):
    # Load gold COIN images
    # (filename, width, height, rows, cols, start_row_index= 0)  3270 / 496    15x 2
    tiles = Tilesheet("assets/images/items/GoldCoin_v1.1/64/spritesheet/GoldCoin.png", 64, 64, 1, 30,
                      0)  # 3 images, row 1
    for x in range(0, tiles.cols, 2):  # skip
        img = tiles.get_tile(x, 0)
        img = scale_img(img, constants.GOLD_COIN_SCALE, use_global_scale=False)
        coin_images.append(img)

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
        img = scale_img(img, constants.GOLD_PILE_SCALE, use_global_scale=False)
        gold_images.append(img)


def load_explosions(explosions):
    # Load explosion images

    path = "assets/images/explosions"
    explosion_data = {}
    explosion_files = []
    explosion_data = {
        'Explosion_1': [],
        "Explosion_9": []
    }

    for item in ["Explosion_9", "Explosion_1"]:

        count = load_files(f"{path}/{item}", "Explosion_", explosion_files)
        if constants.DEBUG_LEVEL:
            print(f"path={path!r}, explosion={item!r}, file_count={count}")

        explosion_files.sort()

        explosion = {}
        for i, image_path in enumerate(explosion_files):
            img = pygame.image.load(image_path).convert_alpha()
            img = scale_img(img, 1, use_global_scale=False)
            tmp_explosion = [image_path, img]
            explosion[i] = tmp_explosion

        explosions.append(explosion)


def load_potions():
    # load potion images
    red_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-red-new.png").convert_alpha(),
                           constants.POTION_SCALE, use_global_scale=False)
    blue_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-blue-new.png").convert_alpha(),
                            constants.POTION_SCALE, use_global_scale=False)
    green_potion = scale_img(pygame.image.load(
        "assets/images/environment/Sprites/PNG/Additional Sprites/bottle-green-new.png").convert_alpha(),
                             constants.POTION_SCALE, use_global_scale=False)

    return red_potion, blue_potion, green_potion


def load_files(directory, prefix, file_array):
    count = 0
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith(".png"):
            try:
                # number = int(filename[4:8])
                file_path = os.path.join(directory, filename)
                file_array.append(file_path)
                count += 1
            except ValueError:
                if constants.DEBUG_LEVEL:
                    print(" MAIN.PY, F:load_files, line:{} Skipping {}".format(line_numb(), filename))
                pass  # ignore files with invalid number format
    return count

# # importing the module
# import tracemalloc
#
# # code or function for which memory
# # has to be monitored
# def app():
# 	lt = []
# 	for i in range(0, 100000):
# 		lt.append(i)
#
# # starting the monitoring
# tracemalloc.start()
#
# # function call
# app()
#
# # displaying the memory
# print(tracemalloc.get_traced_memory())
#
# # stopping the library
# tracemalloc.stop()


