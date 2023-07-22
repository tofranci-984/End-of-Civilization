import inspect
import random
import sys
from pathlib import Path
from button import Button
from colordict import *
from items import Item
from pytmx.util_pygame import *
from pygame import mixer
from support import *
from weapon import Weapon
from world import World


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.text = "0"

    def render(self, level: str):
        self.text = f"level: {level} - FPS:{self.clock.get_fps():.0f} W:{constants.SCREEN_WIDTH!r} H:{constants.SCREEN_HEIGHT!r}"
        # self.text = f"level: {level} - FPS:{self.clock.get_fps():.0f}"

        pygame.display.set_caption(self.text)
        # display.blit(self.font.render(self.text, True, green), ((constants.SCREEN_WIDTH / 2) - 250, 12))


def line_numb():
    """ Returns the current line number in our program
    """
    return inspect.currentframe().f_back.f_lineno


def get_loot(player, enemy, x, y):
    if constants.DEBUG_LEVEL:  # get the function name for debugging
        fn = "[" + inspect.getframeinfo(inspect.currentframe())[2] + "]"

    loot_output = f" *{enemy.name} looted*, found "

    for i in range(random.randint(1, constants.LOOT_MAXIMUM)):
        random_loot = random.randint(1, 15)

        if constants.DEBUG_LEVEL > 1:
            print(f"x={x}, y={y}, count={i}, random_loot={random_loot}")
        ox = x + random.randint(-15, 15)
        oy = y + random.randint(-15, 15)
        if random_loot == 1:
            loot_name = "Red Healing Potion"
            loot_images = item_images[1]
            item_type = 1
            loot = Item(ox, oy, item_type, [item_images[1]])

        elif random_loot == 2:
            loot_name = "Blue Healing Potion"
            loot_images = item_images[2]
            item_type = 2
            loot = Item(ox, oy, item_type, item_images[2])
        elif random_loot == 3:
            loot_name = "Green Healing Potion"
            loot_images = item_images[3]
            item_type = 3
            loot = Item(ox, oy, item_type, item_images[3])
        elif random_loot == 4:
            loot_name = "Gold Pile"
            item_type = random.randint(10, 21)
            loot_images = item_images[5]
            loot = Item(ox, oy, item_type, loot_images)
        else:
            loot_name = "Coin"
            loot_images = item_images[0]
            item_type = 0
            loot = Item(ox, oy, item_type, loot_images)

        if constants.DEBUG_LEVEL > 1:
            print(f"F:{fn}, L:{line_numb()}, item_type={item_type}, loot_images={loot_images}")

        loot_output += loot_name + ", "
        item_group.add(loot)
    print(loot_output)


# function for outputting text onto the screen
def draw_statusbar_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for displaying game info
def draw_statusbar_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))

    text_pos_percentage = {"hp": 1, "mana": 19, "map": 33, "exp": 45, "health_potion": 67, "poison_potion": 74,
                           "mana_potion": 81, "score": 92}
    statbar_pos_offset = {}

    for item in text_pos_percentage:
        statbar_pos_offset[item] = int(constants.SCREEN_WIDTH * text_pos_percentage[item] / 100)

    # HP
    draw_statusbar_text("HP: " + str(player.health) + "/" + str(character_classes_dict['player']['max_health']),
                        font, constants.WHITE, statbar_pos_offset['hp'], 15)
    # MANA
    draw_statusbar_text("MANA: " + str(player.mana), font, constants.WHITE, statbar_pos_offset['mana'], 15)

    # level
    draw_statusbar_text("MAP: " + str(level), font, constants.WHITE, statbar_pos_offset['map'], 15)
    # exp
    draw_statusbar_text("EXP: " + str(player.exp) + "/" + str(player.rank), font, constants.WHITE,
                        statbar_pos_offset['exp'], 15)
    # show score
    draw_statusbar_text(f"X{player.score}", font, constants.WHITE, statbar_pos_offset['score'], 15)

    # show mana potions
    draw_statusbar_text(f"X{player.mana_potions}", font, constants.WHITE, statbar_pos_offset['mana_potion'], 15)
    # show health potions
    draw_statusbar_text(f"X{player.health_potions}", font, constants.WHITE, statbar_pos_offset['health_potion'], 15)
    # show poison potions
    draw_statusbar_text(f"X{player.poison_potions}", font, constants.WHITE, statbar_pos_offset['poison_potion'], 15)


# function to reset level
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()
    lightning_group.empty()
    enemy_stats_sprite_group.empty()

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

    def update(self, time_delta):
        # reposition based on screen scroll
        self.rect.x += screen_scroll[0] + time_delta
        self.rect.y += screen_scroll[1] + time_delta

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


# Begin Game code
# Begin Game code
# Begin Game code

game_title = "The End of Civilization"

if constants.DEBUG_LEVEL:
    print(f"\n\n{game_title} starting\nPath {Path(__file__)}\n")

# load music (has to be done before pygame.init for perf reasons)
mixer.init()
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.2)

# play background music only if SOUND_FX True
if constants.MUSIC:
    pygame.mixer.music.play(-1, 0.0, 5000)

if not constants.SOUND_FX:
    volume = 0.0
else:
    volume = .5

pygame.init()

if constants.DEBUG_LEVEL:
    print("[pygame.mixer] init")
    print(f"[pygame.mixer.music] loaded, volume is {volume}")

# minimum game screen width / height
if constants.SCREEN_WIDTH <= 1200:
    constants.SCREEN_WIDTH = 1200
if constants.SCREEN_HEIGHT <= 480:
    constants.SCREEN_HEIGHT = 480

# vsync setting removes tearing issue when running
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
                                 pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 1
# god_mode = constants.GOD_MODE
start_game = False
pause_game = False
start_intro = False
screen_scroll = [0, 0]

# define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False
use_health_potion = False
use_poison_potion = False
use_mana_potion = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)
colors = ColorDict()
black = colors['black']
white = colors['white']
green = colors['green']
indigo = colors['indigo']
cyan = colors['cyan']

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
                      constants.BUTTON_SCALE, use_global_scale=False)
exit_img = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE,
                     use_global_scale=False)
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(),
                        constants.BUTTON_SCALE, use_global_scale=False)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(),
                       constants.BUTTON_SCALE, use_global_scale=False)

# load heart images
# heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),
#                         constants.HEALTHBAR_SCALE,
#                         use_global_scale=False)
# heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),
#                        constants.HEALTHBAR_SCALE,
#                        use_global_scale=False)
# heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),
#                        constants.HEALTHBAR_SCALE,
#                        use_global_scale=False)
#
# load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow-new.png").convert_alpha(), constants.WEAPON_SCALE,
                      use_global_scale=False)
sword_image = scale_img(pygame.image.load("assets/images/weapons/sword.png").convert_alpha(), constants.WEAPON_SCALE,
                        use_global_scale=False)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE,
                        use_global_scale=False)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),
                           constants.FIREBALL_SCALE, use_global_scale=False)
lightning_image = scale_img(pygame.image.load("assets/images/weapons/red-lightning.png").convert_alpha(),
                            constants.LIGHTNING_SCALE, use_global_scale=False)

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
    print(f" line: {line_numb()}. weapon images loaded")

# dictionary for character images
mob_dict = dict()

animation_types = ["idle", "run", "attack", "death"]
animation_list = []

animation = ""

# read in character / enemy info from JSON file
character_classes_dict = read_code_from_json('character classes.json')

# load in the level data
path = "assets/testing.tmx" if constants.DEBUG_LEVEL else "assets/level1.tmx"

if constants.DEBUG_LEVEL:
    print(f"MAIN.PY, line:{line_numb()}, Loading TMX_MAP file: {path}")

# tmx file should be at root of images directory.  Otherwise images path can get messed up and have to be re-located
# for each file / image in tiled maps :(
try:
    tmx_map = load_pygame(path)

except:
    print(f"MAIN.PY line:{line_numb()}\n Unable to load TMX file: {path}")
    print("-Check path\n-Make sure you can open the file in Tiled\n-Check Tiled icons / locate correct folders")
    pygame.quit()
    exit()

# start FPS monitoring
if constants.DEBUG_LEVEL:
    if constants.FPS_MONITOR:
        fps = FPS()
    print(f" MAIN.PY, line={line_numb()}\n   Creating World\n")

# Create World
world = World(character_classes_dict)

# sprite_group = pygame.sprite.Group()
enemy_stats_sprite_group = pygame.sprite.LayeredUpdates()

success = world.process_data(tmx_map, item_images, mob_dict, enemy_stats_sprite_group)
if not success:
    print(f" MAIN.PY, line:{line_numb()}, world.process_data failed")
    pygame.quit()
    sys.exit()

if constants.DEBUG_LEVEL:
    print(f" MAIN.PY, line={line_numb()}\n   World Created")

# create player
player = world.player

# create player's weapon
bow = Weapon(bow_image, arrow_image)

# extract enemies from world data
enemy_list = world.character_list

# create sprite groups
damage_text_group = pygame.sprite.LayeredUpdates()
arrow_group = pygame.sprite.LayeredUpdates()
item_group = pygame.sprite.LayeredUpdates()
fireball_group = pygame.sprite.LayeredUpdates()
lightning_group = pygame.sprite.LayeredUpdates()

# text_pos_percentage = {"hp": 1, "mana": 19, "map": 33, "exp": 45, "health_potion": 67, "poison_potion": 74,
#                        "mana_potion": 81, "score": 92}
text_pos_percentage = {"hp": 0, "level": 25, "exp": 40, "health": 65, "poison": 72, "mana": 79, "score": 90.5}
statbar_pos_offset = {}

for item in text_pos_percentage:
    statbar_pos_offset[item] = int(constants.SCREEN_WIDTH * text_pos_percentage[item] / 100)

if constants.DEBUG_LEVEL:
    # print(f"   MAIN.PY, L:{line_numb()}")
    print(f"statbar_pos_offset={statbar_pos_offset}")

health_potion_status = Item(statbar_pos_offset['health'], 23, 3, red_potion, True)
poison_potion_status = Item(statbar_pos_offset['poison'], 23, 3, green_potion, True)
mana_potion_status = Item(statbar_pos_offset['mana'], 23, 2, blue_potion, True)
score_status = Item(statbar_pos_offset['score'], 23, 0, coin_images, True)

item_group.add(health_potion_status)
item_group.add(poison_potion_status)
item_group.add(mana_potion_status)
item_group.add(score_status)

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
    print(f"MAIN.PY, line: {line_numb()}\n\nStats:\n {len(world.map_tiles)} tiles\n")
    print(f"    {len(item_group)} objects\n {len(enemy_list)} enemies")
    print(f"    c.rows= {constants.ROWS}, map width= {tmx_map.width}, c.cols={constants.COLS}, map height= {tmx_map.height}")
    print("\n\nSTARTING MAIN LOOP\n")

# main game loop
run = True
level_complete = False
loop_number = 0
damage_text = ""

while run:
    # control frame rate and handle delta time
    time_delta = clock.tick(constants.FPS) / 1000.0

    loop_number += 1

    if constants.DEBUG_LEVEL > 1:
        print(f"  line: {line_numb()}, loop_number={loop_number}, level_complete={level_complete}, run={run}, start_game={start_game}\n")
        print(f"     moving_up={moving_up}, moving_down={moving_down}, moving_left={moving_left}, moving_right={moving_right}")

    if not start_game and constants.DEBUG_LEVEL == 0:
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
                if constants.DEBUG_FAST_TRAVEL:
                    speed = 10
                else:
                    speed = character_classes_dict['player']['speed']
                dx = 0
                dy = 0
                if moving_right:
                    dx = speed
                if moving_left:
                    dx = -speed
                if moving_up:
                    dy = -speed
                if moving_down:
                    dy = speed
                if use_health_potion:
                    if player.health_potions:
                        player.health_potions -= 1
                        player.health += 10
                        heal_fx.play()
                        use_health_potion = False
                if use_mana_potion:
                    if player.mana_potions:
                        player.mana_potions -= 1
                        player.mana += 10
                        heal_fx.play()
                        use_mana_potion = False
                if use_poison_potion:
                    if player.poison_potions:
                        player.poison_potions -= 1
                        player.poison -= 10
                        heal_fx.play()
                        use_poison_potion = False

                # move player
                screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, enemy_list, time_delta, world.exit_tile)

                # update all objects
                world.update(screen_scroll)
                for enemy in enemy_list:
                    # TODO : why is fireball = enemy.ai run for every enemy?  How about lightning?
                    fireball, lightning = enemy.ai(player, world.obstacle_tiles, enemy_list, screen_scroll, fireball_image,
                                                   lightning_image, character_classes_dict, time_delta)
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
                    damage, damage_pos, enemy_name = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list,
                                                                  player)

                    if damage:
                        new_damage, new_enemy_health = damage.split(" : ")
                        new_damage = -(int(new_damage))
                        new_enemy_health = int(new_enemy_health)

                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(new_damage), constants.RED)
                        damage_text_group.add(damage_text)

                        if new_enemy_health <= 0:
                            new_enemy_health = str("dead")
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y + 18, str(new_enemy_health),
                                                     constants.BLUE)

                            get_loot(player, enemy, damage_pos.centerx, damage_pos.centery)
                        else:
                            damage_text = DamageText(damage_pos.centerx, damage_pos.y + 18, str(new_enemy_health),
                                                     constants.GREEN)
                        damage_text_group.add(damage_text)
                        if constants.DEBUG_SHOW_HIT_DAMAGE:
                            print(f"  {new_damage} damage to {enemy_name}.  HP: {new_enemy_health}")
                        hit_fx.play()

                damage_text_group.update(time_delta)
                fireball_group.update(screen_scroll, player)
                lightning_group.update(screen_scroll, player)

                enemy_stats_sprite_group.update(time_delta, screen_scroll)

                item_group.update(screen_scroll, player, coin_fx, heal_fx, time_delta)

                if player.level_complete:
                    level_complete = True
                    if constants.DEBUG_LEVEL:
                        print(f"MAIN.PY, line:{line_numb()}, Level {world.map_level} Completed")

            world.draw(screen)
            item_group.draw(screen)

            # draw player on screen
            player.draw(screen)
            bow.draw(screen)
            player.draw_health(screen)

            # draw enemies
            for enemy in enemy_list:
                if constants.DEBUG_LEVEL > 1:
                    print(f" MAIN.PY, F:main loop, line={line_numb()}, enemy.name={enemy_name}")
                    print(f"   enemy.image={enemy.image}")
                enemy.draw(screen)
                enemy.draw_health(screen)

            # put player.draw here to have player on top of enemies, leave above for enemies to be on top.
            # player.draw(screen)

            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            for lightning in lightning_group:
                lightning.draw(screen)
            damage_text_group.draw(screen)
            draw_statusbar_info()
            score_status.draw(screen)
            mana_potion_status.draw(screen)
            poison_potion_status.draw(screen)
            health_potion_status.draw(screen)

        # check level complete
        if level_complete:
            start_intro = True
            level += 1

            world_data = reset_level()

            # load in the level data
            if constants.DEBUG_LEVEL:
                path = "assets/levels/testing2.tmx"
            else:
                path = f"assets/levels/level{level}.tmx"

            try:
                tmx_map = load_pygame(path)

            except:
                print(f"MAIN.PY line:{line_numb()} Unable to load TMX file: {path}")
                print("-Check path\n-Make sure you can open the file in Tiled\n")
                print("-Check Tiled icons / locate correct folders")
                pygame.quit()
                exit()

            world = World(character_classes_dict)
            success = world.process_data(tmx_map, item_images, mob_dict, enemy_stats_sprite_group)

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
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # show death screen
        if not player.alive:
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    start_game = True
                    world_data = reset_level()

                    path = f"assets/levels/level{level}.tmx"

                    try:
                        tmx_map = load_pygame(path)

                    except:
                        print(f"MAIN.PY line:{line_numb()} Unable to load TMX file: {path}")
                        pygame.quit()
                        exit()

                    world = World(character_classes_dict)
                    success = world.process_data(tmx_map, item_images, mob_dict, enemy_stats_sprite_group)
                    if not success:
                        print(f"  world.process_data failed in MAIN.PY, line:{line_numb()}")
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
                case pygame.K_SPACE:
                    use_health_potion = True
                case pygame.K_m:
                    use_mana_potion = True
                case pygame.K_p:
                    use_poison_potion = True
                    player.exp += 199

                case pygame.K_ESCAPE:
                    pause_game = True

        if event.type == pygame.VIDEORESIZE:
            # scrsize = event.size
            width = event.w
            height = event.h
            constants.SCREEN_WIDTH = event.w
            constants.SCREEN_HEIGHT = event.h

            for item in text_pos_percentage:
                statbar_pos_offset[item] = int(constants.SCREEN_WIDTH * text_pos_percentage[item] / 100)

            _, y= health_potion_status.rect.center
            health_potion_status.rect.center = (statbar_pos_offset['health'], y)
            poison_potion_status.rect.center = (statbar_pos_offset['poison'], y)
            mana_potion_status.rect.center = (statbar_pos_offset['mana'], y)
            score_status.rect.center = (statbar_pos_offset['score'], y)

            screen = pygame.display.set_mode((width, height),
                                             pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)

        # keyboard button released
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_a:
                    moving_left = False
                case pygame.K_d:
                    moving_right = False
                case pygame.K_w:
                    moving_up = False
                case pygame.K_SPACE:
                    use_health_potion = False
                case pygame.K_m:
                    use_mana_potion = False
                case pygame.K_p:
                    use_poison_potion = False

                case pygame.K_s:
                    # item_group.update(screen_scroll, player, coin_fx, heal_fx, time_delta)
                    moving_down = False

    if constants.GOD_MODE:
        if player and player.health < 50:
            player.health = player.character_classes_dict['player']['hp']
            print(f"  *GOD_MODE* has restored your health to {player.character_classes_dict['player']['hp']}")

    # show fps
    if constants.FPS_MONITOR:
        fps.render(str(level))
        fps.clock.tick(constants.FPS)

    pygame.display.update()
#     pygame.display.flip()

pygame.quit()
