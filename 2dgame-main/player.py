import pygame
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
        self.player_speed = 0.2
        self.player_x_direction = 0
        self.player_y_direction = 0
        self.vector_correction = 1
        self.position_change_cooldown = 1
        self.last_position_update = pygame.time.get_ticks()

        self.keys = {pygame.K_a: [-1, self.walk_left_animation,self.sword_left_animation],
                     pygame.K_d: [1, self.walk_right_animation,self.sword_right_animation],
                     pygame.K_w: [-1, self.walk_up_animation,self.sword_up_animation],
                     pygame.K_s: [1, self.walk_down_animation,self.sword_down_animation],
                     "None":[0]}
        self.currently_pressed_keys = []
        self.last_key_pressed = pygame.K_s
        self.xkeys_pressed = ["None"]
        self.ykeys_pressed = ["None"]

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.play_animation()
        self.update_player_position()

    def switch_animation(self,Index=1):
        if self.sword:
            Index = 2
        if self.currently_pressed_keys:
            self.current_animation = self.keys[self.currently_pressed_keys[-1]][Index]
        else:
            self.current_animation = self.keys[self.last_key_pressed][Index]


    def changedirection(self,):
        if pygame.K_a in self.currently_pressed_keys or pygame.K_d in self.currently_pressed_keys or "None":
            self.player_x_direction = self.keys[self.xkeys_pressed[-1]][0]
        if pygame.K_w in self.currently_pressed_keys or pygame.K_s in self.currently_pressed_keys or "None":
            self.player_y_direction = self.keys[self.ykeys_pressed[-1]][0]
        self.switch_animation()

        if self.player_x_direction + self.player_y_direction in (-1, 1):
            self.vector_correction = 1
        else:
            self.vector_correction = 0.7071

    def detect_input(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.currently_pressed_keys.append(event.key)
                self.idle = False
                if event.key in (pygame.K_a, pygame.K_d):
                    self.xkeys_pressed.append(event.key)
                else:
                    self.ykeys_pressed.append(event.key)

                self.changedirection()

        if event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.last_key_pressed = event.key
                self.currently_pressed_keys.remove(event.key)
                if self.currently_pressed_keys == []:
                    self.idle = True
                if event.key in self.xkeys_pressed:
                    self.xkeys_pressed.remove(event.key)
                else:
                    self.ykeys_pressed.remove(event.key)

                self.changedirection()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.sword_cooldown == False:
                self.sword = True
                self.animation_cooldown = 50
                self.switch_animation()
                self.frame = 0
                self.player_speed = 0.5
                self.sword_cooldown = True
                self.last_sword_update = self.current_time
            # This if is for interacting with things
            if event.button == 2:
                pass

    def play_animation(self,):
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = self.current_time
        if self.frame >= len(self.current_animation):
            self.frame = 0
            self.sword = False
            self.animation_cooldown = 200
            self.player_speed = 0.2
            self.switch_animation()
        if self.idle and self.sword == False:
            self.frame = 0
        if self.current_time - self.last_sword_update >= self.sword_cooldown_time:
            self.sword_cooldown = False
        self.screen.blit(self.current_animation[self.frame],(self.player_x - self.player_width / 2, self.player_y - self.player_height / 2))

    def update_player_position(self,):
        if self.current_time - self.last_position_update >= 1:
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
            self.last_position_update = self.current_time

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
    player.update()
    #    pygame.draw.rect(screen,BLACK,[Player.player_x,Player.player_y,Player.player_width,Player.player_height])
    pygame.display.update()
pygame.quit()