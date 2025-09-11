import pygame
import sys
from maze import Labirinto
from player import Jogador
from enemies.ia import Inimigo
from utils.config import *

class Jogo:
    def __init__(self, tela):
        self.tela = tela
        pygame.display.set_caption("DataMaze Escape")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont('consolas', 24)
        
        #elementos do jogo
        self.labirinto = Labirinto()
        self.jogador = Jogador()
        self.inimigos = [
            Inimigo(13, 11),
            Inimigo(14, 11)
        ]
        
        #estado do jogo
        self.rodando = True
        self.estado_jogo = 'jogando' # 'jogando', 'vitoria', 'game_over'
        self.tempo_inicio = pygame.time.get_ticks()
        self.ultimo_hit = 0
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            
            if self.estado_jogo == 'jogando':
                #controles do jogador
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
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False

    
    def atualizar(self):
        if self.estado_jogo != 'jogando':
            return
            
        self.jogador.atualizar(self.labirinto)
        for inimigo in self.inimigos:
            inimigo.atualizar(self.labirinto)
        
        #verificar coleta de itens
        celula_x = int(self.jogador.x // TAMANHO_CELULA)
        celula_y = int(self.jogador.y // TAMANHO_CELULA)
        item = self.labirinto.pegar_item(celula_x, celula_y)
        
        if item == 2:  # Ponto
            self.jogador.pontos += PONTOS_POR_PONTO
        elif item == 3:  # Power-up
            self.jogador.pontos += PONTOS_POR_POWERUP
        
        # Verificar colisão com inimigos
        self.verificar_colisoes()

        # Verificar vitória
        if not self.labirinto.tem_itens():
            self.estado_jogo = 'vitoria'

    def verificar_colisoes(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_hit < 2000: # 2 segundos de invencibilidade
            return

        for inimigo in self.inimigos:
            if self.jogador.rect.colliderect(inimigo.rect):
                self.jogador.vidas -= 1
                self.ultimo_hit = agora
                if self.jogador.vidas <= 0:
                    self.estado_jogo = 'game_over'
                else:
                    self.jogador.resetar_posicao()
                    for i in self.inimigos:
                        i.resetar_posicao()
                break # Sai do loop para não perder mais de uma vida por frame
    
    def desenhar(self):
        self.tela.fill(PRETO)
        
        if self.estado_jogo == 'jogando':
            #desenhar labirinto
            self.labirinto.desenhar(self.tela)

            #desenhar jogador
            self.jogador.desenhar(self.tela)

            #desenhar inimigos
            for inimigo in self.inimigos:
                inimigo.desenhar(self.tela)

            #desenhar HUD
            self.desenhar_hud()
        elif self.estado_jogo == 'vitoria':
            self.desenhar_tela_final("Você Venceu!", f"Pontuação final: {self.jogador.pontos}")
        elif self.estado_jogo == 'game_over':
            self.desenhar_tela_final("Game Over", "Você foi capturado!")

        pygame.display.flip()
    
    def desenhar_tela_final(self, titulo, mensagem):
        fonte_titulo = pygame.font.SysFont('consolas', 50)
        fonte_msg = pygame.font.SysFont('consolas', 30)

        texto_titulo = fonte_titulo.render(titulo, True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))

        texto_msg = fonte_msg.render(mensagem, True, BRANCO)
        rect_msg = texto_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))

        self.tela.blit(texto_titulo, rect_titulo)
        self.tela.blit(texto_msg, rect_msg)

    def desenhar_hud(self):
        """desenha a interface do usuário"""
        #pontuação
        texto_pontos = self.fonte.render(f"Pontos: {self.jogador.pontos}", True, BRANCO)
        self.tela.blit(texto_pontos, (20, 20))
        
        #vidas
        texto_vidas = self.fonte.render(f"Vidas: {self.jogador.vidas}", True, BRANCO)
        self.tela.blit(texto_vidas, (20, 50))
        
        #tempo
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