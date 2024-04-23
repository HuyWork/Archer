import pygame, math
from pygame.locals import *
import settings
from arrow import Arrow

class Player(pygame.sprite.Sprite):
    # khởi tạo ban đầu của player
    def __init__(self):
        super().__init__()
        self.character = pygame.image.load("resources/images/dude.png").convert_alpha()
        self.rect = self.character.get_rect()

        self.angle = 0
        self.pos = [200, settings.Screen.HEIGHT/2]
        self.keys = [False, False, False, False]
        self.arrows = []

    # xác định vị trí và hướng quay của player
    def move(self):
        # tính góc quay của player bằng các tính actan của hiệu mouse pos với vị trí của player
        self.mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(self.mouse_pos[1]-(self.pos[1]+32), self.mouse_pos[0]-(self.pos[0]+26))
        self.rot = pygame.transform.rotate(self.character, 360-angle*57.29).convert_alpha()
        self.newpos = (self.pos[0]-self.rot.get_rect().centerx, self.pos[1]-self.rot.get_rect().centery)

        # cập nhật vị trí của player khi trạng thái của key tương ứng là true 
        # và không vượt ra màn hình thì tọa độ được cập nhật
        if self.keys[0] and self.pos[1] > 25:
            self.pos[1]-=5
        elif self.keys[2] and self.pos[1] < settings.Screen.HEIGHT - self.character.get_height():
            self.pos[1]+=5
        if self.keys[1] and self.pos[0] > 25:
            self.pos[0]-=5
        elif self.keys[3] and self.pos[0] < settings.Screen.WIDTH - self.character.get_width():
            self.pos[0]+=5

    # thức hiện cập nhật các trạng thái arrow trong danh sách arrow đã tạo ở phía trên
    def attack(self, screen):
        for arrow in self.arrows:
            arrow.update(screen)

    # render player lên màn hình
    def render(self, screen):
        screen.blit(self.rot, self.newpos)

    # kiểm tra xem có nhấn một trong các nút dưới đây không và cập nhật trạng thái của keys
    def controller(self):
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_w]:
            self.keys[0] = True
        else: self.keys[0] = False
        if pressed_keys[K_a]:
            self.keys[1] = True
        else: self.keys[1] = False
        if pressed_keys[K_s]:
            self.keys[2] = True
        else: self.keys[2] = False
        if pressed_keys[K_d]:
            self.keys[3] = True
        else: self.keys[3] = False
    
    # thêm một đối tựng arrow vào danh sách arrow với các đối số đã nêu ở trên
    def shoot(self):
        arrow = Arrow([self.newpos[0]+32, self.newpos[1]+32], math.atan2(self.mouse_pos[1]-(self.newpos[1]+32), self.mouse_pos[0]-(self.newpos[0]+26)))
        self.arrows.append(arrow)

    # cập nhật vị trí, góc quay, render player
    # cập nhật danh sách arrow
    # kiểm tra điều khiển của người chơi
    def update(self, screen):
        self.move()
        self.attack(screen)
        self.render(screen)
        self.controller()