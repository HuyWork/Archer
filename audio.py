import pygame

# lưu trữ cái audio của game
class Audio:
    def __init__(self):
        self.castle_damaged = pygame.mixer.Sound("resources/audio/explode.wav")
        self.castle_damaged.set_volume(0.05)

        self.enemy_damaged = pygame.mixer.Sound("resources/audio/enemy.wav")
        self.enemy_damaged.set_volume(0.05)

        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        self.shoot.set_volume(0.05)
        