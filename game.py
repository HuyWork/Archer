import pygame, sys
from pygame.locals import *
from settings import *
from ui import *
from events import *
from audio import *

pygame.init()
screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
pygame.display.set_caption("Game")
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.set_volume(0.25)

FPS_CLOCK = pygame.time.Clock()

class Game():
    def __init__(self):
        self.menu_bg = pygame.image.load("resources/images/menu_bg.png").convert_alpha()
        self.map_bg = pygame.image.load("resources/images/map.png").convert_alpha()
        self.victory_bg = pygame.image.load("resources/images/victory_bg.png").convert_alpha()
        self.game_over_bg = pygame.image.load("resources/images/game_over_bg.png").convert_alpha()
        pygame.mixer.music.play(-1, 0.0)

        # khởi tạo các group sprite trong game
        # các group sprite là nơi chứa các sprite, các class có subclass là pygame.sprite.Sprite sẽ được xem là sprite
        # các class sprite có các thông số bắt buộc là image và rect để khi dùng hàm dawn của group sprite chúng sẽ vẽ các sprite lên màn hình
        # các class sprite có thể có hàm update hoặc không
        # nếu có thì khi update các group sprite chúng sẽ gọi vào các hàm update của từng sprite trong group
        # đối số *groups của hàm khởi tạo của class sprite là để truyền các group sprite 
        # thì khi khởi tạo object của class chúng sẽ tự động được thêm vào các group đã truyền vào
        self.ui_sprites = pygame.sprite.Group()
        self.game_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.hp = pygame.sprite.Group()

        self.ui = UI(self)
        self.handler = GameHandler(self)
        self.audio = Audio()
        self.index = 0
    
    def menu(self):
        self.ui.set_ui_menu()
        while True:
            # cập nhật menu image
            screen.fill((255, 255, 255))
            screen.blit(self.menu_bg, (0, 0))

            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # kiểm tra có click con trỏ vào button hay không
                    if self.ui.PLAY_BUTTON.check_for_input():
                        self.level()
                    if self.ui.QUIT_BUTTON.check_for_input():
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    def level(self):
        self.ui.set_ui_level()
        while True:
            screen.fill((255, 255, 255))
            screen.blit(self.menu_bg, (0, 0))

            self.ui_sprites.draw(screen)
            self.ui_sprites.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.PREVIOUS_BUTTON.check_for_input():
                        self.menu()
                    if self.ui.LV1_BUTTON.check_for_input():
                        self.index = 0
                        self.handler.set_new_level()
                        self.play()
                    if self.ui.LV2_BUTTON.check_for_input():
                        self.index = 1
                        self.handler.set_new_level()
                        self.play()
                    if self.ui.LV3_BUTTON.check_for_input():
                        self.index = 2
                        self.handler.set_new_level()
                        self.play()
            pygame.display.update()

    def play(self):
        self.ui.set_ui_play()
        while True:
            screen.fill((255, 255, 255))
            screen.blit(self.map_bg, (0, 0))

            self.handler.update()

            self.game_sprites.draw(screen)
            self.game_sprites.update()

            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            self.ui.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.OPTION_BUTTON.check_for_input():
                        self.pause()
                    self.audio.shoot.play()
                    self.handler.player.shoot([self.game_sprites, self.arrows])
                if event.type == self.handler.event.enemy_generation_0:
                    self.handler.spawn_enemy(0)
                if event.type == self.handler.event.enemy_generation_1:
                    self.handler.spawn_enemy(1)
                if event.type == self.handler.event.enemy_generation_2:
                    self.handler.spawn_enemy(2)
                if event.type == self.handler.event.enemy_generation_3:
                    self.handler.spawn_enemy(3)
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1:
                        self.victory()
                    if event.key == K_2:
                        self.gameover()
            pygame.display.update()
            FPS_CLOCK.tick(60)

    def pause(self):
        self.ui.set_ui_pause()
        while True:
            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.CONTINUE_BUTTON.check_for_input():
                        self.play()
                    if self.ui.HOME_BUTTON.check_for_input():
                        self.menu()
                    if self.ui.HISTORY_BUTTON.check_for_input():
                        self.history()
                    if self.ui.RESTART_BUTTON.check_for_input():
                        self.handler.set_new_level()
                        self.play()
            pygame.display.update()

    def history(self):
        self.ui.set_ui_history()
        while True:
            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ui.BACK_BUTTON.check_for_input():
                        self.pause()
                    if self.ui.HOME_BUTTON.check_for_input():
                        self.menu()
            pygame.display.update()

    def victory(self):
        screen.blit(self.victory_bg, (0, 0))
        self.ui.set_ui_victory()
        while True:
            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.ui.RESTART_BUTTON.check_for_input():
                        self.handler.set_new_level()
                        self.play()
                    if self.ui.HOME_BUTTON.check_for_input():
                        self.menu()
            pygame.display.update()

    def gameover(self):
        screen.blit(self.game_over_bg, (0, 0))
        self.ui.set_ui_gameover()
        while True:
            self.ui_sprites.draw(screen)
            self.ui_sprites.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.ui.RETRY_BUTTON.check_for_input():
                        self.handler.set_new_level()
                        self.play()
                    if self.ui.HOME_BUTTON.check_for_input():
                        self.menu()
            pygame.display.update()