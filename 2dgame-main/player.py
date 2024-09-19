import pygame
from pygame.display import update

import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')


sprite_sheet_image = pygame.image.load('Knight_10_Walk_Down.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

player_width = 50
player_height = 50
player_x = 250
player_y = 250
player_speed = 0.1
player_x_direction = 0
player_y_direction = 0

BG = (50, 50, 50)
BLACK = (0, 0, 0)

frame_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 200
frame = 0

for x in range(animation_steps):
    frame_list.append(sprite_sheet.get_image(x, 32, 32, 3, BLACK))

def update_player_position():
    global player_x
    global player_y
    global player_x_direction
    global player_y_direction
    if player_x_direction > 0:
        if player_x <500 - player_width:
            player_x += player_x_direction * player_speed
    if player_x_direction < 0:
        if player_x > 0:
            player_x += player_x_direction * player_speed
    if player_y_direction > 0:
        if player_y <500 - player_height:
            player_y += player_y_direction * player_speed
    if player_y_direction < 0:
        if player_y > 0:
            player_y += player_y_direction * player_speed

run = True
while run:
    screen.fill(BG)
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(frame_list):
            frame = 0

    screen.blit(frame_list[frame], (player_x-player_width/2, player_y-player_height/2))
    update_player_position()
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_direction = -1
            if event.key == pygame.K_d:
                player_x_direction = 1
            if event.key == pygame.K_w:
                player_y_direction = -1
            if event.key == pygame.K_s:
                player_y_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_x_direction = 0
            if event.key == pygame.K_d:
                player_x_direction = 0
            if event.key == pygame.K_w:
                player_y_direction = 0
            if event.key == pygame.K_s:
                player_y_direction = 0
#	pygame.draw.rect(screen,BG,[player_x,player_y,player_width,player_height])
    pygame.display.update()
pygame.quit()

