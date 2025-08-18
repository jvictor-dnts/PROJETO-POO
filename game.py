import pygame
import sys
from maze import Labirinto
from player import Jogador
from utils.config import *

class Jogo:
    def __init__(self, tela):
        self.tela = tela
        pygame.display.set_caption("DataMaze Escape")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont('consolas', 24)
        
        # Elementos do jogo
        self.labirinto = Labirinto()
        self.jogador = Jogador()
        
        # Estado do jogo
        self.rodando = True
        self.jogo_ativo = True
        self.tempo_inicio = pygame.time.get_ticks()
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            
            # Controles do jogador
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.jogador.proxima_direcao = [0, -1]
                elif evento.key == pygame.K_DOWN:
                    self.jogador.proxima_direcao = [0, 1]
                elif evento.key == pygame.K_LEFT:
                    self.jogador.proxima_direcao = [-1, 0]
                elif evento.key == pygame.K_RIGHT:
                    self.jogador.proxima_direcao = [1, 0]
                elif evento.key == pygame.K_ESCAPE:
                    self.rodando = False
    
    def atualizar(self):
        if not self.jogo_ativo:
            return
            
        self.jogador.atualizar(self.labirinto)
        
        # Verificar coleta de itens
        celula_x = int(self.jogador.x // TAMANHO_CELULA)
        celula_y = int(self.jogador.y // TAMANHO_CELULA)
        item = self.labirinto.pegar_item(celula_x, celula_y)
        
        if item == 2:  # Ponto
            self.jogador.pontos += PONTOS_POR_PONTO
        elif item == 3:  # Power-up
            self.jogador.pontos += PONTOS_POR_POWERUP
        
        # Verificar vitória
        if not self.labirinto.tem_itens():
            self.jogo_ativo = False
            print("Você venceu! Pontuação:", self.jogador.pontos)
    
    def desenhar(self):
        self.tela.fill(PRETO)
        
        # Desenhar labirinto
        self.labirinto.desenhar(self.tela)
        
        # Desenhar jogador
        self.jogador.desenhar(self.tela)
        
        # Desenhar HUD
        self.desenhar_hud()
        
        pygame.display.flip()
    
    def desenhar_hud(self):
        """Desenha a interface do usuário"""
        # Pontuação
        texto_pontos = self.fonte.render(f"Pontos: {self.jogador.pontos}", True, BRANCO)
        self.tela.blit(texto_pontos, (20, 20))
        
        # Vidas
        texto_vidas = self.fonte.render(f"Vidas: {self.jogador.vidas}", True, BRANCO)
        self.tela.blit(texto_vidas, (20, 50))
        
        # Tempo
        tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicio) // 1000
        texto_tempo = self.fonte.render(f"Tempo: {tempo_decorrido}s", True, BRANCO)
        self.tela.blit(texto_tempo, (20, 80))
    
    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        
        pygame.quit()
        sys.exit()