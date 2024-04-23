import pygame

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# khởi tạo và vẽ thành HP
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.healthbar = pygame.image.load("resources/images/healthbar.png")
        self.health = pygame.image.load("resources/images/health.png")
        self.healthvalue = 194

    def render(self, screen):
        screen.blit(self.healthbar, (5,5))
        for value in range(self.healthvalue):
            screen.blit(self.health, (value + 8, 8))

    def update(self, screen):
            self.render(screen)