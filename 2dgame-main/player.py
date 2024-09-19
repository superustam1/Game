import pygame
from pygame.display import update

import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG = (50, 50, 50)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')


class player:
    def __init__(self):
        self.player_health = 3
        self.player_width = 50
        self.player_height = 50
        self.player_x = 250
        self.player_y = 250
        self.player_speed = 0.1
        self.player_x_direction = 0
        self.player_y_direction = 0
        self.walk_up_animation = self.createanimation('Knight_10_Walk_Up.png',4)
        self.walk_down_animation = self.createanimation('Knight_10_Walk_Down.png', 4)
        self.walk_left_animation = self.createanimation('Knight_10_Walk_Left.png', 4)
        self.walk_right_animation = self.createanimation('Knight_10_Walk_Right.png', 4)
        self.current_animation = self.walk_down_animation



    def createanimation(self,sprite_sheet_image,animation_steps):
        self.sprite_sheet_image = pygame.image.load(sprite_sheet_image).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.frame_list = []
        for x in range(animation_steps):
            self.frame_list.append(self.sprite_sheet.get_image(x, 32, 32, 3, BLACK))
        return self.frame_list



    def detectkey(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.player_x_direction = -1
                self.current_animation = self.walk_left_animation
            if event.key == pygame.K_d:
                self.player_x_direction = 1
                self.current_animation = self.walk_right_animation
            if event.key == pygame.K_w:
                self.player_y_direction = -1
                self.current_animation = self.walk_up_animation
            if event.key == pygame.K_s:
                self.player_y_direction = 1
                self.current_animation = self.walk_down_animation
            print(self.current_animation)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.player_x_direction = 0
            if event.key == pygame.K_d:
                self.player_x_direction = 0
            if event.key == pygame.K_w:
                self.player_y_direction = 0
            if event.key == pygame.K_s:
                self.player_y_direction = 0

    def update_player_position(self):
        if self.player_x_direction > 0:
            if self.player_x <500 - self.player_width:
                self.player_x += self.player_x_direction * self.player_speed
        if self.player_x_direction < 0:
            if self.player_x > 0:
                self.player_x += self.player_x_direction * self.player_speed
        if self.player_y_direction > 0:
            if self.player_y <500 - self.player_height:
                self.player_y += self.player_y_direction * self.player_speed
        if self.player_y_direction < 0:
            if self.player_y > 0:
                self.player_y += self.player_y_direction * self.player_speed




last_update = pygame.time.get_ticks()
animation_cooldown = 200
frame = 0
Player = player()

run = True
while run:
    screen.fill(BG)
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(Player.current_animation):
            frame = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        Player.detectkey(event)

    screen.blit(Player.current_animation[frame], (Player.player_x-Player.player_width/2, Player.player_y-Player.player_height/2))
    Player.update_player_position()
    #event handler

#	pygame.draw.rect(screen,BG,[player_x,player_y,player_width,player_height])
    pygame.display.update()
pygame.quit()

