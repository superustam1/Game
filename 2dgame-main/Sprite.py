import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Knight_10_Walk_Down.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 200
frame = 0


for x in range(animation_steps):
	animation_list.append(sprite_sheet.get_image(x, 32, 32, 3, BLACK))


run = True
while run:

	#update background
	screen.fill(BG)

	#show frame image

	current_time = pygame.time.get_ticks()
	if current_time - last_update >= animation_cooldown:
		frame += 1
		last_update = current_time
		if frame >= len(animation_list):
			frame = 0

	screen.blit(animation_list[frame], (0, 0))

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()