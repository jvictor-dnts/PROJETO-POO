import pygame
import numpy as np
from utils.config import *

class Labirinto:
    def __init__(self):
        self.largura = 28
        self.altura = 31
        self.grade = self.criar_labirinto()
        
    def criar_labirinto(self):
        labirinto = [
            "############################",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#o#  #.#   #.##.#   #.#  #o#",
            "#.####.#####.##.#####.####.#",
            "#..........................#",
            "#.####.##.########.##.####.#",
            "#.####.##.########.##.####.#",
            "#......##....##....##......#",
            "######.##### ## #####.######",
            "     #.##### ## #####.#     ",
            "     #.##          ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "######.## ######## ##.######",
            "     #.## ######## ##.#     ",
            "     #.##          ##.#     ",
            "     #.## ######## ##.#     ",
            "######.## ######## ##.######",
            "#............##............#",
            "#.####.#####.##.#####.####.#",
            "#.####.#####.##.#####.####.#",
            "#o..##................##..o#",
            "###.##.##.########.##.##.###",
            "###.##.##.########.##.##.###",
            "#......##....##....##......#",
            "#.##########.##.##########.#",
            "#.##########.##.##########.#",
            "#..........................#",
            "############################"
        ]
        
        grade = np.zeros((self.altura, self.largura), dtype=int)
        for y in range(self.altura):
            for x in range(self.largura):
                char = labirinto[y][x]
                if char == '#':
                    grade[y][x] = 1  # Parede
                elif char == '.':
                    grade[y][x] = 2  # Ponto
                elif char == 'o':
                    grade[y][x] = 3  # Power-up
        return grade
    
    def desenhar(self, tela):
        for y in range(self.altura):
            for x in range(self.largura):
                rect = pygame.Rect(x * TAMANHO_CELULA, y * TAMANHO_CELULA, 
                                 TAMANHO_CELULA, TAMANHO_CELULA)
                
                if self.grade[y][x] == 1:
                    pygame.draw.rect(tela, AZUL_ESCURO, rect)
                    pygame.draw.rect(tela, AZUL_NEON, rect, 1)
                elif self.grade[y][x] == 2:
                    centro = (x * TAMANHO_CELULA + TAMANHO_CELULA//2, 
                             y * TAMANHO_CELULA + TAMANHO_CELULA//2)
                    pygame.draw.circle(tela, BRANCO, centro, TAMANHO_PONTO)
                elif self.grade[y][x] == 3:
                    centro = (x * TAMANHO_CELULA + TAMANHO_CELULA//2, 
                             y * TAMANHO_CELULA + TAMANHO_CELULA//2)
                    pygame.draw.circle(tela, AMARELO, centro, TAMANHO_POWERUP)
    
    def eh_parede(self, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            return self.grade[y][x] == 1
        return True
    
    def pegar_item(self, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            item = self.grade[y][x]
            if item in [2, 3]:
                self.grade[y][x] = 0
                return item
        return None
    
    def tem_itens(self):
        return any(item in [2, 3] for linha in self.grade for item in linha)