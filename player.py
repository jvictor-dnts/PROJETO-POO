import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        sprite_path = os.path.join(os.path.dirname(__file__), "data", "images", "sprite_sheet.png")
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()

        self.frames_por_linha = 8
        self.linhas = 3
        self.frame_width = self.sprite_sheet.get_width() // self.frames_por_linha
        self.frame_height = self.sprite_sheet.get_height() // self.linhas

        self.andar_frente = self.get_frames(0)  
        self.andar_costas = self.get_frames(1) 
        self.andar_direita = self.get_frames(2)
        self.andar_esquerda = [pygame.transform.flip(frame, True, False) for frame in self.andar_direita]

    
        self.atual = 0
        self.image = self.andar_frente[0]
        self.image = pygame.transform.scale(self.image, (64*3, 64*3))
        self.x = 300
        self.y = 350
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.velocidade = 4
        self.direcao = "frente"

    def get_frames(self, linha):
        frames = []
        for col in range(self.frames_por_linha):
            rect = pygame.Rect(
                col * self.frame_width,
                linha * self.frame_height,
                self.frame_width,
                self.frame_height
            )
            frame = self.sprite_sheet.subsurface(rect)
            frames.append(frame)
        return frames

    def update(self, teclas):
        self.atual += 0.2

        if teclas[pygame.K_d]:
            self.x += self.velocidade
            self.direcao = "direita"
            if self.atual >= len(self.andar_direita):
                self.atual = 0
            self.image = self.andar_direita[int(self.atual)]

        elif teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.direcao = "esquerda"
            if self.atual >= len(self.andar_esquerda):
                self.atual = 0
            self.image = self.andar_esquerda[int(self.atual)]

        elif teclas[pygame.K_w]:
            self.y -= self.velocidade
            self.direcao = "costas"
            if self.atual >= len(self.andar_costas):
                self.atual = 0
            self.image = self.andar_costas[int(self.atual)]

        elif teclas[pygame.K_s]:
            self.y += self.velocidade
            self.direcao = "frente"
            if self.atual >= len(self.andar_frente):
                self.atual = 0
            self.image = self.andar_frente[int(self.atual)]

        else:
            if self.direcao == "direita":
                self.image = self.andar_direita[0]
            elif self.direcao == "esquerda":
                self.image = self.andar_esquerda[0]
            elif self.direcao == "frente":
                self.image = self.andar_frente[0]
            elif self.direcao == "costas":
                self.image = self.andar_costas[0]

        self.rect.topleft = (self.x, self.y)
        self.image = pygame.transform.scale(self.image, (64*3, 64*3))

    def draw(self, tela):
        tela.blit(self.image, self.rect)
