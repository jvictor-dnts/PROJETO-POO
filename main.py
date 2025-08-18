import pygame
from ui.menu import Menu
from game import Jogo

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    
    menu = Menu(tela)
    menu.run()
    
    jogo = Jogo(tela)
    jogo.rodar()

if __name__ == "__main__":
    main()

