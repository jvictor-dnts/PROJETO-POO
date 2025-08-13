from menu import Menu
from game import Game
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    menu = Menu(screen)
    menu.run()  # Fica no menu até o jogador iniciar
    game = Game(screen)
    game.run()  # Começa o jogo

if __name__ == "__main__":
    main()
