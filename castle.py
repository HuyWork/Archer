import pygame, random
import settings
from pyui import HealthBar

#tạo class sprite castle khởi tọa cùng với thanh HealthBar, mục tiêu chính cần bảo vệ
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.castle = pygame.image.load("resources/images/castle.png")
        self.rect = self.castle.get_rect()
        self.healthBar = HealthBar()
        self.rect.center = [75, settings.Screen.HEIGHT / 2]

    # kiểm tra xem lâu đài có va chạm với danh sách enemies không.
    # nếu có thì xóa kẻ thù và trừ máu castle.
    def collision(self, enemies):
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect):
                enemies.remove(enemy)
                self.healthBar.healthvalue -= random.randint(1,5)

    def render(self, screen):
        screen.blit(self.castle, self.rect)
    
    # cập nhật trạng thài thanh HP và render nso và castle
    def update(self, screen):
        self.healthBar.render(screen)
        self.render(screen)