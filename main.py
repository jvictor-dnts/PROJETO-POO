import pygame
from ui.menu import Menu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    menu = Menu(screen)
    menu.run()

    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()

