#основной для запуска
import pygame 
import sys
from menu import show_menu
from player import Player
from map import Map
from npcs import Monster

#Инициализация pygame
pygame.init()

#настройки окна
screen_wigth = 800
screen_height = 600
screen = pygame.display.set_mode((screen_wigth, screen_height))
pygame.display.set_caption('Dangeon Shooter-Platformer-Visual Novel')

#Создание обьектов
player = Player(50,50)
map = Map('png')
monster = Monster(300,200)

#основной цикл игры
def game_loop():
    running =True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()

        screen.fill((0,0,0))
        map.draw(screen)
        player.draw(screen)
        monster.draw(screen)
        pygame.displey.flip()

if __name__ == '__main__':
    show_menu(screen)
    game_loop()






