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
    def __init__(self, pos, surf, sprites, movecoords, newsize):
        super().__init__(sprites)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.move(movecoords[0], movecoords[1])
        self.hitbox.width = newsize[0]
        self.hitbox.height = newsize[1]
    def Detect_Click(self, Mouse):
        return self.hitbox.collidepoint(Mouse.pos)

class Apple(pygame.sprite.Sprite):
    def __init__(self, pos, surf, sprites):
        super().__init__(sprites)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.move(5,0)
        self.hitbox.width = 22
        self.hitbox.height = 20
    def Detect_Click(self,Mouse):
        return self.hitbox.collidepoint(Mouse.pos)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, surf, sprites, rects, height=None, width=None):
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




def CreateSpriteGroup(Layer_Name,Class,Dimensions,HitboxMove=(0,0), HitboxSize=None):
    sprite_group = pygame.sprite.Group()
    for layer in tmx_data.visible_layers:
        if hasattr(layer, 'data') and layer.name == Layer_Name:
            tile_dict = {(x, y): surf for x, y, surf in tmx_data.get_layer_by_name(Layer_Name).tiles()}
            processed_tiles = set()  # To keep track of processed tiles
            for Tile_x, Tile_y, surf in layer.tiles():
                if (Tile_x, Tile_y) not in processed_tiles:
                    pos = [Tile_x * tmx_data.tilewidth, Tile_y * tmx_data.tileheight]
                    currently_processed_tiles = []
                    surface = pygame.Surface((tmx_data.tilewidth * Dimensions[0], tmx_data.tileheight * Dimensions[1]), pygame.SRCALPHA)
                    if HitboxSize == None:
                        HitboxSize = (surface.get_width(), surface.get_height())
                    for X in range(Dimensions[0]):
                        for Y in range(Dimensions[1]):
                            surface.blit(tile_dict.get((Tile_x + X, Tile_y + Y)), (tmx_data.tilewidth * X, tmx_data.tileheight * Y))
                            currently_processed_tiles.append((Tile_x + X, Tile_y + Y))
                    tile = Class(pos, surface, sprite_group,HitboxMove,HitboxSize)
                    processed_tiles.update(currently_processed_tiles)
    return sprite_group


def load_walls_from_tmx(layer_name):
    wall_group = pygame.sprite.Group()
    wall_rects = []
    layer = tmx_data.get_layer_by_name(layer_name)
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    # Include tile ID in the dictionary
    tile_dict = {}
    for x, y, surf in layer.tiles():
        gid = layer.data[y][x] if hasattr(layer, 'data') else None
        tile_dict[(x, y)] = {'surface': surf, 'id': gid}
    processed_tiles = set()  # To keep track of processed tiles

    for (x, y), tile_data in tile_dict.items():
        if (x, y) in processed_tiles:
            continue
        surf = tile_data['surface']
        tile_id = tile_data['id']
        wall_length = 1

        # Horizontal wall detection
        while (x + wall_length, y) in tile_dict and (x + wall_length, y) not in processed_tiles:
            wall_length += 1
        if wall_length > 1:
            pos = [x * tile_width, y * tile_height]
            wall_image = pygame.Surface((wall_length * tile_width, tile_height), pygame.SRCALPHA)
            for i in range(wall_length):
                wall_image.blit(tile_dict[(x + i, y)]['surface'], (i * tile_width, 0))
                processed_tiles.add((x + i, y))
            wall_sprite = Wall(pos, wall_image, wall_group, wall_rects, height=5)

        # Vertical wall detection
        else:
            wall_height = 1
            while (x, y + wall_height) in tile_dict and (x, y + wall_height) not in processed_tiles:
                wall_height += 1
            if wall_height > 1:
                pos = [x * tile_width, y * tile_height]
                wall_image = pygame.Surface((tile_width, wall_height * tile_height), pygame.SRCALPHA)
                for j in range(wall_height):
                    wall_image.blit(tile_dict[(x, y + j)]['surface'], (0, j * tile_height))
                    processed_tiles.add((x, y + j))
                wall_sprite = Wall(pos, wall_image, wall_group, wall_rects, width=12)
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
Apples_Layer = CreateSpriteGroup("Apples",Tile,(1,1),(5,0),(22,20))
Walls_Sprites, Walls_Rects = load_walls_from_tmx("Walls")
Tree_group = CreateSpriteGroup("Trees",Tile,(2,2))

all_sprites.add(player)
all_sprites.add(Tree_group)
all_sprites.add(Apples_Layer)
all_sprites.add(Walls_Sprites)
run = True
Num = 0

while run:
    print(Num)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.detect_input(event,all_sprites,Apples_Layer)
    screen.fill(BG)
    screen.blit(Ground_Layer, (0, 0))
    player.update(Walls_Rects)
    print(player.current_time)

    for sprite in sorted(all_sprites, key=lambda sprite: sprite.hitbox.bottom):
        screen.blit(sprite.image, sprite.rect)
        #pygame.draw.rect(screen,(255, 0, 0),sprite.hitbox,1)
    pygame.display.update()
    Num += 1

pygame.quit()