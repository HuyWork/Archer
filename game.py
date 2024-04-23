import pygame, sys, random, settings
from pygame.locals import *
from pyui import Button
from player import Player
from enemy import Enemy
from map import Map
from castle import Castle
from events import EventHandler


#thiết lập màn hình game, không khuyến khích dùng full màn hình vì pygame scale ảnh lên thì chất hơi kém.
#nếu muốn full màn hình thì thay bằng câu lệnh:
#displaysurface = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.init()
FPS_CLOCK = pygame.time.Clock()
flags = pygame.FULLSCREEN
displaysurface = pygame.display.set_mode((settings.Screen.WIDTH, settings.Screen.HEIGHT))
pygame.display.set_caption("Game")

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
        self.map = Map()
        self.castle = Castle()
        self.player = Player()
        self.handler = EventHandler()
        self.highscore = 0
    
    # bắt đầu một vòng chơi mới, khởi tạo lại các đối tượng ban đầu có trong play
    def new_game(self):
        self.map = Map()
        self.castle = Castle()
        self.player = Player()
        self.handler = EventHandler()
        self.handler.wave1()
        self.play()

    # Thiết lập một button bằng một class tự custom
    def button(self, image, scale, pos, text, fontsize):
        return Button(image=pygame.transform.scale(image, scale), pos=pos,
               text_input=text, font=pygame.font.Font(settings.Screen.FONT, fontsize), base_color="White", hovering_color="#3b8335")
    # thiết lập để render ra một text.
    def text_render(self, text, fontsize, color, pos):
        TEXT = pygame.font.Font(settings.Screen.FONT, fontsize).render(text, True, color)
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

            # khối code này để update các đối tượng như là map, castle, enemy, player
            self.map.update(displaysurface)
            self.castle.update(displaysurface)
            for entity in self.handler.enemies:
                entity.update(displaysurface)
            self.player.update(displaysurface)
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