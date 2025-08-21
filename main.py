import pygame
from ui.menu import Menu
from game import Jogo
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    
    menu = Menu(tela)
    menu.run()
    
    jogo = Jogo(tela)
    jogo.rodar()

if __name__ == "__main__":
    main()



