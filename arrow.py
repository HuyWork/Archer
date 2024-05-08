import pygame, math

class Arrow(pygame.sprite.Sprite):
    # hàm khởi tạo này nhận hai giá trị đầu vào là pos và angle 
    # pos là vị trí tạo ra mũi tên, angle là actan của góc được tạo bởi hiệu mouse position và pos
    def __init__(self, rect, angle, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load("resources/images/arrow.png")
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(rect.center))

        self.vec = pygame.math.Vector2
        self.vel = self.vec(0, 0)
        self.angle = angle

    # quay mũi tên theo hướng của con trỏ chuột
    def rotate(self):
        rotated_image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle)).convert_alpha()
        self.image = rotated_image
        self.rect = rotated_image.get_rect(center=self.rect.center)

    # hàm để cập nhật vị trí của đối tượng arrow
    # tính vận tốc bằng angle sau đó cộng với tọa độ xy
    def move(self):
        self.vel.x = math.cos(self.angle) * 10
        self.vel.y = math.sin(self.angle) * 10

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
    
    # liên tục cập nhật việc vẽ lại và vị trí của  arrow
    def update(self):
        self.rotate()
        self.move()