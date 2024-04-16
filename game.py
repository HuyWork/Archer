import pygame, sys
from pygame.locals import *
import random
import math
from pybutton import Button

pygame.init()
vec = pygame.math.Vector2
WIDTH = 640
HEIGHT = 480
FPS = 60
FPS_CLOCK = pygame.time.Clock()
FONT = "resources/font.ttf"
'''
thiết lập màn hình game, không khuyến khích dùng full màn hình vì pygame scale ảnh lên thì chất hơi kém.
nếu muốn full màn hình thì thay bằng câu lệnh:
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), flags)
'''
flags = pygame.FULLSCREEN
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

'''
lớp cấy là để vẽ đối tượng câu lên mành hình gồm có hai hàm cơ bản:
hàm __init__ khởi tạo lúc đầu, self là tham chiếu đến đối tượng tại mà bạn đang làm việc trong lớp
hàm render thì cơ bản là vẽ tree lên màn hình với pos là tọa độ
'''
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tree = pygame.image.load("resources/images/tree.png").convert_alpha()

    def render(self, pos):
        displaysurface.blit(self.tree, pos)
'''
Cũng tương tự lớp trên để tạo một đối tượng sprite
ở đây là tạo ground, bên trong có khởi tạo đối tượng tree để thực hiện render đồng thời với ground,
self.trees_pos là các vị trí của tree nha tôi hơi bận nếu được thì bạn thêm vào cho background đỡ trống
'''
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tree = Tree()
        self.grass = pygame.image.load("resources/images/grass.png").convert_alpha()
        self.trees_pos = [[80, 25], [60, 50], [100, 50], [150, 40], [140, 60], [70, 65], [120, 80]]
    
    def render(self):
        for x in range(int(WIDTH/self.grass.get_width())+1):
            for y in range(int(HEIGHT/self.grass.get_height())+1):
                displaysurface.blit(self.grass, (x * 100, y * 100))
        for i in self.trees_pos:
            self.tree.render(i)

    def update(self):
        self.render()

'''
tạo class sprite castle khởi tọa cùng với thanh HealthBar, mục tiêu chính cần bảo vệ
'''
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.castle = pygame.image.load("resources/images/castle.png")
        self.rect = self.castle.get_rect()
        self.healthBar = HealthBar()
        self.rect.center = [75, HEIGHT/2]

    # kiểm tra xem lâu đài có va chạm với danh sách enemies không.
    # nếu có thì xóa kẻ thù và trừ máu castle.
    def collision(self, enemies):
        for enemy in enemies:
            if enemy.rect.colliderect(self.rect):
                enemies.remove(enemy)
                self.healthBar.healthvalue -= random.randint(1,5)

    def render(self):
        displaysurface.blit(self.castle, self.rect)
    
    # cập nhật trạng thài thanh HP và render nso và castle
    def update(self):
        self.healthBar.render()
        self.render()

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
    def render(self):
        displaysurface.blit(self.arrowrot, self.rect)
    
    # liên tục cập nhật việc vẽ lại và vị trí của  arrow
    def update(self):
        self.move()
        self.render()

class Player(pygame.sprite.Sprite):
    # khởi tạo ban đầu của player
    def __init__(self):
        super().__init__()
        self.character = pygame.image.load("resources/images/dude.png").convert_alpha()
        self.rect = self.character.get_rect()

        self.mousepos = []
        self.angle = 0
        self.pos = [200, HEIGHT/2]
        self.keys = [False, False, False, False]
        self.arrows = []

    # xác định vị trí và hướng quay của player
    def move(self):
        # tính góc quay của player bằng các tính actan của hiệu mouse pos với vị trí của player
        self.mousepos = pygame.mouse.get_pos()
        angle = math.atan2(self.mousepos[1]-(self.pos[1]+32), self.mousepos[0]-(self.pos[0]+26))
        self.rot = pygame.transform.rotate(self.character, 360-angle*57.29).convert_alpha()
        self.newpos = (self.pos[0]-self.rot.get_rect().centerx, self.pos[1]-self.rot.get_rect().centery)

        # cập nhật vị trí của player khi trạng thái của key tương ứng là true 
        # và không vượt ra màn hình thì tọa độ được cập nhật
        if self.keys[0] and self.pos[1] > 25:
            self.pos[1]-=5
        elif self.keys[2] and self.pos[1] < HEIGHT - self.character.get_height():
            self.pos[1]+=5
        if self.keys[1] and self.pos[0] > 25:
            self.pos[0]-=5
        elif self.keys[3] and self.pos[0] < WIDTH - self.character.get_width():
            self.pos[0]+=5

    # thức hiện cập nhật các trạng thái arrow trong danh sách arrow đã tạo ở phía trên
    def attack(self):
        for arrow in self.arrows:
            arrow.update()

    # render player lên màn hình
    def render(self):
        displaysurface.blit(self.rot, self.newpos)

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
        arrow = Arrow([self.newpos[0]+32, self.newpos[1]+32], math.atan2(self.mousepos[1]-(self.newpos[1]+32), self.mousepos[0]-(self.newpos[0]+26)))
        self.arrows.append(arrow)

    # cập nhật vị trí, góc quay, render player
    # cập nhật danh sách arrow
    # kiểm tra điều khiển của người chơi
    def update(self):
        self.move()
        self.attack()
        self.render()
        self.controller()
    
class Enemy(pygame.sprite.Sprite):
    # khởi tạo ban đầu của enemy gồm vị trí, mục tiêu , và tốc độ
    def __init__(self, pos, target, speed):
        super().__init__()
        self.badguy = pygame.image.load("resources/images/badguy.png").convert_alpha()
        self.rect = self.badguy.get_rect()
        self.rect.center = pos
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
    def render(self):
        displaysurface.blit(self.badguyrot, self.rect)

    # cập nhật vị trí và render enemy
    def update(self):
        self.move()
        self.render()

# khởi tạo và vẽ thành HP
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.healthbar = pygame.image.load("resources/images/healthbar.png")
        self.health = pygame.image.load("resources/images/health.png")
        self.healthvalue = 194
    
    def render(self):
        displaysurface.blit(self.healthbar, (5,5))
        for value in range(self.healthvalue):
            displaysurface.blit(self.health, (value + 8, 8))

class EventHandler():
    # khởi tạo hàm sử lý sự kiện.
    def __init__(self):
        self.enemy_count = 0
        self.new_stage = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_stage, 200)
        self.enemy_generation = pygame.USEREVENT + 2
        self.stage_enemies = [9, 16, 25, 33, 41, 45, 51, 60, 65, 72]
        self.enemies = []
        self.stage = 1
        self.score = 0
    
    # đang trong quá trính phát triển
    def stage_handler(self):
        pass

    # kiểm tra va chạm của danh sách arrow và danh sách enemy
    def collision(self, arrows):
        for arrow in arrows:
            for enemy in self.enemies:
                if arrow.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self.score += 1
                if enemy.rect.colliderect(arrow.rect):
                    arrows.remove(arrow)

    # chuyển sang stage tiếp theo, gán bộ đếm enemy = 0, setup lại thời gian của timer sự kiện enemy_generation
    def next_stage(self):
        self.stage += 1
        self.enemy_count = 0
        print("Stage: "  + str(self.stage))
        pygame.time.set_timer(self.enemy_generation, 500 - (20 * self.stage)) 

    # khởi đầu wave 1, stage = 1
    def wave1(self):
        pygame.time.set_timer(self.enemy_generation, 500)

# chứa các thiệt lập để hiển thị các màng hình trong game
class Screen():
    # ngoài khởi tạo các image cần ra ta còn khởi tạo các đối tượng của các class ở trên
    # đây là các đối tượng sẽ được sử dụng trong hàm play
    def __init__(self):
        self.menu_bgimage = pygame.image.load("resources/images/menu_bg.png")
        self.pause_image = pygame.image.load("resources/images/in_game_menu.png")
        self.win_game_bg = pygame.image.load("resources/images/you_win.png")
        self.game_over_bg = pygame.image.load("resources/images/game_over.png")
        self.button_image = pygame.image.load("resources/images/button.png")
        self.pause_rect = self.pause_image.get_rect(center=(320, 240))
        self.ground = Ground()
        self.castle = Castle()
        self.player = Player()
        self.handler = EventHandler()
        self.highscore = 0
    
    # bắt đầu một vòng chơi mới, khởi tạo lại các đối tượng ban đầu có trong play
    def new_game(self):
        self.ground = Ground()
        self.castle = Castle()
        self.player = Player()
        self.handler = EventHandler()
        self.handler.wave1()
        self.play()

    # Thiết lập một button bằng một class tự custom
    def button(self, image, scale, pos, text, fontsize):
        return Button(image=pygame.transform.scale(image, scale), pos=pos,
               text_input=text, font=pygame.font.Font(FONT, fontsize), base_color="White", hovering_color="#3b8335")
    # thiết lập để render ra một text.
    def text_render(self, text, fontsize, color, pos):
        TEXT = pygame.font.Font(FONT, fontsize).render(text, True, color)
        RECT = TEXT.get_rect(center=pos)
        displaysurface.blit(TEXT, RECT)

    # màn hình bắt đầu 
    def main_menu(self):
        pygame.display.set_caption("Menu")
        while True:
            # cập nhật vị trí con trỏ liên tục
            MOUSE_POS = pygame.mouse.get_pos()
            # cập nhật menu image
            displaysurface.fill((255, 255, 255))
            displaysurface.blit(self.menu_bgimage, (0, 0))
            
            # khởi tạo các button cần thiết
            PLAY_BUTTON = self.button(self.button_image, [180, 71], [320, 150], "PLAY", 20)
            QUIT_BUTTON = self.button(self.button_image, [180, 71], [320, 250], "QUIT", 20)

            # render các text cần thiết
            self.text_render("MAIN MENU", 45,"#b68f40", [320, 50])

            # render và cập nhật button
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                # đỏi màu chữ khi phát hiện con trỏ chuột ở trong button
                button.changeColor(MOUSE_POS)
                button.update(displaysurface)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # kiểm tra có click con trỏ vào button hay không
                    if PLAY_BUTTON.checkForInput(MOUSE_POS):
                        self.new_game()
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
    
    # Khởi tạo màn hình play
    def play(self):
        pygame.display.set_caption("Play")
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            displaysurface.fill((255, 255, 255))

            # khởi tạo label và button cần
            # ở đây mình dùng luôn button đê tạo lable cho tiện, chỉ cần không kiểm tra nhấn hay cho đổi màu
            # thì chẳng khác gì label cả
            SCORE_LABEL = self.button(pygame.image.load("resources/images/score_label.png"), [161, 52], [500, 30], "SCORE:" + str(self.handler.score), 15)
            SELECTER_BUTTON = self.button(pygame.image.load("resources/images/selector_button.png"), [40, 40], [610, 25], "", 25)

            # khối code này để update các đối tượng như là ground, castle, enemy, player
            self.ground.update()
            self.castle.update()
            for entity in self.handler.enemies:
                entity.update()
            self.player.update()
            self.handler.collision(self.player.arrows)
            self.castle.collision(self.handler.enemies)

            # vẽ button và lable
            for button in [SELECTER_BUTTON, SCORE_LABEL]:
                button.update(displaysurface)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        self.win_game()
                    if event.key == K_2:
                        self.game_over()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # kiểm tra xem có bấm con trỏ trong phạm vi button selector không
                    # nếu có chuyển sang pause screen
                    if SELECTER_BUTTON.checkForInput(MOUSE_POS):
                        self.pause()
                    self.player.shoot()
                # kiểm tra sự kiện new_stage để xem đã có thể chuyển qua stage khác chưa
                if event.type == self.handler.new_stage:
                    # nếu số lượng của enemy_count bằng với số lương stage_enemies tương ứng 
                    # và danh sách enemies là rỗng thì sang stage tiếp
                    if self.handler.enemy_count == self.handler.stage_enemies[self.handler.stage - 1] and not self.handler.enemies:
                        self.handler.next_stage()
                    # nếu hp castle <= 0 chuyển qua màng hình game over
                    if self.castle.healthBar.healthvalue <= 0:
                        self.game_over()
                    # nếu hp castle > 0 và đã vượt qua hết các stage hiện có thì qua màn hình win game
                    if self.handler.stage - 1 == len(self.handler.stage_enemies) and self.castle.healthBar.healthvalue > 0:
                        self.win_game()
                # kiểm tra xem đã đến lúc tạo quái chưa
                if event.type == self.handler.enemy_generation:
                    # nếu số lượng enemy_count < số trong stage_enemies thì thêm tạo thêm quái ở vị trí bất kỳ
                    if self.handler.enemy_count < self.handler.stage_enemies[self.handler.stage - 1]:
                        enemy = Enemy([640, random.randint(50,430)], self.castle.rect, self.handler.stage)
                        self.handler.enemies.append(enemy)
                        self.handler.enemy_count += 1
                        print(self.handler.enemy_count)
            pygame.display.update()
            FPS_CLOCK.tick(60)

    # màn hình pause
    def pause(self):
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            displaysurface.blit(self.pause_image, self.pause_rect)

            CONTINUE_BUTTON = self.button(self.button_image, [100, 40], [320, 270], "CONTINUE", 8)
            HOME_BUTTON = self.button(self.button_image, [100, 40], [320, 320], "HOME", 8)

            self.text_render("PAUSE", 20, "#218ede", [320, 145])
            self.text_render("HIGH SCORE:", 15, "white", [320, 200])
            self.text_render(str(self.highscore), 15, "white", [320, 230])

            for button in [CONTINUE_BUTTON, HOME_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(displaysurface)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BUTTON.checkForInput(MOUSE_POS):
                        self.play()
                    if HOME_BUTTON.checkForInput(MOUSE_POS):
                        self.main_menu()
            pygame.display.update()
    
    # màn hình win game
    def win_game(self):
        displaysurface.blit(self.win_game_bg, (0, 0))
        while True:
            MOUSE_POS = pygame.mouse.get_pos()
            
            REPLAY_BUTTON = self.button(self.button_image, [180, 71], [200, 400], "REPLAY", 20)
            HOME_BUTTON = self.button(self.button_image, [180, 71], [420, 400], "HOME", 20)

            for button in [REPLAY_BUTTON, HOME_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(displaysurface)
            
            # highscore là thuộc tính được khởi tạo bởi screen nên khi khởi tạo lại new thì giá trị sẽ
            # không bị reset về 0 như score của handler
            if self.highscore < self.handler.score:
                self.highscore = self.handler.score

            self.text_render("SCORE:" + str(self.handler.score), 15, "white", [320, 270])
            self.text_render("HIGH SCORE:" + str(self.highscore), 15, "white", [320, 300])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if REPLAY_BUTTON.checkForInput(MOUSE_POS):
                        self.new_game()
                    if HOME_BUTTON.checkForInput(MOUSE_POS):
                        self.main_menu()
            pygame.display.update()
    # tạo màn hình game over
    def game_over(self):
        displaysurface.blit(self.game_over_bg, (0, 0))
        while True:
            MOUSE_POS = pygame.mouse.get_pos()

            RETRY_BUTTON = self.button(self.button_image, [180, 71], [200, 400], "RETRY", 20)
            HOME_BUTTON = self.button(self.button_image, [180, 71], [420, 400], "HOME", 20)

            for button in [RETRY_BUTTON, HOME_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(displaysurface)

            if self.highscore < self.handler.score:
                self.highscore = self.handler.score

            self.text_render("SCORE:" + str(self.handler.score), 15, "white", [320, 270])
            self.text_render("HIGH SCORE:" + str(self.highscore), 15, "white", [320, 300])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if RETRY_BUTTON.checkForInput(MOUSE_POS):
                        self.new_game()
                    if HOME_BUTTON.checkForInput(MOUSE_POS):
                        self.main_menu()
            pygame.display.update()
            
def main():
    screen = Screen()
    screen.main_menu()

if __name__ == "__main__":
    main()