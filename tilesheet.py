import pygame


class Tilesheet:
    def __init__(self, filename, width, height, rows, cols, start_row_index=0):
        """ The function creates the whole Tilesheet, not just a row of tiles"""
        self.filename = filename
        self.rows = rows
        self.cols = cols
        self.start_row_index = start_row_index
        image = pygame.image.load(filename).convert_alpha()
        self.tile_table = []

        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(start_row_index, rows):
                rect = (tile_x * width, tile_y * height, width, height)
                line.append(image.subsurface(rect))

    def get_tile(self, x, y):
        return self.tile_table[x][y]

    def draw(self, screen):
        # draws all tiles of tilesheet
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x * 72, y * 72))
