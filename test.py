import pygame, sys, settings, math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((settings.Screen.WIDTH, settings.Screen.HEIGHT))
pygame.display.set_caption("Test")
map = pygame.image.load("resources/images/map.png").convert()
FPS_CLOCK = pygame.time.Clock()
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load("resources/images/dude.png").convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(200, settings.Screen.HEIGHT/2))
        self.angle = 0
        self.speed = 5
        self.vel = vec(0, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel = vec(0, 0)
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed
    
    def rotate(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.angle = math.atan2(self.mouse_pos[1] - self.rect.centery, self.mouse_pos[0] - self.rect.centerx)
        rotated_image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle)).convert_alpha()
        self.image = rotated_image
        self.rect = rotated_image.get_rect(center=self.rect.center)

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

    def update(self):
        self.move()
        self.rotate()
        self.handle_input()
        

player = Player()
all_scripts = pygame.sprite.Group()
all_scripts.add(player)

while True:
    screen.fill((255, 255, 255))
    screen.blit(map, (0, 0))

    all_scripts.draw(screen)
    all_scripts.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    FPS_CLOCK.tick(60)

