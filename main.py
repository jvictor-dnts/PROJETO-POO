import pygame
from ui.menu import Menu
from game import Jogo
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DataMaze Escape")
    try:
        icon = pygame.image.load("F.png")
        pygame.display.set_icon(icon)
    except pygame.error:
        print("Não foi possível carregar o ícone.")
    try:
        pygame.mixer.music.load("musica_hacker.mp3")
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Não foi possível carregar o arquivo de música.")
    menu = Menu(tela)
    menu.run()
    pygame.mixer.music.stop()
    jogo = Jogo(tela)
    jogo.rodar()

if __name__ == "__main__":
    main()



