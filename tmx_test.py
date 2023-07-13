from pytmx.util_pygame import *
import pygame


def line_numb():
    ''' Returns the current line number in our program
    '''
    return inspect.currentframe().f_back.f_lineno


# load in the level data
    # path = "assets/levels/level1.tmx"
path = "assets/levels/test-error.tmx"

if constants.DEBUG_LEVEL:
    print("MAIN.PY, line:{}, Loading TMX_MAP file: {}".format(line_numb(), path))

try:
    tmx_map = load_pygame(path)

except:
    print("MAIN.PY line:{}\n Unable to load TMX file: {}".format(line_numb(), path))
    pygame.quit()
    exit()

print("loaded fine")
