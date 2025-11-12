import pygame
import random
from utils.config import TAMANHO_CELULA, VERMELHO

class Inimigo:
    def __init__(self, x, y):
        self.pos_inicial_x, self.pos_inicial_y = x, y
        self.x = x * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = y * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.raio = TAMANHO_CELULA // 2 - 2
        self.cor = VERMELHO
        self.velocidade = 2
        self.direcao = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.rect = pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)
    def resetar_posicao(self):
        self.x = self.pos_inicial_x * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = self.pos_inicial_y * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.rect.center = (self.x, self.y)
    def atualizar(self, labirinto):
        prox_x = self.x + self.direcao[0] * self.velocidade
        prox_y = self.y + self.direcao[1] * self.velocidade
        celula_x = int(prox_x // TAMANHO_CELULA)
        celula_y = int(prox_y // TAMANHO_CELULA)
        if not labirinto.eh_parede(celula_x, celula_y):
            self.x = prox_x
            self.y = prox_y
        else:
            self.direcao = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.rect.center = (self.x, self.y)
    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
