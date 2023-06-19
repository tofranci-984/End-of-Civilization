import pygame
import pytmx

# Load the tiled map
tmx_map = pytmx.TiledMap("assets/images/environment/basic.tmx")

# Create a surface to display the map
print(f"width = {tmx_map.width}, tilewidth={tmx_map.tilewidth}, height={tmx_map.height}, tileheight={tmx_map.tileheight}")
map_surface = pygame.Surface((tmx_map.width * tmx_map.tilewidth, tmx_map.height * tmx_map.tileheight))

# Load the tileset image
#tileset_image = pygame.image.load("assets/images/environment/basic.tmx")

# Loop through all layers and draw the tiles
for layer in tmx_map.layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_map.get_tile_image_by_gid(gid)
            if tile:
                print(f"x ={x}, y={y}, gid={gid}, layer={layer.name}")
                map_surface.blit(tile[0], (x * tmx_map.tilewidth, y * tmx_map.tileheight))

# Loop through all object layers and draw the objects
for object_layer in tmx_map.layers:
    if isinstance(object_layer, pytmx.TiledObjectGroup):
        for obj in object_layer:
            pass  # handle each object

# Display the map
pygame.init()
screen = pygame.display.set_mode((tmx_map.width * tmx_map.tilewidth, tmx_map.height * tmx_map.tileheight))
while True:
    screen.blit(map_surface, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
