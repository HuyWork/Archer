import pygame, math
from pygame.locals import *
import settings
from arrow import Arrow

class Player(pygame.sprite.Sprite):
    # khởi tạo ban đầu của player
    def __init__(self, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load("resources/images/dude.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(200, settings.Screen.HEIGHT/2))

        self.vec = pygame.math.Vector2
        self.vel = self.vec(0, 0)
        self.mouse_pos = [0, 0]
        self.speed = 5
    
    # kiểm tra xem có nhấn một trong các nút dưới đây không và cập nhật trạng thái của keys
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel = self.vec(0, 0)
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed

    # xác định vị trí và hướng quay của player
    # tính góc quay của player bằng các tính actan của hiệu mouse pos với vị trí của player
    def rotate(self):
        self.mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(self.mouse_pos[1] - self.rect.centery, self.mouse_pos[0] - self.rect.centerx)
        rotated_image = pygame.transform.rotate(self.original_image, math.degrees(-angle)).convert_alpha()
        self.image = rotated_image
        self.rect = rotated_image.get_rect(center=self.rect.center)

    # cập nhật vị trí của player
    # và không vượt ra màn hình thì tọa độ được cập nhật
    def move(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.rect.right > settings.Screen.WIDTH:
            self.rect.right = settings.Screen.WIDTH
        if self.rect.bottom > settings.Screen.HEIGHT:
            self.rect.bottom = settings.Screen.HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
    
    # tạo và thêm đối tượng arrow vào group sprite
    def shoot(self, *groups):
        angle = math.atan2(self.mouse_pos[1] - self.rect.centery, self.mouse_pos[0] - self.rect.centerx)
        Arrow(self.rect, angle, *groups)
        

    # cập nhật vị trí, góc quay
    # cập nhật danh sách arrow
    # kiểm tra điều khiển của người chơi
    def update(self):
        self.move()
        self.rotate()
        self.handle_input()