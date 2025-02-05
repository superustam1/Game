import pygame
import spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, Screen,ScreenWidth,ScreenHeight):
        super().__init__()
        self.screen = Screen
        self.screenwidth = ScreenWidth
        self.screenheight = ScreenHeight

        self.walk_up_animation = self.create_animation('CharacterModels/Knight_10_Walk_Up.png',4)
        self.walk_down_animation = self.create_animation('CharacterModels/Knight_10_Walk_Down.png', 4)
        self.walk_left_animation = self.create_animation('CharacterModels/Knight_10_Walk_Left.png', 4)
        self.walk_right_animation = self.create_animation('CharacterModels/Knight_10_Walk_Right.png', 4)
        self.sword_up_animation = self.create_animation('CharacterModels/Knight_10_Sword_Up.png', 4)
        self.sword_down_animation = self.create_animation('CharacterModels/Knight_10_Sword_Down.png', 4)
        self.sword_left_animation = self.create_animation('CharacterModels/Knight_10_Sword_Left.png', 4)
        self.sword_right_animation = self.create_animation('CharacterModels/Knight_10_Sword_Right.png', 4)

        self.current_animation = self.walk_down_animation
        self.idle = True
        self.frame = 0
        self.animation_cooldown = 200

        self.using_sword = False
        self.sword_cooldown = False
        self.sword_cooldown_time = 1000
        self.last_frame_update = pygame.time.get_ticks()
        self.last_sword_use = pygame.time.get_ticks()

        self.player_health = 3
        self.rect = self.current_animation[0].get_rect()
        self.image = self.current_animation[0]
        self.player_speed = 1.5
        self.vector_correction = 1
        self.player_x = 200
        self.player_y = 200
        self.player_x_direction = 0
        self.player_y_direction = 0
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

        self.padding_x = 23
        self.padding_y = 17
        self.hitbox = pygame.Rect(self.rect.x + self.padding_x,
                                  self.rect.y + self.padding_y, 50, 58)

        self.next_x = self.player_x + self.player_x_direction * self.player_speed * self.vector_correction
        self.next_y = self.player_y + self.player_y_direction * self.player_speed * self.vector_correction
        self.next_hitbox_x = self.hitbox.move(self.next_x - self.hitbox.x, 0)
        self.next_hitbox = self.hitbox.move(0, self.next_y - self.hitbox.y)

        self.left_side = pygame.Rect(self.hitbox.left - 1, self.hitbox.bottom, 1, 4)
        self.right_side = pygame.Rect(self.hitbox.right, self.hitbox.bottom, 1, 4)
        self.top_side = pygame.Rect(self.hitbox.left, self.hitbox.bottom - 1, 46, 1)
        self.bottom_side = pygame.Rect(self.hitbox.left, self.hitbox.bottom, 46, 1)



    def create_animation(self,sprite_sheet_image,animation_steps):
        self.sprite_sheet_image = pygame.image.load(sprite_sheet_image).convert_alpha()
        self.sprite_sheet = spritesheet.SpriteSheet(self.sprite_sheet_image)
        self.frame_list = []
        for x in range(animation_steps):
            self.frame_list.append(self.sprite_sheet.get_image(x, 32, 32, 3, (0,0,0)))
        return self.frame_list


    def detect_input(self,event,All_sprites, Apples):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.currently_pressed_keys.append(event.key)
                self.idle = False
                if event.key in (pygame.K_a, pygame.K_d):
                    self.xkeys_pressed.append(event.key)
                elif event.key in (pygame.K_w, pygame.K_s):
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
            self.clicked_sprite = False
            for sprite in Apples:
                if sprite.Detect_Click(event):
                    All_sprites.remove(sprite)  # Remove the sprite from the group, making it disappear
                    self.clicked_sprite = True
                    break
            if event.button == 1 and self.sword_cooldown == False and self.clicked_sprite == False:
              self.using_sword = True
              self.animation_cooldown = 50
              self.switch_animation()
              self.frame = 0
              self.player_speed = 5
              self.sword_cooldown = True
              self.last_sword_use = self.current_time



    def update(self,walls_group):
        self.current_time = pygame.time.get_ticks()
        self.play_animation()
        self.update_player_position(walls_group)

    def play_animation(self,):
        if self.current_time - self.last_frame_update >= self.animation_cooldown:
            self.frame += 1
            self.last_frame_update = self.current_time
        if self.frame >= len(self.current_animation):
            self.frame = 0
            self.using_sword = False
            self.animation_cooldown = 200
            self.player_speed = 1.5
            self.switch_animation()
        if self.idle and self.using_sword == False:
            self.frame = 0
        if self.current_time - self.last_sword_use >= self.sword_cooldown_time:
            self.sword_cooldown = False
        self.image = self.current_animation[self.frame]
        #pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.next_hitbox_x, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.next_hitbox, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.left_side, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.right_side, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.top_side, 1)
#        pygame.draw.rect(self.screen, (255, 0, 0), self.bottom_side, 1)

    def update_player_position(self,walls_group):
        if self.current_time - self.last_position_update >= 10:

            self.next_x = self.player_x + self.player_x_direction * self.player_speed * self.vector_correction
            self.next_y = self.player_y + self.player_y_direction * self.player_speed * self.vector_correction

            # Create a full-sized hitbox for screen edge detection
            next_full_hitbox = self.hitbox.move(self.next_x - self.hitbox.x + self.padding_x, self.next_y - self.hitbox.y + self.padding_y)

            # Create thin hitboxes for precise wall collision on each side
            self.next_hitbox = self.hitbox.move(2, self.next_y - self.hitbox.y + self.padding_y + self.hitbox.height)
            self.next_hitbox.height = 4
            self.next_hitbox.width = 46

            # Define smaller side rects based on player dimensions
            self.left_side = pygame.Rect(self.next_hitbox.left - 1, self.next_hitbox.top, 1, self.next_hitbox.height-1)
            self.right_side = pygame.Rect(self.next_hitbox.right, self.next_hitbox.top, 1, self.next_hitbox.height-1)
            self.top_side = pygame.Rect(self.next_hitbox.left + 1, self.next_hitbox.top - 1, self.next_hitbox.width-2, 1)
            self.bottom_side = pygame.Rect(self.next_hitbox.left + 1, self.next_hitbox.bottom, self.next_hitbox.width-2, 1)

            # Check collisions with walls
            self.is_touching_left = self.left_side.collidelist(walls_group) != -1
            self.is_touching_right = self.right_side.collidelist(walls_group) != -1
            self.is_touching_top = self.top_side.collidelist(walls_group) != -1
            self.is_touching_bottom = self.bottom_side.collidelist(walls_group) != -1

            # Screen boundaries for original hitbox size
            screen_left = 0
            screen_right = self.screenwidth
            screen_top = 0
            screen_bottom = self.screenheight

            # Check horizontal movement
            if screen_left <= next_full_hitbox.left and next_full_hitbox.right <= screen_right:
                if self.player_x_direction > 0 and not self.is_touching_right:
                    # Moving right and not colliding with right wall or screen edge
                    self.player_x = self.next_x
                elif self.player_x_direction < 0 and not self.is_touching_left:
                    # Moving left and not colliding with left wall or screen edge
                    self.player_x = self.next_x

            # Check vertical movement
            if screen_top <= next_full_hitbox.top and next_full_hitbox.bottom <= screen_bottom:
                if self.player_y_direction > 0 and not self.is_touching_bottom:
                    # Moving down and not colliding with bottom wall or screen edge
                    self.player_y = self.next_y
                elif self.player_y_direction < 0 and not self.is_touching_top:
                    # Moving up and not colliding with top wall or screen edge
                    self.player_y = self.next_y

            # Update the player's rect and hitbox positions
            self.rect.x, self.rect.y = self.player_x, self.player_y
            self.hitbox.x = self.rect.x + self.padding_x
            self.hitbox.y = self.rect.y + self.padding_y
            self.last_position_update = self.current_time

    def switch_animation(self,Index=1):
        if self.using_sword:
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

        self.vector_correction = 1
        if self.player_x_direction + self.player_y_direction in (-2, 0, 2):
            self.vector_correction = 0.7071

