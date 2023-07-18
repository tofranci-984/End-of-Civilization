import pygame
import constants
import inspect
import random


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin=False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type  # 0: coin, 1: health potion, 2 blue potion, 10 gold piles begin
        self.animation_list = animation_list
        self.exit_portal = False
        if constants.DEBUG_LEVEL> 1:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            ln = inspect.getframeinfo(inspect.currentframe())[1]
            if constants.DEBUG_LEVEL > 0:
                print("ITEMS.PY, F:{}, line:{}, New Item Init.  item_type={}".format(fn, ln, item_type))

        self.update_time = pygame.time.get_ticks()
        match self.item_type:
            case 0:  # gold coin
                self.frame_index = random.randrange(0, len(self.animation_list))
                self.image = self.animation_list[self.frame_index]
            case 1:  # health potion
                self.frame_index = 0
                self.image = self.animation_list[self.frame_index]
            case 2 | 3:  # potions
                self.frame_index = 0
                self.image = self.animation_list
            case 100:  # exit portal
                self.frame_index = 0
                self.exit_portal = True
                self.image = self.animation_list[self.frame_index]
            case _:  # gold piles
                if item_type < 10:
                    if constants.DEBUG_LEVEL:
                        print("ITEMS.PY, F:{}\n\n ** ERROR **\n\nInvalid item_type={}".format(fn, item_type))
                        pygame.quit()
                self.frame_index = 0

                if item_type >= 10:  # gold piles
                    self.image = self.animation_list[0]
                else:
                    self.image = self.animation_list[item_type]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player, coin_fx, heal_fx, time_delta):
        fn = ""
        # level_complete = False
        if constants.DEBUG_LEVEL:  # get the function name for debugging
            fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"
            ln = inspect.getframeinfo(inspect.currentframe())[1]
            if constants.DEBUG_LEVEL > 1:
                print("ITEMS.PY, F {}, LN:{}".format(fn, ln))

        # doesn't apply to the dummy coin that is always displayed at the top of the screen
        if not self.dummy_coin:
            # reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]

# TODO: want to use time delta but it causes portal to move back on screen when offscreen
            # self.rect.x += screen_scroll[0] + time_delta
            # self.rect.y += screen_scroll[1] + time_delta

        # check to see if item has been collected by the player
        if self.rect.colliderect(player.rect):
            # coin collected

            match self.item_type:
                case 0:  # coin
                    player.score += 1
                    coin_fx.play()
                case 1:  # red potion / health
                    player.health += 10
                    heal_fx.play()
                case 2:  # blue potion for spell(s)
                    player.health += 10
                    heal_fx.play()
                case 3:  # green potion / future ...
                    player.health += 10
                    heal_fx.play()
                case 100:  # exit portal
                    pass
                    player.level_complete = True
                case _:  # gold pile
                    if constants.DEBUG_LEVEL:
                        print("ITEMS.PY f:{}, line:{}, item_type={}".format(fn, ln, self.item_type))
                    player.score += random.randrange(2, 20)
                    coin_fx.play()

            # TODO add some exit level sound here

            if constants.DEBUG_LEVEL:
                print("ITEMS.PY, F:{}, LN:{}, item_type= {}".format(fn, ln, self.item_type))

            # kill / remove item unless it is the exit portal
            if self.item_type != 100:
                self.kill()

        # handle animation
        animation_cooldown = 150
        # update image
        if self.item_type != 100 and self.item_type >= 10:  # gold piles are images not animations
            self.image = self.animation_list[self.item_type - 10]
        elif self.item_type in [2, 3]:  # potions
            self.image = self.animation_list
        else:  #
            self.image = self.animation_list[self.frame_index]

        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.item_type not in [2, 3]:
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
