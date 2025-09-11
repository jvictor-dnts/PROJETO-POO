import pygame
import sys
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Cores do menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (70, 130, 180)

class Button:
    def __init__(self, text, pos, font, callback):
        self.text = text
        self.callback = callback
        self.font = font
        self.default_color = WHITE
        self.highlight_color = HIGHLIGHT
        self.label = self.font.render(self.text, True, self.default_color)
        self.rect = self.label.get_rect(center=pos)

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            label = self.font.render(self.text, True, self.highlight_color)
        else:
            label = self.label
        surface.blit(label, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

class Menu:
    def __init__(self, tela):
        self.screen = tela
        self.running = True

        # Carregar fontes
        try:
            self.title_font = pygame.font.Font("fontehacker.ttf", 32)
            self.font = pygame.font.Font("fontehacker.ttf", 26)
        except pygame.error:
            self.title_font = pygame.font.SysFont('consolas', 32)
            self.font = pygame.font.SysFont('consolas', 26)

        # Carregar background
        try:
            self.background = pygame.image.load("F.png").convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BLACK)

        # Título
        self.title_surface = self.title_font.render("DataMaze Escape", True, WHITE)
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))

        # Botões
        mid_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        gap = 70

        self.buttons = [
            Button("Iniciar Jogo", (mid_x, start_y), self.font, self.start_game),
            Button("Sair", (mid_x, start_y + gap), self.font, self.exit_game),
        ]

    def start_game(self):
        self.running = False

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title_surface, self.title_rect)

            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)