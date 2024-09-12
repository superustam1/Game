import pygame


Player = pygame.Rect((300,300,50,50))

while True:
    key = pygame.key.get_pressed()
    if key[pygame.K_w] == True:
        Player.move_ip(0, -1)
    if key[pygame.K_s] == True:
        Player.move_ip(0, 1)

    if key[pygame.K_a] == True:
        Player.move_ip(-1, 0)
    if key[pygame.K_d] == True:
        Player.move_ip(1, 0)


