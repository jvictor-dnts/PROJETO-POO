import pygame
import os
from utils.config import *

class Jogador:
    def __init__(self):
        self.resetar_posicao()
        self.velocidade = VELOCIDADE_JOGADOR
        self.raio = TAMANHO_JOGADOR // 2
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
        self.velocidade_boost_ativo = False
        self.tempo_velocidade_boost = 0
    
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
        # Suporte a sprites por direção (jogador_cima.png, jogador_esq.png, etc.)
        mapeamento_direcoes = {
            "cima": "jogador_cima.png",
            "baixo": "jogador_baixo.png",
            "esquerda": "jogador_esq.png",
            "direita": "jogador_dir.png"
        }
        carregou_algum = False
        for direcao, arquivo in mapeamento_direcoes.items():
            caminho = os.path.join(pasta_sprites, arquivo)
            if os.path.exists(caminho):
                try:
                    img = pygame.image.load(caminho).convert_alpha()
                    img = pygame.transform.scale(img, (LARGURA_SPRITE, ALTURA_SPRITE))
                    animacoes[direcao].append(img)
                    carregou_algum = True
                except Exception:
                    pass
        if carregou_algum:
            return animacoes
        # Fallback: tenta jogador.png como sprite genérico
        jogador_path = os.path.join(pasta_sprites, "jogador.png")
        if os.path.exists(jogador_path):
            try:
                img = pygame.image.load(jogador_path).convert_alpha()
                img = pygame.transform.scale(img, (LARGURA_SPRITE, ALTURA_SPRITE))
                for direcao in animacoes.keys():
                    animacoes[direcao].append(img)
                return animacoes
            except Exception:
                pass
        # Caso não exista, tenta carregar sprite-sheets por direção (comportamento antigo)
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
                        num_frames = max(1, largura_sheet // LARGURA_SPRITE)
                        for i in range(num_frames):
                            x = i * LARGURA_SPRITE
                            frame = sprite_sheet.subsurface(
                                pygame.Rect(x, 0, LARGURA_SPRITE, altura_sheet)
                            )
                            frame = frame.copy()
                            frame = pygame.transform.scale(frame, (LARGURA_SPRITE, ALTURA_SPRITE))
                            animacoes[direcao].append(frame)
                    except Exception:
                        pass
            sucesso = all(len(frames) > 0 for frames in animacoes.values())
            if sucesso:
                return animacoes
            else:
                return None
        except Exception:
            return None
    
    def resetar_posicao(self):
        self.x = 5 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.y = 1 * TAMANHO_CELULA + TAMANHO_CELULA // 2
        self.direcao = [0, 0]
        self.proxima_direcao = [0, 0]
        self.estado = "baixo"
        try:
            self.rect.center = (self.x, self.y)
        except Exception:
            pass
    
    def atualizar(self, labirinto):
        if self.velocidade_boost_ativo:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_velocidade_boost > DURACAO_VELOCIDADE_BOOST:
                self.velocidade_boost_ativo = False
                self.velocidade = VELOCIDADE_JOGADOR
        
        self.tentar_mudar_direcao(labirinto)
        if any(self.direcao):
            novo_x = self.x + self.direcao[0] * self.velocidade
            novo_y = self.y + self.direcao[1] * self.velocidade
            if self.pode_se_mover(novo_x, novo_y, labirinto):
                self.x = novo_x
                self.y = novo_y
        
        if self.x < 0:
            self.x = 0
        elif self.x > labirinto.largura * TAMANHO_CELULA:
            self.x = labirinto.largura * TAMANHO_CELULA
        if self.y < 0:
            self.y = 0
        elif self.y > labirinto.altura * TAMANHO_CELULA:
            self.y = labirinto.altura * TAMANHO_CELULA
        
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
        celula_x = int(novo_x // TAMANHO_CELULA)
        celula_y = int(novo_y // TAMANHO_CELULA)
        return not labirinto.eh_parede(celula_x, celula_y)
    
    def tentar_mudar_direcao(self, labirinto):
        if self.proxima_direcao != [0, 0]:
            teste_x = self.x + self.proxima_direcao[0] * self.velocidade
            teste_y = self.y + self.proxima_direcao[1] * self.velocidade
            if self.pode_se_mover(teste_x, teste_y, labirinto):
                self.direcao = self.proxima_direcao.copy()
    
    def ativar_vida_extra(self):
        self.vidas += 1
    
    def ativar_velocidade_boost(self):
        if not self.velocidade_boost_ativo:
            self.velocidade_boost_ativo = True
            self.velocidade = VELOCIDADE_JOGADOR * 2
            self.tempo_velocidade_boost = pygame.time.get_ticks()
    
    def desenhar(self, tela, scale=1.0, offset=(0,0)):
        ox, oy = offset
        try:
            if self.animacoes and self.estado in self.animacoes and len(self.animacoes[self.estado]) > 0:
                frame = self.animacoes[self.estado][self.frame_atual]
                sw = int(LARGURA_SPRITE * scale)
                sh = int(ALTURA_SPRITE * scale)
                frame_scaled = pygame.transform.scale(frame, (sw, sh))
                pos_x = ox + int(self.x * scale - sw // 2)
                pos_y = oy + int(self.y * scale - sh // 2)
                tela.blit(frame_scaled, (pos_x, pos_y))
            else:
                self.desenhar_fallback(tela, scale, offset)
        except Exception:
            self.desenhar_fallback(tela, scale, offset)
    
    def desenhar_fallback(self, tela, scale=1.0, offset=(0,0)):
        ox, oy = offset
        raio = max(3, int((TAMANHO_JOGADOR // 2 + 2) * scale))
        centro = (ox + int(self.x * scale), oy + int(self.y * scale))
        pygame.draw.circle(tela, self.cor_fallback, centro, raio)
        pygame.draw.circle(tela, (255, 255, 100), centro, raio, max(2, int(2 * scale)))
        olho_x, olho_y = 0, 0
        olho_offset = max(1, int(5 * scale))
        if self.direcao[0] > 0:
            olho_x = olho_offset
        elif self.direcao[0] < 0:
            olho_x = -olho_offset
        elif self.direcao[1] > 0:
            olho_y = olho_offset
        elif self.direcao[1] < 0:
            olho_y = -olho_offset
        olho_raio = max(2, int((TAMANHO_JOGADOR // 4 + 1) * scale))
        pygame.draw.circle(tela, PRETO, (centro[0] + olho_x, centro[1] + olho_y), olho_raio)
