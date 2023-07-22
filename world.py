# import pytmx
# from pytmx.util_pygame import load_pygame
import inspect
# from pathlib import Path
import sys

import pygame

import constants
from character import Character
from items import Item


def line_numb():
    """Returns the current line number in our program"""
    return inspect.currentframe().f_back.f_lineno


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class World():
    def __init__(self, character_classes_dict):
        fn = ""
        if constants.DEBUG_LEVEL > 0:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            if constants.DEBUG_LEVEL > 1:
                print("WORLD.PY, F:{}, line: {}, creating WORLD".format(fn, line_numb()))

        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player = None
        self.character_list = []
        self.character_classes_dict = character_classes_dict
        self.player_count = 0
        self.map_level = 1

    def process_data(self, tmx_data, item_images, mob_dict, sprite_group):
        fn = ""
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"

        # self.level_length = tmx_data.width * tmx_data.height

        # process enemies and objects (ground is after)
        if constants.DEBUG_LEVEL:
            print(" WORLD.PY, F:{}, LN:{}\nPROCESSING {} objects (including enemies)".
                  format(fn, line_numb(), len(tmx_data.objects_by_id)))

        for i, obj in enumerate(tmx_data.objects):
            pos = obj.x, obj.y
            image_x = int(obj.x)
            image_y = int(obj.y)

            if constants.DEBUG_LEVEL> 1:
                print("WORLD.PY, F:{}, LN:{}".format(fn, line_numb()))
                print("\nPROCESSING {}, i={}".format(obj.properties['item_name'], i))

            # tile_data = []
            if obj.image:
                image = obj.image
                image_rect = image.get_rect()
                image_rect.center = (image_x, image_y)

                tile_data = [image, image_rect, image_x, image_y]
            else:  # object has no image
                print("\n\nERROR **\n\nWORLD.PY, F:{}, LN:{}. object_index= {}. Object ID{}, image {}"
                      .format(fn, line_numb(), i, obj.id, obj.image))
                pygame.quit()
                sys.exit()

            item_name_to_index = {
                "gold1": 10, "gold2": 11, "gold3": 12, "gold4": 13, "gold5": 14, "gold6": 15,
                "gold7": 16, "gold8": 17, "gold9": 18, "gold10": 19, "gold11": 20, "gold12": 21
            }
            match obj.properties['item_name']:
                case "player":
                    self.player_count += 1
                    player = Character(image_x, image_y, mob_dict,
                                       obj.properties['item_name'], self.character_classes_dict)
                    self.player = player
                case "gold":
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(coin)
                case "red potion":
                    potion = Item(image_x, image_y, 1, [item_images[1]])
                    self.item_list.append(potion)
                case "blue potion":
                    potion = Item(image_x, image_y, 2, [item_images[2]])
                    self.item_list.append(potion)
                case "green potion":
                    potion = Item(image_x, image_y, 3, [item_images[3]])
                    self.item_list.append(potion)
                case item_name if item_name in item_name_to_index:
                    coin = Item(image_x, image_y, item_name_to_index[item_name], item_images[5])
                    self.item_list.append(coin)
                case "exit portal":
                    portal = Item(image_x, image_y, 100, [item_images[4]])
                    self.item_list.append(portal)
                    self.exit_tile = tile_data
                case _:
                    if constants.DEBUG_LEVEL:
                        print(f"  WORLD.PY, F:{fn}, ln:{line_numb()}, name={obj.properties['item_name']}")
                    if not obj.properties['item_name']:
                        print(f"  *ERROR*: self.name undefined.  Check that  item_names are defined in TSX files")
                        pygame.quit()
                        sys.exit()
                    enemy = Character(image_x, image_y, mob_dict, obj.properties['item_name'],
                                      self.character_classes_dict)
                    self.character_list.append(enemy)

        # process ground tiles
        if constants.DEBUG_LEVEL:
            print(" WORLD.PY, F:{}, LN:{}\n\nPROCESSING GROUND TILES".format(fn, line_numb()))

        unknown_tiles = []
        wall_count = open_count = green_count = secret_count = floor_count = 0
        count = 0
        for layer in tmx_data.visible_layers:
            if constants.DEBUG_LEVEL > 1:
                print(" WORLD.PY, F: {}, LN: {}, Layer Name: [{}], count= {}".format(fn, line_numb(), layer.name, count))

            if not hasattr(layer, 'data'):  # only tile layers have data, not object layers
                if constants.DEBUG_LEVEL:
                    print("  line:{}, Layer [{}] has no Data attribute. Skipping".format(line_numb(), layer.name))
                continue
            else:
                if constants.DEBUG_LEVEL:
                    print(" Processing layer: {}".format(layer.name))

            for x, y, surf in layer.tiles():
                if constants.DEBUG_LEVEL > 1:
                    print("  line:{}, x ={}, y ={}".format(line_numb(), x, y))

                count += 1
                image = tmx_data.get_tile_image(x, y, 0)
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)

                tile_type = layer.data[y][x]
                tile_prop = tmx_data.get_tile_properties(x, y, 0)
                tile_group = tile_prop['item_group']
                tile_name = tile_prop['item_name']
                tile_source = tile_prop['source']

                if not tile_group:
                    print(" WORLD.PY, F: {}, Line:{}, x= {}, y= {}, count= {}".format(fn, line_numb(), x, y, count))
                    print("   item_group missing from tile at x={}, y={}".format(x, y))
                    print("    tile_type= {}, tile_group={}, tile_name={}".format(tile_type, tile_group, tile_name))
                    print("    source= {}".format(tile_source))
                    pygame.quit()
                    sys.exit()

                tile_data = [image, image_rect, image_x, image_y]

                if constants.DEBUG_LEVEL > 1:
                    print("  WORLD.PY, F: {}, Line:{}, x= {}, y= {}, count= {}".format(fn, line_numb(), x, y, count))
                    print("   tile_type= {}, tile_group={}, tile_name={}".format(tile_type, tile_group, tile_name))
                    print("   source= {}".format(tile_source))

                match tile_group:
                    case "wall":
                        wall_count += 1
                        self.obstacle_tiles.append(tile_data)
                        self.map_tiles.append(tile_data)
                        Tile(pos=pos, surf=surf, groups=sprite_group)
                    case "floor" | "green" | "secret" | "holes":
                        if tile_group == "floor":
                            open_count += 1
                        elif tile_group == "secret":
                            secret_count += 1
                        elif tile_group == "holes":
                            floor_count += 1
                        else:  # green tiles
                            green_count += 1

                        self.map_tiles.append(tile_data)
                        Tile(pos=pos, surf=surf, groups=sprite_group)
                    case _:
                        print("   Unknown tile group={}, item_name={}".format(tile_group, tile_name))
                        unknown_tiles.append(tile_type)
                        if constants.DEBUG_LEVEL:
                            print(" WORLD.PY, F: {}, LN:{}, ** UNKNOWN TILE TYPE **, x={}, y={}, tile_type={}".
                                  format(fn, line_numb(), x, y, tile_type))

        if constants.DEBUG_LEVEL:
            print(" WORLD.PY, F:{}: LN:{}, count tiles processed={}".format(fn, line_numb(), count))
            print("   {} Wall tiles\n   {} Open\n   {} Secret\n   {} Green\n   {} Floor\n".
                  format(wall_count, open_count, secret_count, green_count, floor_count))
            if unknown_tiles:
                print(" WORLD.PY, F: {}, LN:{}, {} UNKNOWN TILES".
                      format(fn, line_numb(), len(unknown_tiles)))
                for tile in unknown_tiles:
                    print(f" {tile} ", end="")
                return 0  # failed

        return 1  # success

    def update(self, screen_scroll):
        if constants.DEBUG_LEVEL > 1:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            ln = inspect.getframeinfo(inspect.currentframe())[1]
            print(" WORLD.PY, F {}, LN:{}, self.char_type = {}".format(fn, ln, len(self.map_tiles)))

        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        if constants.DEBUG_LEVEL > 1:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            print(" WORLD.PY, F {}, LN:{}".format(fn, line_numb()))

        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
