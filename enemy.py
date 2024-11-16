import pygame
from pathfinder import PathFinder

class Bogey(pygame.sprite.Sprite):
    # khởi tạo ban đầu của enemy gồm vị trí, mục tiêu , và tốc độ
    def __init__(self, pos, target, speed, diagonal_movement, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("resources/images/bogey.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.vec = pygame.math.Vector2
        self.direction = self.vec(0, 0)
        self.pos = self.rect.center
        self.target, self.speed = target, speed
        self.hp = 1

        # tạo tuyến đường cho bogey
        self.pathfinder = PathFinder(self.pos, self.target)
        self.path = self.pathfinder.create_path(diagonal_movement)
        self.collision_rects = self.pathfinder.create_collision_rects()

    # kiểm tra va chạm với các ô trong ma trận và xác định hướng di chuyển tiếp theo
    def get_direction(self):
        if self.collision_rects:
            start = self.vec(self.pos)
            end = self.vec(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = self.vec(0, 0)
            self.path = []

    # kiểm tra va chạm với các ô trong ma trận
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.path = []
    
    # cập nhật vị trí của bogey
    def move(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos
    
    def update(self):
        self.move()

class Snail(pygame.sprite.Sprite):
    # khởi tạo ban đầu của enemy gồm vị trí, mục tiêu , và tốc độ
    def __init__(self, pos, target, speed, diagonal_movement, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("resources/images/snail.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.vec = pygame.math.Vector2
        self.direction = self.vec(0, 0)
        self.pos = self.rect.center
        self.target, self.speed = target, speed
        self.hp = 2

        # tạo tuyến đường cho bogey
        self.pathfinder = PathFinder(self.pos, self.target)
        self.path = self.pathfinder.create_path(diagonal_movement)
        self.collision_rects = self.pathfinder.create_collision_rects()

    # kiểm tra va chạm với các ô trong ma trận và xác định hướng di chuyển tiếp theo
    def get_direction(self):
        if self.collision_rects:
            start = self.vec(self.pos)
            end = self.vec(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = self.vec(0, 0)
            self.path = []

    # kiểm tra va chạm với các ô trong ma trận
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.path = []
    
    # cập nhật vị trí của bogey
    def move(self):
        self.pos += self.direction * self.speed
        self.check_collisions()
        self.rect.center = self.pos
    
    def update(self):
        self.move()