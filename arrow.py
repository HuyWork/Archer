import pygame, math

class Arrow(pygame.sprite.Sprite):
    # hàm khởi tạo này nhận hai giá trị đầu vào là pos và angle 
    # pos là vị trí tạo ra mũi tên, angle là actan của góc được tạo bởi hiệu mouse position và pos
    def __init__(self, pos, angle):
        self.arrow = pygame.image.load("resources/images/arrow.png")
        self.rect = self.arrow.get_rect()
        self.pos = pos
        self.angle = angle

    # hàm để cập nhật vị trí của đối tượng arrow
    # tính vận tốc bằng angle sau đó cộng với tọa độ xy
    # arrowrot là dùng để arrow quay mặt vào mục tiêu
    def move(self):
        velx=math.cos(self.angle) * 10
        vely=math.sin(self.angle) * 10
        self.pos[0] += velx
        self.pos[1] += vely
        self.arrowrot = pygame.transform.rotate(self.arrow, math.degrees(-self.angle))
        self.rect.center = (self.pos[0], self.pos[1])
    
    # vẽ arrow ở vị trí đã xác định ở hàm move
    def render(self, screen):
        screen.blit(self.arrowrot, self.rect)
    
    # liên tục cập nhật việc vẽ lại và vị trí của  arrow
    def update(self, screen):
        self.move()
        self.render(screen)