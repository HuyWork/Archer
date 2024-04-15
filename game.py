import pygame, sys
from pygame.locals import *
import random
import math
from tkinter import filedialog
from tkinter import *
from pybutton import Button

pygame.init()
vec = pygame.math.Vector2
WIDTH = 640
HEIGHT = 480
ACC = 0.3
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
FONT = "resources/font.ttf"
flags = pygame.RESIZABLE
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Game")

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tree = pygame.image.load("resources/images/tree.png").convert_alpha()

    def render(self, x, y):
        displaysurface.blit(self.tree, (x, y))

class Ground(pygame.sprite.Sprite):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.grass = pygame.image.load("resources/images/grass.png").convert_alpha()
    
    def render(self):
        for x in range(int(WIDTH/self.grass.get_width())+1):
            for y in range(int(HEIGHT/self.grass.get_height())+1):
                displaysurface.blit(self.grass, (x * 100, y * 100))
        self.tree.render(100, 100)

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.castle = pygame.image.load("resources/images/castle.png").convert_alpha()
        self.x = 25
        self.y = 180

    def render(self):
        displaysurface.blit(self.castle, (self.x, self.y))
                
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.character = pygame.image.load("resources/images/dude.png").convert_alpha()
        self.arrow = pygame.image.load("resources/images/arrow.png").convert_alpha()
        self.arrows = []
        self.rect = self.character.get_rect()

        # Position and direction
        self.mousepos = []
        self.angle = 0
        self.pos = [100, 100]
        self.keys = [False, False, False, False]

    def collsion(self):
        pass

    def move(self):
        self.mousepos = pygame.mouse.get_pos()
        angle = math.atan2(self.mousepos[1]-(self.pos[1]+32), self.mousepos[0]-(self.pos[0]+26))
        self.rot = pygame.transform.rotate(self.character, 360-angle*57.29).convert_alpha()
        self.newpos = (self.pos[0]-self.rot.get_rect().width/2, self.pos[1]-self.rot.get_rect().height/2)

        if self.keys[0] and self.pos[1] > 25:
            self.pos[1]-=5
        elif self.keys[2] and self.pos[1] < HEIGHT - self.character.get_height():
            self.pos[1]+=5
        if self.keys[1] and self.pos[0] > 25:
            self.pos[0]-=5
        elif self.keys[3] and self.pos[0] < WIDTH - self.character.get_width():
            self.pos[0]+=5

    def attack(self):
        for arrow in self.arrows:
            index=0
            velx=math.cos(arrow[0])*10
            vely=math.sin(arrow[0])*10
            arrow[1] += velx
            arrow[2] += vely
            if arrow[1] < -64 or arrow[1] > 640 or arrow[2] < -64 or arrow[2] > 480:
                self.arrows.pop(index)
            index+=1
            for projectile in self.arrows:
                arrow1 = pygame.transform.rotate(self.arrow, 360-projectile[0]*57.29)
                displaysurface.blit(arrow1, (projectile[1], projectile[2]))

    def render(self):
        displaysurface.blit(self.rot, self.newpos)

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
    
    def shoot(self): 
        self.arrows.append([math.atan2(self.mousepos[1]-(self.newpos[1]+32), self.mousepos[0]-(self.newpos[0]+26)), 
                                self.newpos[0]+32,self.newpos[1]+32])

    def update(self):
        self.move()
        self.attack()
        self.render()
        self.controller()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.badguy = pygame.image.load("resources/images/badguy.png")
        self.rect = self.badguy.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0)
    
    def move(self):
        pass

    def render(self):
        displaysurface.blit(self.badguy, (0, 0))

class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
    
    def stage_handler(self):
        self.root = Tk()
        self.root.geometry('200x170')
             
        button1 = Button(self.root, text = "Twilight Dungeon", width = 18, height = 2,
                        command = self.world1)
        button2 = Button(self.root, text = "Skyward Dungeon", width = 18, height = 2,
                        command = self.world2)
        button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2,
                        command = self.world3)
              
        button1.place(x = 40, y = 15)
        button2.place(x = 40, y = 65)
        button3.place(x = 40, y = 115)
             
        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        pygame.time.set_timer(self.enemy_generation, 2000)
        self.battle = True
 
    def world2(self):
        self.battle = True
        
    def world3(self):
        self.battle = True

class Screen():
    def __init__(self, ground, castle, player, displaysurface):
        self.menu_bgimage = pygame.image.load("resources/images/menu_bg.png")
        self.displaysurface = displaysurface
        self.ground = ground
        self.castle = castle
        self.player = player
        
    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MOUSE_POS):
                        self.play()
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    
                    WINDOW_WIDTH, WINDOW_HEIGHT = event.size
                    self.displaysurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 
                                                                pygame.RESIZABLE)
            
            self.displaysurface.fill((255, 255, 255))
            self.displaysurface.blit(self.menu_bgimage, (0, 0))
            pygame.display.set_caption("Menu")
            MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = pygame.font.Font(FONT, 45).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(320, 50))

            PLAY_BUTTON = Button(image=pygame.image.load("resources/images/button.png"), pos=(320, 150), 
                                text_input="PLAY", font=pygame.font.Font(FONT, 25), base_color="White", hovering_color="#3b8335")
            QUIT_BUTTON = Button(image=pygame.image.load("resources/images/button.png"), pos=(320, 250), 
                                text_input="QUIT", font=pygame.font.Font(FONT, 25), base_color="White", hovering_color="#3b8335")

            self.displaysurface.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.displaysurface)

            pygame.display.update()
    
    def play(self):
        pygame.display.set_caption("Play")

        while True:
            displaysurface.fill((255, 255, 255))
            
            self.ground.render()
            self.castle.render()
            self.player.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.shoot()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
            
            pygame.display.update()
            FPS_CLOCK.tick(FPS)

tree = Tree()
ground = Ground(tree)
castle = Castle()
player = Player()
handler = EventHandler()
screen = Screen(ground, castle, player, displaysurface)

def main():
    screen.main_menu()

if __name__ == "__main__":
    main()