import pygame

#Cũng tương tự lớp trên để tạo một đối tượng sprite
#ở đây là tạo ground, bên trong có khởi tạo đối tượng tree để thực hiện render đồng thời với ground,
#self.trees_pos là các vị trí của tree nha tôi hơi bận nếu được thì bạn thêm vào cho background đỡ trống
class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.map = pygame.image.load("resources/images/map.png")
    
    def render(self, screen):
        screen.blit(self.map, (0, 0))

    def update(self, screen):
        self.render(screen)