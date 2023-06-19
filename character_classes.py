character_classes = [
    {"name": "Warrior", "run": 6, "idle": 60, "attack": 12, "death": 12, "exp": 10, "hp": 200, "scale": .2, "speed": 3,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 10, 10], "trim_rect": [0, 0, 0, 0]},

    # normal creatures, no special attacks

    # {"name": "Bear", "run": 6, "idle": 35, "attack": 28, "death": 21, "exp": 20, "hp": 200, "scale": 1.5, "speed": 2,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True,
    #  "animation_cooldown": 150, "run_cooldown": 75,
    #  "trim_hitbox": [30, 60, 80, 30], "trim_rect": [120, 90, 90, 150]},
    #
    # {"name": "Deer",
    #  "run": 7, "idle": 22, "attack": 17, "death": 17, "exp": 10, "hp": 100, "scale": 1, "speed": 7,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [30, 50, 30, 10], "trim_rect": [80, 80, 100, 155]},
    # {"name": "Eagle",
    #  "run": 9, "idle": 11, "attack": 14, "death": 17, "exp": 10, "hp": 100, "scale": 1, "speed": 7,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [50, 100, 20, 70], "trim_rect": [50, 120, 50, 150]},
    # {"name": "Fox",
    #  "run": 5, "idle": 39, "attack": 17, "death": 15, "exp": 10, "hp": 100, "scale": 1, "speed": 5,
    #  "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [20, 20, 30, 10], "trim_rect": [125, 120, 150, 160]},
    # {"name": "Goat",
    #  "run": 6, "idle": 6, "attack": 14, "death": 16, "exp": 10, "hp": 100, "scale": 1, "speed": 4,
    #  "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [30, 30, 10, 10], "trim_rect": [0, 0, 10, 20]},
    # {"name": "Insect", "run": 20, "idle": 20, "attack": 24, "death": 35, "exp": 20, "hp": 200, "scale": .5, "speed": 6,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
    #  "trim_hitbox": [50, 50, 50, 50], "trim_rect": [50, 90, 75, 75]},
    # {"name": "Meerkat", "run": 5, "idle": 29, "attack": 11, "death": 17, "exp": 10, "hp": 100, "scale": 1, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [55, 15, 20, 5], "trim_rect": [125, 160, 170, 155]},
    # {"name": "Panther", "run": 6, "idle": 23, "attack": 14, "death": 20, "exp": 15, "hp": 150, "scale": 2, "speed": 6,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [90, 40, 60, 30], "trim_rect": [120, 130, 155, 150]},
    # {"name": "Raven", "run": 7, "idle": 9, "attack": 12, "death": 24, "exp": 10, "hp": 100, "scale": 1, "speed": 8,
    #  "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
    #  "trim_hitbox": [20, 20, 30, 110], "trim_rect": [120, 120, 80, 120]},
    # {"name": "Snake", "run": 7, "idle": 18, "attack": 13, "death": 14, "exp": 10, "hp": 100, "scale": 1, "speed": 7,
    #  "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [50, 50, 20, 10], "trim_rect": [110, 100, 160, 150]},
    # {"name": "Wolf", "run": 6, "idle": 39, "attack": 14, "death": 18, "exp": 15, "hp": 150, "scale": 1.5, "speed": 6,
    #  "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
    #  "trim_hitbox": [40, 60, 30, 20], "trim_rect": [120, 120, 155, 155]},

    # mid level attackers

    # {"name": "Cyclops1", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "fly": 13, "hp": 200,
    #  "scale": .5, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [100, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    # {"name": "Cyclops2", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "fly": 13, "hp": 200,
    #  "scale": .5, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [100, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    # {"name": "Cyclops3", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "fly": 13, "hp": 200,
    #  "scale": .5, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [100, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    #
    # {"name": "Elemental1",
    #  "run": 5, "idle": 5, "attack": 5, "death": 5, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    # {"name": "Elemental2",
    #  "run": 5, "idle": 5, "attack": 5, "death": 5, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    # {"name": "Elemental3",
    #  "run": 5, "idle": 5, "attack": 5, "death": 5, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
    #  "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
    #  "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Jinn",
     "run": 4, "idle": 3, "attack": 4, "death": 6, "exp": 25, "hp": 200, "scale": 1.5, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Knight Man", "run": 20, "idle": 76, "attack": 45, "death": 69, "exp": 20, "hp": 100, "scale": 1,
     "speed": 5,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True,
     "animation_cooldown": 25, "run_cooldown": 75,
     "trim_hitbox": [120, 120, 10, 10], "trim_rect": [75, 75, 150, 170]},
    {"name": "Magic Fox", "run": 16, "idle": 20, "attack": 16, "death": 20, "exp": 50, "hp": 200, "scale": .75,
     "speed": 7,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [30, 100, 110, 60], "trim_rect": [90, 85, 70, 80]},
    {"name": "Gaerron", "run": -1, "idle": 23, "attack": 14, "death": 20, "exp": 50, "hp": 200, "scale": 2, "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 150,
     "trim_hitbox": [30, 30, 20, 30], "trim_rect": [20, 20, 20, 0]},
    {"name": "Lord Esther", "run": -1, "idle": 23, "attack": 14, "death": 20, "exp": 50, "hp": 200, "scale": 2,
     "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [50, 50, 20, 10], "trim_rect": [0, 0, 0, 0]},
    {"name": "PrinceTaerron", "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 50, "hp": 200, "scale": .5,
     "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 250,
     "trim_hitbox": [50, 50, 10, 10], "trim_rect": [5, 5, 25, 25]},
    {"name": "Little Demon", "run": 6, "idle": 3, "attack": 4, "death": 6, "exp": 50, "hp": 200, "scale": 1, "speed": 3,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "Fireball", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [30, 40, 40, 20], "trim_rect": [30, 80, 60, 50]},


    {"name": "Skeleton", "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 50, "hp": 200, "scale": 1.25,
     "speed": 5,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 50,
     "trim_hitbox": [70, 70, 50, 50], "trim_rect": [70, 30, 50, 0]},

    {"name": "Skeleton2", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200,
     "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [50, 1, 1, 1],
     "trim_rect": [0, 0, 0, 0]},
    {"name": "Skeleton3", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200,
     "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [50, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Skeleton4", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200,
     "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [50, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Thief", "run": 16, "idle": 24, "attack": 24, "death": 24, "exp": 10, "hp": 100, "scale": .65, "speed": 6,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 10, 10], "trim_rect": [0, 0, 0, 0]},

    # boss level attackers

    {"name": "Crocodile Warrior", "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 100, "hp": 250, "scale": .75,
     "speed": 5,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [130, 40, 10, 10], "trim_rect": [150, 10, 75, 5]},
    {"name": "Crab Monster", "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 100, "hp": 250, "scale": 1,
     "speed": 3,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 150,
     "trim_hitbox": [70, 130, 5, 5], "trim_hitbox_320": [50, 70, 10, 10],
     "trim_rect": [150, 70, 100, 0], "trim_rect_320": [70, 35, 50, 0]},
    {"name": "Red Demon",
     "run": -1, "idle": 23, "attack": 14, "death": 20, "exp": 100, "hp": 250, "scale": 1.4,
     "speed": 3,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "Fireball", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 10, 10], "trim_rect": [25, 50, 50, 50]},
    {"name": "Reptile Warrior",
     "run": 16, "idle": 20, "attack": 24, "death": 16, "exp": 100, "hp": 250, "scale": 1.25,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [50, 130, 50, 80], "trim_rect": [100, 110, 140, 100]},
    {"name": "Saurial",
     "run": -1, "idle": 23, "attack": 14, "death": 20, "exp": 60, "hp": 300, "scale": 1.2,
     "speed": 6,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "Lightning", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 10, 10], "trim_rect": [0, 0, 0, 0]},
    {"name": "SunkenGod",
     "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 50, "hp": 250, "scale": .5,
     "speed": 5,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 150,
     "trim_hitbox": [30, 30, 30, 40],
     "trim_rect": [60, 60, 15, 70]},
    {"name": "TheOldKing",
     "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 100, "hp": 300, "scale": 1,
     "speed": 5,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 80, 100],
     "trim_rect": [40, 40, 40, 40]},
    {"name": "TheTriplets",
     "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 75, "hp": 250, "scale": .5,
     "speed": 5,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": False, "animation_cooldown": 150,
     "trim_hitbox": [20, 50, 10, 50],
     "trim_rect": [0, 0, 0, 30]},
    {"name": "Witch",
     "run": -1, "idle": -1, "attack": -1, "death": -1, "exp": 25, "hp": 200, "scale": .5, "speed": 4,
     "is_Hitbox_Symmetrical": True, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [10, 10, 10, 10], "trim_rect": [0, 0, 0, 0]},

    {"name": "GHOST1",
     "run": 7, "idle": 7, "attack": 7, "death": 6, "exp": 25, "hp": 200, "scale": .1, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "GHOST2",
     "run": 7, "idle": 7, "attack": 7, "death": 6, "exp": 25, "hp": 200, "scale": .1, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "GHOST3",
     "run": 7, "idle": 7, "attack": 7, "death": 6, "exp": 25, "hp": 200, "scale": .1, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Goblin1",
     "run": 19, "idle": 9, "attack": 9, "death": 19, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [5, 60, 30, 5], "trim_rect": [0, 0, 0, 0]},
    {"name": "Goblin2", "run": 19, "idle": 9, "attack": 9, "death": 19, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [5, 60, 30, 5], "trim_rect": [0, 0, 0, 0]},
    {"name": "Goblin3", "run": 19, "idle": 9, "attack": 9, "death": 19, "exp": 25, "hp": 200, "scale": .15, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 50,
     "trim_hitbox": [5, 60, 30, 5], "trim_rect": [0, 0, 0, 0]},

    {"name": "Golem1",
     "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Golem2", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Golem3", "run": 10, "idle": 10, "attack": 10, "death": 10, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Dragon1",
     "run": 16, "idle": 26, "attack": 33, "death": 13, "exp": 25, "fly": 13, "hp": 200, "scale": .5,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [60, 130, 100, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Dragon2", "run": 16, "idle": 26, "attack": 33, "death": 13, "exp": 25, "fly": 13, "hp": 200, "scale": .25,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Dragon3", "run": 16, "idle": 26, "attack": 33, "death": 13, "exp": 25, "fly": 13, "hp": 200, "scale": .25,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Orc1", "run": 10, "idle": 10, "attack": 15, "death": 10, "exp": 25, "fly": 13, "hp": 200, "scale": .5,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Orc2", "run": 10, "idle": 10, "attack": 15, "death": 10, "exp": 25, "fly": 13, "hp": 200, "scale": .5,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Orc3", "run": 10, "idle": 10, "attack": 15, "death": 10, "exp": 25, "fly": 13, "hp": 200, "scale": .5,
     "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 100,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Minotaur1",
     "run": 10, "idle": 10, "attack": 10, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Minotaur2",
     "run": 10, "idle": 10, "attack": 10, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Minotaur3",
     "run": 10, "idle": 10, "attack": 10, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Undead1",
     "run": 20, "idle": 20, "attack": 20, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Undead2",
     "run": 20, "idle": 20, "attack": 20, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Undead3",
     "run": 20, "idle": 20, "attack": 20, "death": 13, "exp": 25, "hp": 200, "scale": .25, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 75,
     "trim_hitbox": [50, 30, 1, 1], "trim_rect": [0, 0, 0, 0]},

    {"name": "Zombie1",
     "run": 10, "idle": 4, "attack": 6, "death": 8, "exp": 25, "hp": 200, "scale": .5, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Zombie2", "run": 10, "idle": 4, "attack": 6, "death": 8, "exp": 25, "hp": 200, "scale": .5, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]},
    {"name": "Zombie3", "run": 10, "idle": 4, "attack": 6, "death": 8, "exp": 25, "hp": 200, "scale": .5, "speed": 4,
     "is_Hitbox_Symmetrical": False, "Special_Attack": "None", "flip_image": True, "animation_cooldown": 150,
     "trim_hitbox": [1, 1, 1, 1], "trim_rect": [0, 0, 0, 0]}]

