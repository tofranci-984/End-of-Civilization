
import pygame
import math
import random
import constants
import inspect

def line_numb():
    ''' Returns the current line number in our program
    '''
    return inspect.currentframe().f_back.f_lineno


class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        shot_cooldown = constants.ARROW_COOLDOWN
        arrow = None

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)  # -ve because pygame y coordinates increase down the screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired == False and (
                pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        # reset mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, (
        (self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))



class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(
            self.angle)) * constants.ARROW_SPEED)  # -ve because pygame y coordiate increases down the screen

    def update(self, screen_scroll, obstacle_tiles, enemy_list):
        # fn = ""
        # if constants.DEBUG_LEVEL:
        #     fn = "["+inspect.getframeinfo(inspect.currentframe())[2]+"]"
        #     ln = inspect.getframeinfo(inspect.currentframe())[1]
        #     if constants.DEBUG_LEVEL>1 and (dx != 0 or dy != 0):
        #         print(" MAIN.PY, F:[{}], line={}, self.name={}, dx={}, dy={}".
        #               format(fn, pygame.time.get_ticks(), ln, self.char_index, self.name, dx, dy))
        #         print("  self.rect={}".format(self.rect))

        # reset variables
        damage = 0
        damage_pos = None

        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check for collision between arrow and tile walls
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                self.kill()

        # check if arrow has gone off-screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        # check collision between arrow and enemies HITBOX
        for enemy in enemy_list:
            if self.rect.colliderect(enemy.hitbox) and enemy.alive and not enemy.dying:
                damage = random.randrange(constants.ARROW_MIN_DAMAGE, constants.ARROW_MAX_DAMAGE )
                damage_pos = enemy.rect
                enemy.health -= damage
                damage = str(damage) + " : " + str(enemy.health)
                enemy.hit = True
                self.kill()
                break

        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, (
        (self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))



class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y, boss, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        match boss.name:
            case "TheOldKing":
                if dx <= 0:
                    self.rect.center = (x - 160, y - 10)
                if dx > 0:
                    self.rect.center = (x + 160, y - 10)
            case _:
                self.rect.center = (x, y)

        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(
            self.angle)) * constants.FIREBALL_SPEED)  # -ve because pygame y coordiate increases down the screen

    def update(self, screen_scroll, player):
        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check if fireball has gone off-screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        # check collision between self and player
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= random.randrange(constants.FIREBALL_MIN_DAMAGE, constants.FIREBALL_MAX_DAMAGE)
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, (
            (self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))

class Lightning(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y, boss, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        x_dist = target_x - x
        y_dist = -(target_y - y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle + 115)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        match boss.name:
            case "TheOldKing":
                if dx <= 0:
                    self.rect.center = (x - 160, y - 10)
                if dx > 0:
                    self.rect.center = (x + 160, y - 10)
            case _:
                self.rect.center = (x, y)

        # calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(math.radians(self.angle)) * constants.LIGHTNING_SPEED
        self.dy = -(math.sin(math.radians(
            self.angle)) * constants.LIGHTNING_SPEED)  # -ve because pygame y coordiate increases down the screen

    def update(self, screen_scroll, player):
        # reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy

        # check if fireball has gone off-screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()

        # check collision between self and player
        if player.rect.colliderect(self.rect) and player.hit == False:
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            player.health -= random.randrange(constants.LIGHTNING_MIN_DAMAGE, constants.LIGHTNING_MAX_DAMAGE)
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, (
            (self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))
