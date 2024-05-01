import pygame

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
        # print("Stage: "  + str(self.stage))
        pygame.time.set_timer(self.enemy_generation, 500 - (20 * self.stage)) 

    # khởi đầu wave 1, stage = 1
    def wave1(self):
        pygame.time.set_timer(self.enemy_generation, 500)