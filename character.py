import random
import sys

import pygame
import math
import weapon
import constants
import inspect
from pygame.locals import *
import pygame_gui
from pygame_gui.core import ObjectID



def line_numb():
    '''Returns the current line number in our program'''
    return inspect.currentframe().f_back.f_lineno


def search_character_classes(name, character_classes):
    for i, char in enumerate(character_classes):
        if char["name"] == name:
            return i
    return -1  # Return -1 if character not found


class Character():
    def __init__(self, x, y, mob_animations, char_name, character_classes, manager):
        fn = ""
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"

        if constants.DEBUG_LEVEL:
            print(" CHARACTER.PY, F:{}, line:{}, Creating new Character: {}".format(fn, line_numb(), char_name))

# TODO: Need to on using centerx, centery to place objects NOT x,y due to stutter when switching from idle to attack.
        self.x = x
        self.y = y
        self.name = char_name

        # set the special attack if avail, else None
        # TODO: why is a misssing attribute causing a crash?  Troll2 doesn't have the special attack, troll1 does
        self.special_attack = character_classes[search_character_classes(self.name, character_classes)][
            'Special_Attack']
        self.score = 0
        self.flip = False
        self.level_complete = False
        self.ghost = False

        # assign initial hitbox info
        self.hitbox = (0, 0, 0, 0)
        self.character_classes = character_classes

        if self.name == "player":
            self.char_index = 0  # player uses "Warrior" so need to manually set index to 0 (Warrior)
            if constants.DEBUG_GHOST_MODE_ON:
                self.ghost = True
        else:
            self.char_index = search_character_classes(self.name, character_classes)

        if self.char_index == -1:
            print(
                "CHAR.PY, F:{}, line:{}, self.name={}\n\n  ERROR: object ({}) from map is not found in "
                "character_classes array\n".format(
                    fn, line_numb(), self.name, self.name))
            print(
                "Check the spelling of the item_name property on Tiled map object compared to the character classes "
                "array\n")
            pygame.quit()
            sys.exit()

        self.animation_list = mob_animations[self.char_index]

        self.frame_index = random.randrange(0, len(self.animation_list) - 1)  # randomly choose a frame from idle list
        self.action = 0  # 0:idle, 1:run, 2:attack, 3:die
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = character_classes[self.char_index]['hp']
        self.alive = True
        self.dying = False
        self.death_cooldown = 0
        self.animation_cooldown = character_classes[self.char_index]['animation_cooldown']
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

# TODO: getting error when healthbar is uncommented

        # self.healthbar = pygame_gui.elements.UIStatusBar(pygame.Rect((0, image_height - 10), (50, 6)), manager,
        #                                                  sprite=self.image,
        #                                                  percent_method=self.get_health_percentage,
        #                                                  object_id=ObjectID('#health_bar', '@player_status_bars'))

        if constants.DEBUG_LEVEL > 0:
            print(" F: {}, line:{}\n  rect: {}\n  char_index= {}\n  self.name={}".
                  format(fn, line_numb(), self.rect, self.char_index, self.name))
            print("   self.image={}".format(self.image))
            print("")

    def get_health_percentage(self) -> float:
        return self.health / constants.PLAYER_START_HEALTH

    def get_mana_percentage(self) -> float:
        return self.current_mana / self.max_mana

    def move(self, dx, dy, obstacle_tiles, time_delta, exit_tile=None):
        fn = ""
        if constants.DEBUG_LEVEL:
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            ln = inspect.getframeinfo(inspect.currentframe())[1]
            if constants.DEBUG_LEVEL > 1 and (dx != 0 or dy != 0):
                print(" CHARACTER.PY, F:[{}], ticks={}, line={}, self.name={}, dx={}, dy={}".
                      format(fn, pygame.time.get_ticks(), ln, self.char_index, self.name, dx, dy))
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
            # self.rect.x += screen_scroll[0]
            # self.rect.y += screen_scroll[1]

        return screen_scroll, level_complete

    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image, lightning_image, character_classes, time_delta):
        fn = ""
        if (constants.DEBUG_LEVEL > 0):  # get the function name for debugging
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
        # self.rect.x += screen_scroll[0] + time_delta
        # self.rect.y += screen_scroll[1] + time_delta
        hbx = hby = hbw = hbh = -1
        index = search_character_classes(self.name, character_classes)
        character = character_classes[index]
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

        if self.name == "Crab Monster":
            if self.action == 1:  # attack action uses 320 pixels instead of 512 so different hitbox and rect
                trim_hitbox = character['trim_hitbox_320']
            else:
                trim_hitbox = character['trim_hitbox']

            self.hitbox = (self.rect.x + trim_hitbox[0], self.rect.y + trim_hitbox[2],
                           self.rect.width - subtract_width, self.rect.height - subtract_height)

        elif search_character_classes(self.name, self.character_classes):
            self.hitbox = (self.rect.x + character['trim_hitbox'][0], self.rect.y + character['trim_hitbox'][2],
                           self.rect.width - subtract_width, self.rect.height - subtract_height)
        else:
            if constants.DEBUG_LEVEL:
                print(" CHARACTER.PY, F:{}, line={}, self.name={}\n\n WARNING: Character unknown".
                      format(fn, line_numb(), self.name))
                pygame.quit()
                sys.exit()

        # create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        if constants.DEBUG_ENEMY_MOTION_OFF:
            if constants.DEBUG_LEVEL > 1:
                print(" F:{}, line: {}, char_type={}, speed={}, enemy motion is OFF"
                      .format(fn, line_numb(), self.char_index, speed))
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
                    player.health -= random.randrange(5, 15)  # random hit of between 5 and 15 damage.
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                    self.attacking = True
                    self.running = False
                else:
                    if not player.hit:
                        self.attacking = False

                # boss enemies shoot fireballs and Lightning. delay recharge between shots
                fireball_cooldown = constants.FIREBALL_RECHARGE
                lightning_cooldown = constants.LIGHTNING_RECHARGE

                if self.special_attack != "None":
                    if dist < (constants.BOSS_VIEW_DISTANCE):  # range the boss can see the player
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
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = inspect.getframeinfo(inspect.currentframe())[2]
            if constants.DEBUG_LEVEL > 1:
                print("[{},ln={}]: self.name={}, self.char_type= {},  self.image={}".
                      format(fn, line_numb(), self.name, self.char_index, self.image))

        # check if character has died
        if self.health <= 0:
            self.health = 0
            if self.alive:
                if not self.dying:
                    player.exp += self.character_classes[self.char_index]['exp']
                self.dying = True
                self.running = False
                # add enemy's exp to player

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
            print("[{},line={}]: self.name={}, self.char_imdex={}, self.image={}".format(fn, line_numb(), self.name,
                                                                                         self.char_index, self.image))

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
