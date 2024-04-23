import pygame, math

class Enemy(pygame.sprite.Sprite):
    # khởi tạo ban đầu của enemy gồm vị trí, mục tiêu , và tốc độ
    def __init__(self, pos, target, speed):
        super().__init__()
        self.badguy = pygame.image.load("resources/images/badguy.png").convert_alpha()
        self.rect = self.badguy.get_rect(center = pos)
        self.target = target
        self.speed = speed

    # xác định hướng của enemy là tiến vào castle và cập nhật vị trí với tốc độ khởi đầu
    # ở đây ta vẫn xác đinh góc quay bằng actan nhưng về việc di chuyển ta tính khoảng cách rùi cập nhật vị trí
    # ta không cập nhật băng cách xác định sin và cos của angle vì khi đó độ chính xác của quãng đường 
    # đến mục tiêu phụ thuộc vào speed rất lớn, nhưng ở dưới ta cần tùy chỉnh speed theo mỗi dợt quái khác nhau.
    def move(self):
        angle = math.atan2(self.target.centery - self.rect.centery, 
                           self.target.centerx - self.rect.centerx)
        dx = self.target.centerx - self.rect.centerx
        dy = self.target.centery - self.rect.centery

        distance = math.sqrt(dx ** 2 + dy ** 2)

        new_centerx = self.rect.centerx + dx / distance * self.speed
        new_centery = self.rect.centery + dy / distance * self.speed
    
        self.rect.center = (new_centerx, new_centery)
        self.badguyrot = pygame.transform.rotate(self.badguy, math.degrees(-angle) + 180)

    # render enemy
    def render(self, screen):
        screen.blit(self.badguyrot, self.rect)

    # cập nhật vị trí và render enemy
    def update(self, screen):
        self.move()
        self.render(screen)