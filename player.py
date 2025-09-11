import pygame
from utils.config import *

class Jogador:
    def __init__(self):
        self.resetar_posicao()
        self.velocidade = VELOCIDADE_JOGADOR
        self.direcao = [0, 0]
        self.proxima_direcao = [0, 0]
        self.pontos = 0
        self.vidas = 3
        
        # Carrega a sprite sheet
        try:
            self.sprite_sheet = pygame.image.load("spriteplayer.png").convert_alpha()
        except:
            # Fallback caso o sprite não carregue
            self.sprite_sheet = None
            self.cor_fallback = AMARELO
        
        # Configurações de animação
        self.animacoes = self.carregar_animacoes() if self.sprite_sheet else None
        self.frame_atual = 0
        self.contador_animacao = 0
        self.estado = "baixo"
        self.rect = pygame.Rect(self.x - LARGURA_SPRITE // 2, self.y - ALTURA_SPRITE // 2, LARGURA_SPRITE, ALTURA_SPRITE)
    
    def carregar_animacoes(self):
        """Divide a sprite sheet em animações"""
        animacoes = {
            "baixo": [],
            "esquerda": [],
            "direita": [],
            "cima": []
        }
        
        for linha in range(4):
            for coluna in range(4):
                frame = pygame.Surface((LARGURA_SPRITE, ALTURA_SPRITE), pygame.SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), 
                          (coluna * LARGURA_SPRITE, linha * ALTURA_SPRITE, 
                           LARGURA_SPRITE, ALTURA_SPRITE))
                
                if linha == 0: animacoes["baixo"].append(frame)
                elif linha == 1: animacoes["esquerda"].append(frame)
                elif linha == 2: animacoes["direita"].append(frame)
                elif linha == 3: animacoes["cima"].append(frame)
        
        return animacoes
    
    def resetar_posicao(self):
        """Reseta o jogador para a posição inicial"""
        self.x = 14 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = 23 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.direcao = [0, 0]
        self.proxima_direcao = [0, 0]
        self.estado = "baixo"
    
    def atualizar(self, labirinto):
        """Atualiza a posição e animação do jogador"""
        self.tentar_mudar_direcao(labirinto)
        
        # Movimento
        novo_x = self.x + self.direcao[0] * self.velocidade
        novo_y = self.y + self.direcao[1] * self.velocidade
        
        # Colisão com paredes
        celula_x = int(novo_x // TAMANHO_CELULA)
        celula_y = int(novo_y // TAMANHO_CELULA)
        
        if not labirinto.eh_parede(celula_x, celula_y):
            self.x = novo_x
            self.y = novo_y
        else:
            # Alinhamento com a grade
            if self.direcao[0] != 0:
                self.y = (self.y // TAMANHO_CELULA) * TAMANHO_CELULA + TAMANHO_CELULA // 2
            else:
                self.x = (self.x // TAMANHO_CELULA) * TAMANHO_CELULA + TAMANHO_CELULA // 2
        
        # Túneis
        if self.x < 0:
            self.x = labirinto.largura * TAMANHO_CELULA
        elif self.x > labirinto.largura * TAMANHO_CELULA:
            self.x = 0
        
        # Atualizar animação
        if any(self.direcao):
            self.contador_animacao += 1
            if self.contador_animacao >= VELOCIDADE_ANIMACAO:
                self.contador_animacao = 0
                self.frame_atual = (self.frame_atual + 1) % 4
        
        # Determinar direção para animação
        if self.direcao[1] > 0:
            self.estado = "baixo"
        elif self.direcao[1] < 0:
            self.estado = "cima"
        elif self.direcao[0] > 0:
            self.estado = "direita"
        elif self.direcao[0] < 0:
            self.estado = "esquerda"

        # Atualizar o rect para detecção de colisão
        self.rect.center = (self.x, self.y)
    
    def tentar_mudar_direcao(self, labirinto):
        """Tenta mudar para a próxima direção solicitada"""
        if self.proxima_direcao != [0, 0]:
            celula_x = int(self.x // TAMANHO_CELULA)
            celula_y = int(self.y // TAMANHO_CELULA)
            
            # Verifica alinhamento com a grade
            alinhado_x = abs(self.x - (celula_x * TAMANHO_CELULA + TAMANHO_CELULA // 2)) < 5
            alinhado_y = abs(self.y - (celula_y * TAMANHO_CELULA + TAMANHO_CELULA // 2)) < 5
            
            if alinhado_x and alinhado_y:
                nova_celula_x = celula_x + self.proxima_direcao[0]
                nova_celula_y = celula_y + self.proxima_direcao[1]
                
                if not labirinto.eh_parede(nova_celula_x, nova_celula_y):
                    self.direcao = self.proxima_direcao.copy()
                    self.proxima_direcao = [0, 0]
    
    def desenhar(self, tela):
        """Desenha o jogador com animação"""
        if self.animacoes:
            frame = self.animacoes[self.estado][self.frame_atual]
            tela.blit(frame, (self.x - LARGURA_SPRITE // 2, self.y - ALTURA_SPRITE // 2))
        else:
            # Fallback visual caso o sprite não carregue
            pygame.draw.circle(tela, self.cor_fallback, (int(self.x), int(self.y)), TAMANHO_JOGADOR // 2)
            
            # Olhos indicando direção
            olho_x, olho_y = 0, 0
            if self.direcao[0] > 0: olho_x = 5
            elif self.direcao[0] < 0: olho_x = -5
            elif self.direcao[1] > 0: olho_y = 5
            elif self.direcao[1] < 0: olho_y = -5
            
            pygame.draw.circle(tela, PRETO, (int(self.x + olho_x), int(self.y + olho_y)), TAMANHO_JOGADOR // 4)