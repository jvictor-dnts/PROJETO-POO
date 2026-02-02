import pygame
import random
import os
from utils.config import TAMANHO_CELULA, VERMELHO, TAMANHO_JOGADOR

class Inimigo:
    def __init__(self, x, y):
        self.pos_inicial_x, self.pos_inicial_y = x, y
        self.x = x * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = y * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.raio = int(TAMANHO_JOGADOR * 1.5) // 2
        self.cor = VERMELHO
        self.velocidade = 1.5
        self.direcao = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
        self.rect = pygame.Rect(self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2)
        self.imagem = None
        try:
            caminho_policial = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "sprites", "policial.png"))
            if os.path.exists(caminho_policial):
                img = pygame.image.load(caminho_policial).convert_alpha()
                tamanho = (int(self.raio * 2), int(self.raio * 2))
                img = pygame.transform.scale(img, tamanho)
                self.imagem = img
        except Exception:
            self.imagem = None
    def resetar_posicao(self):
        self.x = self.pos_inicial_x * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = self.pos_inicial_y * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.rect.center = (self.x, self.y)
    def atualizar(self, labirinto, jogador=None):
        if jogador:
            dx = jogador.x - self.x
            dy = jogador.y - self.y
            distancia = (dx*dx + dy*dy) ** 0.5
            
            if distancia < 200:
                novo_direcao = [0, 0]
                
                if abs(dx) > abs(dy):
                    novo_direcao[0] = 1 if dx > 0 else -1
                else:
                    novo_direcao[1] = 1 if dy > 0 else -1
                
                prox_x = self.x + novo_direcao[0] * self.velocidade
                prox_y = self.y + novo_direcao[1] * self.velocidade
                celula_x = int(prox_x // TAMANHO_CELULA)
                celula_y = int(prox_y // TAMANHO_CELULA)
                
                if not labirinto.eh_parede(celula_x, celula_y):
                    self.x = prox_x
                    self.y = prox_y
                    self.direcao = novo_direcao
                else:
                    novo_direcao_alt = [novo_direcao[1], novo_direcao[0]]
                    prox_x_alt = self.x + novo_direcao_alt[0] * self.velocidade
                    prox_y_alt = self.y + novo_direcao_alt[1] * self.velocidade
                    celula_x_alt = int(prox_x_alt // TAMANHO_CELULA)
                    celula_y_alt = int(prox_y_alt // TAMANHO_CELULA)
                    
                    if not labirinto.eh_parede(celula_x_alt, celula_y_alt):
                        self.x = prox_x_alt
                        self.y = prox_y_alt
                        self.direcao = novo_direcao_alt
            else:
                self._movimento_aleatorio(labirinto)
        else:
            self._movimento_aleatorio(labirinto)
        
        self.rect.center = (self.x, self.y)
    
    def _movimento_aleatorio(self, labirinto):
        prox_x = self.x + self.direcao[0] * self.velocidade
        prox_y = self.y + self.direcao[1] * self.velocidade
        celula_x = int(prox_x // TAMANHO_CELULA)
        celula_y = int(prox_y // TAMANHO_CELULA)
        
        if not labirinto.eh_parede(celula_x, celula_y):
            self.x = prox_x
            self.y = prox_y
        else:
            self.direcao = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])
    def desenhar(self, tela, scale=1.0, offset=(0,0)):
        ox, oy = offset
        if self.imagem:
            ow, oh = self.imagem.get_width(), self.imagem.get_height()
            nw = max(1, int(ow * scale))
            nh = max(1, int(oh * scale))
            img_scaled = pygame.transform.scale(self.imagem, (nw, nh))
            pos_x = ox + int(self.x * scale - nw / 2)
            pos_y = oy + int(self.y * scale - nh / 2)
            tela.blit(img_scaled, (pos_x, pos_y))
        else:
            raio = max(1, int(self.raio * scale))
            centro = (ox + int(self.x * scale), oy + int(self.y * scale))
            pygame.draw.circle(tela, self.cor, centro, raio)
