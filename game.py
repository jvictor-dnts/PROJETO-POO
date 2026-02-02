import pygame
import sys
import os
from maze import Labirinto
from player import Jogador
from enemies.ia import Inimigo
from utils.config import *

class Jogo:
    def __init__(self, tela):
        self.tela = tela
        self.tela_width = tela.get_width()
        self.tela_height = tela.get_height()
        
        escala_x = self.tela_width / SCREEN_WIDTH
        escala_y = self.tela_height / SCREEN_HEIGHT
        self.scale = min(escala_x, escala_y)
        
        self.hud_height_escalado = int(HUD_ALTURA * self.scale)
        self.game_height_escalado = int(GAME_HEIGHT * self.scale)
        self.labirinto_width_escalado = int(SCREEN_WIDTH * self.scale)
        
        self.offset_x = (self.tela_width - self.labirinto_width_escalado) // 2
        self.offset_y = self.hud_height_escalado
        
        pygame.display.set_caption("DataMaze Escape")
        self.relogio = pygame.time.Clock()
        self.fonte_hud = pygame.font.SysFont('consolas', max(16, int(22 * self.scale)), bold=True)
        self.fonte_objetivo = pygame.font.SysFont('consolas', max(12, int(14 * self.scale)))
        self.fonte_botao = pygame.font.SysFont('consolas', max(20, int(28 * self.scale)), bold=True)
        self.botao_fechar = self.fonte_botao.render("✕", True, VERMELHO)
        self.rect_botao = self.botao_fechar.get_rect(topright=(self.tela_width - 15, 15))
        
        self.fase = 1
        self.labirinto = Labirinto(self.fase)
        self.jogador = Jogador()
        self.inimigos = self._criar_inimigos()
        self.rodando = True
        self.estado_jogo = 'jogando'
        self.tempo_inicio = pygame.time.get_ticks()
        self.ultimo_hit = 0
        self.musica_tocando = False
        self.saida_desbloqueada = False
        self.iniciar_musica()
    
    def _criar_inimigos(self):
        if self.fase == 1:
            return [
                Inimigo(2, 8),
                Inimigo(35, 8),
                Inimigo(20, 15)
            ]
        elif self.fase == 2:
            return [
                Inimigo(2, 8),
                Inimigo(35, 8),
                Inimigo(20, 15),
                Inimigo(5, 15),
                Inimigo(38, 5)
            ]
        elif self.fase == 3:
            return [
                Inimigo(2, 5),
                Inimigo(35, 5),
                Inimigo(2, 15),
                Inimigo(35, 15),
                Inimigo(20, 10),
                Inimigo(10, 8),
                Inimigo(30, 12)
            ]
        return []
    
    def iniciar_musica(self):
        try:
            caminho_musica = os.path.join(os.path.dirname(__file__), "game_music.mp3")
            if os.path.exists(caminho_musica):
                pygame.mixer.music.load(caminho_musica)
                pygame.mixer.music.play(-1)
                self.musica_tocando = True
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.rect_botao.collidepoint(mouse_pos):
                    self.rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False
        
        # Suporte a movimento contínuo com teclas pressionadas
        if self.estado_jogo == 'jogando':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.jogador.proxima_direcao = [0, -1]
            elif keys[pygame.K_DOWN]:
                self.jogador.proxima_direcao = [0, 1]
            elif keys[pygame.K_LEFT]:
                self.jogador.proxima_direcao = [-1, 0]
            elif keys[pygame.K_RIGHT]:
                self.jogador.proxima_direcao = [1, 0]
            else:
                self.jogador.proxima_direcao = self.jogador.direcao.copy()
    def atualizar(self):
        if self.estado_jogo != 'jogando':
            return
        self.jogador.atualizar(self.labirinto)
        for inimigo in self.inimigos:
            inimigo.atualizar(self.labirinto, self.jogador)
        
        celula_x = int(self.jogador.x // TAMANHO_CELULA)
        celula_y = int(self.jogador.y // TAMANHO_CELULA)
        
        if self.fase == 3 and not self.labirinto.tem_itens():
            self.saida_desbloqueada = True
        
        if self.labirinto.saida_pos and (celula_x, celula_y) == self.labirinto.saida_pos:
            if self.fase < 3:
                self.proxima_fase()
            elif self.fase == 3 and self.saida_desbloqueada:
                self.estado_jogo = 'vitoria'
        
        item = self.labirinto.pegar_item(celula_x, celula_y)
        if item == 2:
            self.jogador.pontos += PONTOS_POR_PONTO
        elif item == 3:
            self.jogador.pontos += PONTOS_POR_POWERUP
        elif item == 5:
            self.jogador.ativar_vida_extra()
            self.jogador.pontos += PONTOS_VIDA_EXTRA
        elif item == 6:
            self.jogador.ativar_velocidade_boost()
            self.jogador.pontos += PONTOS_POR_POWERUP
        self.verificar_colisoes()
        if not self.labirinto.tem_itens():
            pass
    def verificar_colisoes(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_hit < 2000:
            return
        for inimigo in self.inimigos:
            dx = self.jogador.x - inimigo.x
            dy = self.jogador.y - inimigo.y
            distancia2 = dx * dx + dy * dy
            raio_jogador = getattr(self.jogador, 'raio', TAMANHO_JOGADOR // 2)
            raio_inimigo = getattr(inimigo, 'raio', TAMANHO_JOGADOR // 2)
            raio_soma = raio_jogador + raio_inimigo
            if distancia2 <= raio_soma * raio_soma:
                self.jogador.vidas -= 1
                self.ultimo_hit = agora
                if self.jogador.vidas <= 0:
                    self.estado_jogo = 'game_over'
                else:
                    self.jogador.resetar_posicao()
                    for i in self.inimigos:
                        i.resetar_posicao()
                break
    
    def proxima_fase(self):
        self.fase += 1
        self.saida_desbloqueada = False
        self.labirinto = Labirinto(self.fase)
        self.jogador.resetar_posicao()
        self.inimigos = self._criar_inimigos()
        for inimigo in self.inimigos:
            inimigo.resetar_posicao()
    def desenhar(self):
        self.tela.fill(PRETO)
        if self.estado_jogo == 'jogando':
            self.labirinto.desenhar(self.tela, scale=self.scale, offset=(self.offset_x, self.offset_y))
            self.jogador.desenhar(self.tela, scale=self.scale, offset=(self.offset_x, self.offset_y))
            for inimigo in self.inimigos:
                inimigo.desenhar(self.tela, scale=self.scale, offset=(self.offset_x, self.offset_y))
            self.desenhar_hud()
            self.tela.blit(self.botao_fechar, self.rect_botao)
        elif self.estado_jogo == 'vitoria':
            self.desenhar_tela_final("Você Venceu!", f"Pontuação final: {self.jogador.pontos}")
        elif self.estado_jogo == 'game_over':
            self.desenhar_tela_final("Game Over", "Você foi capturado!")
        pygame.display.flip()
    def desenhar_tela_final(self, titulo, mensagem):
        fonte_titulo = pygame.font.SysFont('consolas', 40)
        fonte_msg = pygame.font.SysFont('consolas', 24)
        texto_titulo = fonte_titulo.render(titulo, True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(self.tela_width/2, self.tela_height/2 - 50))
        texto_msg = fonte_msg.render(mensagem, True, BRANCO)
        rect_msg = texto_msg.get_rect(center=(self.tela_width/2, self.tela_height/2 + 20))
        self.tela.blit(texto_titulo, rect_titulo)
        self.tela.blit(texto_msg, rect_msg)
    def desenhar_hud(self):
        pygame.draw.rect(self.tela, (0, 0, 0), pygame.Rect(0, 0, self.tela_width, self.hud_height_escalado))
        pygame.draw.line(self.tela, AZUL_NEON, (0, self.hud_height_escalado - 2), 
                        (self.tela_width, self.hud_height_escalado - 2), 3)
        
        pad_h = int(15 * self.scale)
        pad_v = int(8 * self.scale)
        
        texto_pontos = self.fonte_hud.render(f"Pontos: {self.jogador.pontos}", True, VERDE)
        self.tela.blit(texto_pontos, (pad_h, pad_v))
        
        texto_vidas = self.fonte_hud.render(f"Vidas: {self.jogador.vidas}", True, VERMELHO)
        rect_vidas = texto_vidas.get_rect(centerx=self.tela_width // 2, top=pad_v)
        self.tela.blit(texto_vidas, rect_vidas)
        
        texto_fase = self.fonte_hud.render(f"Fase: {self.fase}", True, CIANO)
        rect_fase = texto_fase.get_rect(topright=(self.tela_width - pad_h, pad_v))
        self.tela.blit(texto_fase, rect_fase)
        
        tempo_decorrido = (pygame.time.get_ticks() - self.tempo_inicio) // 1000
        texto_tempo = self.fonte_hud.render(f"Tempo: {tempo_decorrido}s", True, AMARELO)
        rect_tempo = texto_tempo.get_rect(right=rect_fase.left - 20, top=pad_v)
        self.tela.blit(texto_tempo, rect_tempo)
        
        pad_v_2 = int(45 * self.scale)
        texto_objetivo = self.fonte_objetivo.render("Objetivo: Alcance o portal VERDE na saída →", True, BRANCO)
        rect_obj = texto_objetivo.get_rect(centerx=self.tela_width // 2, top=pad_v_2)
        self.tela.blit(texto_objetivo, rect_obj)
    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        pygame.quit()
        sys.exit()