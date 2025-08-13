import pygame
class Player:
    def __init__(self):
        
        self.sprite_sheet = pygame.image.load("spritesplayer.png").convert_alpha()

    
        self.frame_width = self.sprite_sheet.get_width() // 2  
        self.frame_height = self.sprite_sheet.get_height()

        
        self.frames = [
            self.sprite_sheet.subsurface((0, 0, self.frame_width, self.frame_height)),
            self.sprite_sheet.subsurface((self.frame_width, 0, self.frame_width, self.frame_height))
        ]

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 1  # ms por frame

        # Posição inicial do jogador
        self.x = 400
        self.y = 300
        self.speed = 0

    def update(self, teclas):
        # Movimento básico
        if teclas[pygame.K_LEFT]:
            self.x -= self.speed
        if teclas[pygame.K_RIGHT]:
            self.x += self.speed
        if teclas[pygame.K_UP]:
            self.y -= self.speed
        if teclas[pygame.K_DOWN]:
            self.y += self.speed

        # Atualiza animação
        self.animation_timer += pygame.time.get_ticks() % 1000
        if self.animation_timer > self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], (self.x, self.y))
