import pygame
from ui.menu import Menu
from player import Player

# Configurações
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Game:
    def __init__(self, screen=None):

        self.screen = screen or pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DataMaze Escape")
        self.clock = pygame.time.Clock()
        self.player = Player()

    def run(self):
        if not isinstance(self, Menu):
            menu = Menu(self.screen)
            menu.run()

        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            teclas = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Atualiza jogador
            self.player.update(teclas)

            # Desenha cena
            self.screen.fill((30, 30, 30))
            self.player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
