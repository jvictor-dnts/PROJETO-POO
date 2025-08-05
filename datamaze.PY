import pygame
import sys

# --------- Configurações ---------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (70, 130, 180)

pygame.init()
pygame.display.set_caption("Menu Inicial - DataMaze Escape")
FONT = pygame.font.Font("JOGO/fonte/fontehacker.ttf", 26)


# >>> ADICIONADO: fonte maior para o título
TITLE_FONT = pygame.font.Font("JOGO/fonte/fontehacker.ttf", 32)


# >>> ADICIONADO: inicializa o mixer para som
pygame.mixer.init()

# >>> ADICIONADO: carrega a música estilo hacker
pygame.mixer.music.load("JOGO/musica_hacker.mp3")  # coloque o arquivo na pasta do projeto
pygame.mixer.music.play(-1)  # -1 = toca em loop infinito


class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.callback = callback
        self.default_color = WHITE
        self.highlight_color = HIGHLIGHT
        self.label = FONT.render(self.text, True, self.default_color)
        self.rect = self.label.get_rect(center=pos)

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            label = FONT.render(self.text, True, self.highlight_color)
        else:
            label = self.label
        surface.blit(label, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()


class Menu:
    def __init__(self, screen):
        self.screen = screen

        # Carrega o background e ajusta o tamanho
        self.background = pygame.image.load("JOGO/F.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        mid_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        gap = 70

        self.buttons = [
            Button("Iniciar Jogo", (mid_x, start_y), self.start_game),
            Button("Opções",       (mid_x, start_y + gap), self.show_options),
            Button("Sair",         (mid_x, start_y + 2 * gap), self.exit_game),
        ]
        self.running = True

        # >>> ADICIONADO: cria o texto do título para exibir na tela
        self.title_surface = TITLE_FONT.render("DataMaze Escape", True, (0, 255, 0))  # Verde neon
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))

    def start_game(self):
        print("Iniciando o jogo...")
        self.running = False
        pygame.mixer.music.stop()  # >>> ADICIONADO: para a música ao iniciar o jogo

    def show_options(self):
        print("Abrindo opções...")

    def exit_game(self):
        pygame.mixer.music.stop()  # >>> ADICIONADO: para a música antes de sair
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            # Exibe o background
            self.screen.blit(self.background, (0, 0))

            # >>> ADICIONADO: desenha o título na tela
            self.screen.blit(self.title_surface, self.title_rect)

            # Desenha os botões
            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self):
        menu = Menu(self.screen)
        menu.run()
        self.game_loop()

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((30, 30, 30))
            # Aqui seria o jogo principal
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
