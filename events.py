import pygame, random
from player import Player
from enemy import * 
from castle import *
from preset import *

class GameHandler():
    def __init__(self, game):
        self.game = game
        self.castle = Castle([self.game.game_sprites])
        self.player = Player([self.game.game_sprites])
        self.event = Event()
        self.score = 0
        self.highscores = [0, 0, 0]

    # hàm khởi tạo khi mới bắt đầu một level
    def set_new_level(self):
        self.game.game_sprites.empty()
        self.game.enemies.empty()
        self.game.arrows.empty()
        self.game.hp.empty()

        self.castle = Castle([self.game.game_sprites])
        self.player = Player([self.game.game_sprites])
        self.event = Event()
        self.event.set_event(self.game.index)
        self.score = 0

    # hàm tạo enemy với mỗi đường
    def spawn_enemy(self, index):
            if self.event.enemy_count[index] < self.event.stage_enemies[self.event.stage - 1][index]:
                self.event.choice_number(index)
                value = bool(random.randint(0, 1))
                if value:
                    Bogey(self.event.enemy_pos[index], Preset.enemy_target[index], self.event.speed[self.event.stage - 1], Preset.diagonal_movement[index], [self.game.game_sprites, self.game.enemies])
                else:
                    Snail(self.event.enemy_pos[index], Preset.enemy_target[index], self.event.speed[self.event.stage - 1], Preset.diagonal_movement[index], [self.game.game_sprites, self.game.enemies])
                self.event.enemy_count[index] += 1
            else: 
                self.event.stage_state[index] = True

    # hàm update các sự kiện trong game
    def update(self):
        # kiểm tra xem hp của castle có = 0 không nếu = 0 thì game over
        if self.castle.hp == 0:
            if self.score > self.highscores[self.game.index]:
                self.highscores[self.game.index] = self.score
            self.game.gameover()
        
        # kiểm tra xem là đã spawn hết enemy ở mỗi đường chưa và đã hết enemy trên map chưa
        # nếu hết rùi thì kiểm tra xem là đã là stage cuối chưa, nếu cuối thì cho victory
        if all(self.event.stage_state) and self.game.enemies.__len__() == 0:
            if self.event.stage < self.event.stage_enemies.__len__():
                self.event.next_stage()
            elif self.event.stage == self.event.stage_enemies.__len__():
                if self.score > self.highscores[self.game.index]:
                    self.highscores[self.game.index] = self.score
                self.game.victory()

        # kiểm tra và xử lý khi tên bắn vô enemy
        for sprite in self.game.enemies.sprites():
            hits = pygame.sprite.spritecollide(sprite ,self.game.arrows, True)
            for hit in hits:
                self.game.audio.enemy_damaged.play()
                sprite.hp -= 1
                if sprite.hp == 0:
                    sprite.kill()
                    self.score += 1

        # kiểm tra và xử lý khi enemy tấn công castle
        hits = pygame.sprite.spritecollide(self.castle, self.game.enemies, True)
        for hit in hits:
            self.game.audio.castle_damaged.play()
            if self.castle.hp > 0:
                damaged = random.randint(3, 5)
                if damaged >= self.castle.hp:
                    damaged = self.castle.hp
                self.castle.hp -= damaged
                for i in range(damaged):
                    self.game.hp.sprites()[-1].kill()

class Event():
    # hàm khởi tạo của sự kiện.
    def __init__(self):
        self.enemy_count = [0, 0, 0, 0]
        self.number = 0
        self.enemy_pos = []
        self.speed = []
        self.stage_state = [False, False, False, False]
        self.stage_enemies = []

        # Khởi tạo sự kiển tạo enemy ở cái đường
        self.enemy_generation_0 = pygame.USEREVENT + 1
        self.enemy_generation_1 = pygame.USEREVENT + 2
        self.enemy_generation_2 = pygame.USEREVENT + 3
        self.enemy_generation_3 = pygame.USEREVENT + 4
        
        self.stage = 1

    # random vị trí của enemy ở mỗi đường.
    def choice_number(self, index):
        self.number = random.choice(Preset.number_random[index])
        self.enemy_pos = [
            [self.number, 16],
            [624, self.number],
            [624, self.number],
            [self.number, 464]
        ]

    # chuyển sang stage tiếp theo, gán bộ đếm enemy = 0, setup lại thời gian của timer sự kiện enemy_generation
    def next_stage(self):
        self.stage += 1
        self.stage_state = [False, False, False, False]
        self.enemy_count = [0, 0, 0, 0]
        pygame.time.set_timer(self.enemy_generation_0, 800 - (20 * self.stage))
        pygame.time.set_timer(self.enemy_generation_1, 810 - (20 * self.stage))
        pygame.time.set_timer(self.enemy_generation_2, 820 - (20 * self.stage))
        pygame.time.set_timer(self.enemy_generation_3, 830 - (20 * self.stage)) 

    # khởi tạo các đối số cho sự kiện tạo enemy
    # stage_enemies là số lượng quái mỗi đường với mỗi stage
    # speed là tốc độ của enemy ở mỗi stage
    def set_event(self, index):
        self.stage_enemies = Preset.level[index].stage_enemies
        self.speed = Preset.level[index].speed
        pygame.time.set_timer(self.enemy_generation_0, 800)
        pygame.time.set_timer(self.enemy_generation_1, 810)
        pygame.time.set_timer(self.enemy_generation_2, 820)
        pygame.time.set_timer(self.enemy_generation_3, 830)