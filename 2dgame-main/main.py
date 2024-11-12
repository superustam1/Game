import pygame
from pytmx.util_pygame import load_pygame
from player import Player


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
BG = (50, 50, 50)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_data = load_pygame('./Maps/FirstMap.tmx')
sprite_group = pygame.sprite.Group()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, sprites):
        super().__init__(sprites)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, surf, sprites,rects, height=None, width=None):
        super().__init__(sprites)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.center = self.hitbox.center
        rects.append(self.hitbox)
        if height:
            self.height = height
            self.hitbox.width -= 20
            pos[1] += 64
            self.hitbox.bottomleft = pos
            self.hitbox.height = self.height
            self.hitbox.centerx = self.center[0]
        if width:
            self.width = width

            self.hitbox.width = self.width
            self.hitbox.center = self.center




def CreateSpriteGroup(Layer_Name):
    sprite_group = pygame.sprite.Group()

    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data') and layer.name == Layer_Name:
            tile_dict = {(x, y): surf for x, y, surf in tmx_data.get_layer_by_name(Layer_Name).tiles()}
            processed_tiles = set()  # To keep track of processed tiles

            for x, y, surf in layer.tiles():
                if (x, y) not in processed_tiles:
                    pos = [x * tmx_data.tilewidth, y * tmx_data.tileheight]

                    tree_image = pygame.Surface((tmx_data.tilewidth * 2, tmx_data.tileheight * 2), pygame.SRCALPHA)
                    tree_image.blit(surf, (0, 0))  # Top-left
                    tree_image.blit(tile_dict.get((x + 1, y)), (tmx_data.tilewidth, 0))  # Top-right
                    tree_image.blit(tile_dict.get((x, y + 1)), (0, tmx_data.tileheight))  # Bottom-left
                    tree_image.blit(tile_dict.get((x + 1, y + 1)),
                    (tmx_data.tilewidth, tmx_data.tileheight))  # Bottom-right
                    tile = Tile(pos, tree_image,sprite_group)

                    processed_tiles.update([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)])
    return sprite_group


def load_walls_from_tmx(layer_name):
    wall_group = pygame.sprite.Group()
    wall_rects = []
    layer = tmx_data.get_layer_by_name(layer_name)
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    # Dictionary of all tiles on the specified layer
    tile_dict = {(x, y): surf for x, y, surf in layer.tiles()}
    processed_tiles = set()  # To keep track of processed tiles

    for (x, y), surf in tile_dict.items():
        if (x, y) in processed_tiles:
            continue  # Skip already processed tiles

        # Check for horizontal wall segment
        wall_length = 1
        while (x + wall_length, y) in tile_dict and (x + wall_length, y) not in processed_tiles:
            wall_length += 1

        if wall_length > 1:  # Horizontal wall detected
            pos = [x * tile_width, y * tile_height]
            wall_image = pygame.Surface((wall_length * tile_width, tile_height), pygame.SRCALPHA)

            # Blit each tile in the wall segment onto the wall_image
            for i in range(wall_length):
                wall_image.blit(tile_dict[(x + i, y)], (i * tile_width, 0))
                processed_tiles.add((x + i, y))

            # Create and add the horizontal wall sprite as one contiguous sprite
            wall_sprite = Wall(pos, wall_image, wall_group,wall_rects,height=5)

        else:  # Check for vertical wall segment if no horizontal wall is found
            wall_height = 1
            while (x, y + wall_height) in tile_dict and (x, y + wall_height) not in processed_tiles:
                wall_height += 1

            if wall_height > 1:  # Vertical wall detected
                pos = [x * tile_width, y * tile_height]
                wall_image = pygame.Surface((tile_width, (wall_height) * tile_height), pygame.SRCALPHA)

                # Blit each tile in the vertical wall segment onto the wall_image
                for j in range(wall_height-1):
                    wall_image.blit(tile_dict[(x, y + j)], (0, j * tile_height))
                    processed_tiles.add((x, y + j))

                # Create and add the vertical wall sprite as one contiguous sprite
                wall_sprite = Wall(pos, wall_image, wall_group,wall_rects,width=12)

    return wall_group, wall_rects


def CreateLayerImage(layerNames):
    layer_surface = pygame.Surface((960, 640),pygame.SRCALPHA)
    for layer in tmx_data.visible_layers:
        if hasattr(layer,'data') and layer.name in layerNames:
            for x,y,surf in layer.tiles():
                pos = (x * 32, y * 32)
                layer_surface.blit(surf, pos)
    return layer_surface



all_sprites = pygame.sprite.LayeredUpdates()

player = Player(screen,SCREEN_WIDTH,SCREEN_HEIGHT)

Ground_Layer = CreateLayerImage(("Ground","Path"))
Apples_Layer = CreateLayerImage("Apples")
Walls_Sprites, Walls_Rects = load_walls_from_tmx("Walls")
Tree_group = CreateSpriteGroup("Trees")

all_sprites.add(player)
all_sprites.add(Tree_group)
all_sprites.add(Walls_Sprites)
run = True
Num = 0

while run:
    print(Num)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.detect_input(event)
    screen.fill(BG)
    screen.blit(Ground_Layer, (0, 0))
    screen.blit(Apples_Layer, (0, 0))
    player.update(Walls_Rects)
    print(player.current_time)

    for sprite in sorted(all_sprites, key=lambda sprite: sprite.hitbox.bottom):
        screen.blit(sprite.image, sprite.rect)
        #pygame.draw.rect(screen,(255, 0, 0),sprite.hitbox,1)
    pygame.display.update()
    Num += 1

pygame.quit()