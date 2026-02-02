import pygame
import numpy as np
from utils.config import *

class Labirinto:
    def __init__(self, fase=1):
        self.largura = MAPA_LARGURA
        self.altura = MAPA_ALTURA
        self.fase = fase
        self.grade = self.criar_labirinto()
    def criar_labirinto(self):
        if self.fase == 1:
            labirinto = [
                "########################################",
                "#......................................#",
                "#.####.#####.#########.####.####.####.#",
                "#.#  #.#   #.#       #.#  #.#  #.#  #.#",
                "#.####.#####.#########.####.####.####.#",
                "#..........................#............#",
                "#.####.##.#####.######.##.#.##.####...#",
                "#.####.##.#####.######.##.#.##.####...#",
                "#......##....##....##....#.#..##.......#",
                "######.##### ## #####.####.##### ......#",
                "#................#......#.#....#.....#",
                "#.##########.#######.##.#.####.#####.#",
                "#.##########.#######.##.#.#....#.....#",
                "#................#......#.#....#....S#",
                "#................#......#............#",
                "#.##########.#######.##.#.####.####.#.#",
                "#.##########.#######.##.#.####.####.#.#",
                "#......##....##....##....#.#..##......#",
                "######.##### ## #####.######### ######",
                "########################################"
            ]
        elif self.fase == 2:
            labirinto = [
                "########################################",
                "#......#........#........#........#...#",
                "#.###.#.#.####.#.#.####.#.#.###.#.#.#.#",
                "#.....#...#....#.#.#....#.#...#.#...#.#",
                "#.###.###.#.##.#.#.#.##.#.#.#.#.###.#.#",
                "#.#...#...#....#.#.....#.....#.#.....#.#",
                "#.#.###.###.##.#.###.###.###.#.#.####.#.#",
                "#...#...#...#....#...#...#.#.#.....#...#",
                "#.#.#.###.###.#.#.#.#.###.#.#.###.#.###.#",
                "#.....#.......#.#.#.........#.....#.....#",
                "#.###.#.###.##.#.#.###.###.#.###.###.#.#",
                "#.#...#...#...#.#.#...#...#...#...#.#.#",
                "#.#.#.###.#.###.#.#.#.#.###.###.#.###.#",
                "#.#.#.......#...#.#.#.......#...#.....S#",
                "#.###.#####.#.###.#.#.#####.#.#####.###.#",
                "#.......................#.......#.....#",
                "#.###.###.###.###.###.##.#.#####.#.###.#",
                "#...#...#.#...#...#.#....#.......#...#.#",
                "#.#.###.#.#.###.#.#.#.#.###.#####.###.#.#",
                "#...................#.................#",
                "########################################"
            ]
        elif self.fase == 3:
            labirinto = [
                "########################################",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#......................................#",
                "#...#...#...#...#...#...#...#...#...#..#",
                "#.....................................S#", # 'S' agora dentro dos 40 caracteres
                "#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.##",
                "#......................................#",
                "#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.##",
                "#......................................#",
                "#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.##",
                "########################################"
            ]
        labirinto = [linha.ljust(40, '#')[:40] for linha in labirinto]
        
        grade = np.zeros((self.altura, self.largura), dtype=int)
        self.saida_pos = None
        for y in range(self.altura):
            for x in range(self.largura):
                if y < len(labirinto) and x < len(labirinto[y]):
                    char = labirinto[y][x]
                    if char == '#':
                        grade[y][x] = 1
                    elif char == '.':
                        grade[y][x] = 2
                    elif char == 'o':
                        grade[y][x] = 3
                    elif char == 'V':
                        grade[y][x] = 5
                    elif char == 'B':
                        grade[y][x] = 6
                    elif char == 'S':
                        grade[y][x] = 4
                        self.saida_pos = (x, y)
        return grade
    def desenhar(self, tela, scale=1.0, offset=(0,0)):
        ox, oy = offset
        for y in range(self.altura):
            for x in range(self.largura):
                px = ox + int(x * TAMANHO_CELULA * scale)
                py = oy + int(y * TAMANHO_CELULA * scale)
                tamanho = int(TAMANHO_CELULA * scale)
                rect = pygame.Rect(px, py, tamanho, tamanho)
                if self.grade[y][x] == 1:
                    pygame.draw.rect(tela, AZUL_ESCURO, rect)
                    pygame.draw.rect(tela, AZUL_NEON, rect, max(1, int(scale)))
                elif self.grade[y][x] == 2:
                    centro = (px + tamanho//2, py + tamanho//2)
                    raio = max(1, int(TAMANHO_PONTO * scale))
                    pygame.draw.circle(tela, BRANCO, centro, raio)
                elif self.grade[y][x] == 3:
                    centro = (px + tamanho//2, py + tamanho//2)
                    raio = max(1, int(TAMANHO_POWERUP * scale))
                    pygame.draw.circle(tela, AMARELO, centro, raio)
                elif self.grade[y][x] == 5:
                    centro = (px + tamanho//2, py + tamanho//2)
                    raio = max(2, int(TAMANHO_POWERUP * scale * 1.5))
                    pygame.draw.circle(tela, VERDE, centro, raio)
                    pygame.draw.circle(tela, BRANCO, centro, raio - 1)
                elif self.grade[y][x] == 6:
                    centro = (px + tamanho//2, py + tamanho//2)
                    raio = max(2, int(TAMANHO_POWERUP * scale * 1.5))
                    pygame.draw.circle(tela, CIANO, centro, raio)
                    pygame.draw.circle(tela, BRANCO, centro, raio - 1)
                elif self.grade[y][x] == 4:
                    pygame.draw.rect(tela, VERDE, rect)
                    pygame.draw.rect(tela, BRANCO, rect, max(2, int(scale * 2)))
    def eh_parede(self, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            return self.grade[y][x] == 1
        return True
    def pegar_item(self, x, y):
        if 0 <= x < self.largura and 0 <= y < self.altura:
            item = self.grade[y][x]
            if item in [2, 3, 5, 6]:
                self.grade[y][x] = 0
                return item
            if item == 4:
                return None
        return None
    def tem_itens(self):
        return any(item in [2, 3, 5, 6] for linha in self.grade for item in linha)