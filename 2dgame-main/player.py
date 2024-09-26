from idlelib.debugger_r import frametable

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


class Player:
    def __init__(self, Screen,ScreenWidth,ScreenHeight):
        self.screen = Screen
        self.screenwidth = ScreenWidth
        self.screenheight = ScreenHeight

        self.walk_up_animation = self.create_animation('Knight_10_Walk_Up.png',4)
        self.walk_down_animation = self.create_animation('Knight_10_Walk_Down.png', 4)
        self.walk_left_animation = self.create_animation('Knight_10_Walk_Left.png', 4)
        self.walk_right_animation = self.create_animation('Knight_10_Walk_Right.png', 4)
        self.sword_up_animation = self.create_animation('Knight_10_Sword_Up.png', 4)
        self.sword_down_animation = self.create_animation('Knight_10_Sword_Down.png', 4)
        self.sword_left_animation = self.create_animation('Knight_10_Sword_Left.png', 4)
        self.sword_right_animation = self.create_animation('Knight_10_Sword_Right.png', 4)

        self.current_animation = self.walk_down_animation
        self.idle = True
        self.frame = 0
        self.animation_cooldown = 200
        self.sword = False
        self.sword_cooldown = False
        self.sword_cooldown_time = 1000
        self.last_update = pygame.time.get_ticks()
        self.last_sword_update = pygame.time.get_ticks()

        self.player_health = 3
        self.player_width = 50
        self.player_height = 50
        self.player_x = 250
        self.player_y = 250
        self.player_speed = 0.1
        self.player_x_direction = 0
        self.player_y_direction = 0
        self.vector_correction = 1

        self.keys = {pygame.K_a: [-1, self.walk_left_animation,self.sword_left_animation],
                     pygame.K_d: [1, self.walk_right_animation,self.sword_right_animation],
                     pygame.K_w: [-1, self.walk_up_animation,self.sword_up_animation],
                     pygame.K_s: [1, self.walk_down_animation,self.sword_down_animation]}
        self.currently_pressed_keys = []
        self.last_key_pressed = pygame.K_s

    def switch_animation(self,new_animation=None):
        if self.sword == False:
            self.current_animation = new_animation
        elif self.sword:
            self.current_animation = self.keys[self.last_key_pressed][2]

    def detect_input(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.sword_cooldown == False:
                self.sword = True
                self.animation_cooldown = 50
                self.switch_animation()
                self.frame = 0
                self.player_speed = 0.25
                self.sword_cooldown = True
                self.last_sword_update = self.current_time
            # This if is for interacting with things
            if event.button == 2:
                pass

        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.last_key_pressed = event.key
                self.currently_pressed_keys.append(event.key)
                self.switch_animation(self.keys[event.key][1])
                self.idle = False
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player_x_direction = self.keys[event.key][0]
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    self.player_y_direction = self.keys[event.key][0]
                if self.player_x_direction != 0 and self.player_y_direction != 0:
                    self.vector_correction = 0.7071

        if event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.currently_pressed_keys.remove(event.key)
                if self.currently_pressed_keys == []:
                    self.idle = True
                if pygame.K_a not in self.currently_pressed_keys and pygame.K_d not in self.currently_pressed_keys:
                    self.player_x_direction = 0
                if pygame.K_w not in self.currently_pressed_keys and pygame.K_s not in self.currently_pressed_keys:
                    self.player_y_direction = 0
                if self.player_x_direction + self.player_y_direction != 1 or self.player_x_direction + self.player_y_direction != -1:
                    self.vector_correction = 1

    def play_animation(self,):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
        if self.frame >= len(self.current_animation):
            self.frame = 0
            self.sword = False
            self.current_animation = self.keys[self.last_key_pressed][1]
            self.animation_cooldown = 200
            self.player_speed = 0.1
        if self.idle and self.sword == False:
            self.frame = 0
        if self.current_time - self.last_sword_update >= self.sword_cooldown_time:
            self.sword_cooldown = False
        self.screen.blit(self.current_animation[self.frame],(self.player_x - self.player_width / 2, self.player_y - self.player_height / 2))





    def update_player_position(self,):
        if self.player_x_direction > 0:
            if self.player_x <self.screenwidth - self.player_width:
                self.player_x += self.player_x_direction * self.player_speed * self.vector_correction
        if self.player_x_direction < 0:
            if self.player_x > 0:
                self.player_x += self.player_x_direction * self.player_speed * self.vector_correction
        if self.player_y_direction > 0:
            if self.player_y <self.screenheight - self.player_height:
                self.player_y += self.player_y_direction * self.player_speed * self.vector_correction
        if self.player_y_direction < 0:
            if self.player_y > 0:
                self.player_y += self.player_y_direction * self.player_speed * self.vector_correction
    def create_animation(self,sprite_sheet_image,animation_steps):
        self.sprite_sheet_image = pygame.image.load(sprite_sheet_image).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.frame_list = []
        for x in range(animation_steps):
            self.frame_list.append(self.sprite_sheet.get_image(x, 32, 32, 3, BLACK))
        return self.frame_list


player = Player(screen,SCREEN_WIDTH,SCREEN_HEIGHT)

run = True
while run:
    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.detect_input(event)
    player.play_animation()
    player.update_player_position()
    #    pygame.draw.rect(screen,BLACK,[Player.player_x,Player.player_y,Player.player_width,Player.player_height])
    pygame.display.update()
pygame.quit()