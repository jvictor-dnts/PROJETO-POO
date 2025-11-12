import pygame
import os
from utils.config import *

class Jogador:
    def __init__(self):
        self.resetar_posicao()
        self.velocidade = VELOCIDADE_JOGADOR
        self.direcao = [0, 0]
        self.proxima_direcao = [0, 0]
        self.pontos = 0
        self.vidas = 3
        self.cor_fallback = AMARELO
        self.animacoes = self.carregar_animacoes()
        self.frame_atual = 0
        self.contador_animacao = 0
        self.estado = "baixo"
        self.rect = pygame.Rect(self.x - LARGURA_SPRITE // 2, self.y - ALTURA_SPRITE // 2, LARGURA_SPRITE, ALTURA_SPRITE)
    
    def carregar_animacoes(self):
        animacoes = {
            "cima": [],
            "baixo": [],
            "esquerda": [],
            "direita": []
        }
        pasta_sprites = os.path.join(os.path.dirname(__file__), "sprites")
        if not os.path.exists(pasta_sprites):
            return None
        try:
            mapeamento = {
                "cima": "andar_cima.png",
                "baixo": "andar_baixo.png",
                "esquerda": "andar_esquerda.png",
                "direita": "andar_direita.png"
            }
            for direcao, arquivo in mapeamento.items():
                caminho_sprite = os.path.join(pasta_sprites, arquivo)
                if os.path.exists(caminho_sprite):
                    try:
                        sprite_sheet = pygame.image.load(caminho_sprite).convert_alpha()
                        largura_sheet = sprite_sheet.get_width()
                        altura_sheet = sprite_sheet.get_height()
                        num_frames = largura_sheet // LARGURA_SPRITE
                        for i in range(num_frames):
                            x = i * LARGURA_SPRITE
                            frame = sprite_sheet.subsurface(
                                pygame.Rect(x, 0, LARGURA_SPRITE, altura_sheet)
                            )
                            frame = frame.copy()
                            frame = pygame.transform.scale(frame, (LARGURA_SPRITE, ALTURA_SPRITE))
                            animacoes[direcao].append(frame)
                    except Exception as e:
                        pass
                else:
                    pass
            sucesso = all(len(frames) > 0 for frames in animacoes.values())
            if sucesso:
                return animacoes
            else:
                return None
        except Exception as e:
            return None
    
    def resetar_posicao(self):
        self.x = 14 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = 23 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.direcao = [0, 0]
        self.proxima_direcao = [0, 0]
        self.estado = "baixo"
    
    def atualizar(self, labirinto):
        self.tentar_mudar_direcao(labirinto)
        if any(self.direcao):
            novo_x = self.x + self.direcao[0] * self.velocidade
            novo_y = self.y + self.direcao[1] * self.velocidade
            if self.pode_se_mover(novo_x, novo_y, labirinto):
                self.x = novo_x
                self.y = novo_y
            else:
                self.resetar_posicao()
        if self.x < 0:
            self.x = 0
            self.resetar_posicao()
        elif self.x > labirinto.largura * TAMANHO_CELULA:
            self.x = labirinto.largura * TAMANHO_CELULA
            self.resetar_posicao()
        if self.y < 0:
            self.y = 0
            self.resetar_posicao()
        elif self.y > labirinto.altura * TAMANHO_CELULA:
            self.y = labirinto.altura * TAMANHO_CELULA
            self.resetar_posicao()
        if any(self.direcao):
            self.contador_animacao += 1
            if self.contador_animacao >= VELOCIDADE_ANIMACAO:
                self.contador_animacao = 0
                if self.animacoes and self.estado in self.animacoes:
                    self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado])
        else:
            self.frame_atual = 0
        if self.direcao[1] > 0:
            self.estado = "baixo"
        elif self.direcao[1] < 0:
            self.estado = "cima"
        elif self.direcao[0] > 0:
            self.estado = "direita"
        elif self.direcao[0] < 0:
            self.estado = "esquerda"
        self.rect.center = (self.x, self.y)
    
    def pode_se_mover(self, novo_x, novo_y, labirinto):
        raio = TAMANHO_JOGADOR // 2 - 3
        pontos_verificacao = [
            (novo_x, novo_y),
            (novo_x - raio, novo_y),
            (novo_x + raio, novo_y),
            (novo_x, novo_y - raio),
            (novo_x, novo_y + raio),
            (novo_x - raio, novo_y - raio),
            (novo_x + raio, novo_y - raio),
            (novo_x - raio, novo_y + raio),
            (novo_x + raio, novo_y + raio),
        ]
        for px, py in pontos_verificacao:
            celula_x = int(px // TAMANHO_CELULA)
            celula_y = int(py // TAMANHO_CELULA)
            if labirinto.eh_parede(celula_x, celula_y):
                return False
        return True
    
    def tentar_mudar_direcao(self, labirinto):
        if self.proxima_direcao != [0, 0]:
            if self.proxima_direcao != self.direcao:
                teste_x = self.x + self.proxima_direcao[0] * self.velocidade
                teste_y = self.y + self.proxima_direcao[1] * self.velocidade
                if self.pode_se_mover(teste_x, teste_y, labirinto):
                    self.direcao = self.proxima_direcao.copy()
                    self.proxima_direcao = [0, 0]
    
    def desenhar(self, tela):
        try:
            if self.animacoes and self.estado in self.animacoes:
                if len(self.animacoes[self.estado]) > 0:
                    frame = self.animacoes[self.estado][self.frame_atual]
                    pos_x = int(self.x - LARGURA_SPRITE // 2)
                    pos_y = int(self.y - ALTURA_SPRITE // 2)
                    tela.blit(frame, (pos_x, pos_y))
                else:
                    self.desenhar_fallback(tela)
            else:
                self.desenhar_fallback(tela)
        except Exception as e:
            self.desenhar_fallback(tela)
    
    def desenhar_fallback(self, tela):
        pygame.draw.circle(tela, self.cor_fallback, (int(self.x), int(self.y)), TAMANHO_JOGADOR // 2)
        olho_x, olho_y = 0, 0
        if self.direcao[0] > 0:
            olho_x = 5
        elif self.direcao[0] < 0:
            olho_x = -5
        elif self.direcao[1] > 0:
            olho_y = 5
        elif self.direcao[1] < 0:
            olho_y = -5
        pygame.draw.circle(tela, PRETO, (int(self.x + olho_x), int(self.y + olho_y)), TAMANHO_JOGADOR // 4)
