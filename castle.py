import pygame
from settings import *
from preset import Preset

#tạo class sprite castle, mục tiêu chính cần bảo vệ
class Castle(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("resources/images/castle.png").convert_alpha()
        self.rect = self.image.get_rect(center=(25, Screen.HEIGHT / 2))
        self.hp = Preset.hp_castle
        self.damaged = 0
    
    # khi hp của castle xuống 50% thì sẽ thành castle broken
    def update(self):
        if self.hp < Preset.hp_castle // 2:
            self.image = pygame.image.load("resources/images/castle_broken.png").convert_alpha()
        if self.hp <= 0:
            self.image = pygame.image.load("resources/images/castle_destroy.png").convert_alpha()
        