import pygame
from settings import *
from preset import Preset

# khởi tạo các button, text, label của mỗi màn hình.
class UI():
    def __init__(self, game):
        self.game = game
        self.game_window = pygame.image.load("resources/images/game_window.png").convert_alpha()
        self.option_button = pygame.image.load("resources/images/option_button.png").convert_alpha()
        self.score_label = pygame.image.load("resources/images/score_label.png").convert_alpha()
        self.level_label = pygame.image.load("resources/images/level_label.png").convert_alpha()
        self.previous_button = pygame.image.load("resources/images/previous_button.png").convert_alpha()

    def set_ui_menu(self):
        self.game.ui_sprites.empty()
        TextRender([320, 50], Text("MAIN MENU", Font.f1, FontSize.h7, Color.primary), [self.game.ui_sprites])
        self.PLAY_BUTTON = Button([320, 150], [180, 70], None, Text("PLAY", Font.f1, FontSize.h2, Color.white, Color.green), [self.game.ui_sprites])
        self.QUIT_BUTTON = Button([320, 250], [180, 70], None, Text("QUIT", Font.f1, FontSize.h2, Color.white, Color.green), [self.game.ui_sprites])

    def set_ui_level(self):
        self.game.ui_sprites.empty()
        Label([320, 240], [320, 145], [250, 250], self.game_window, Text("LEVEL", Font.f1, FontSize.h2, Color.red), [self.game.ui_sprites])
        self.LV1_BUTTON = Button([320, 200], [100, 40], None, Text("Level1", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.LV2_BUTTON = Button([320, 250], [100, 40], None, Text("Level2", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.LV3_BUTTON = Button([320, 300], [100, 40], None, Text("Level3", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.PREVIOUS_BUTTON = Button([40, 450], [45, 25], self.previous_button, None, [self.game.ui_sprites])

    def set_ui_play(self):
        self.game.ui_sprites.empty()
        self.SCORE_LABEL = Label([500, 30], [500, 30], [160, 50], self.score_label, Text("SCORE:0", Font.f1, FontSize.h0, Color.white), [self.game.ui_sprites])
        self.OPTION_BUTTON = Button([610, 25], [40, 40], self.option_button, None, [self.game.ui_sprites])
        self.healthbar = HealthBar([self.game.ui_sprites])
        self.healthbar.set_health([self.game.ui_sprites, self.game.hp])
        Label([55, 45], [55, 45], [100, 35], self.level_label, Text(str(Preset.level[self.game.index].caption), Font.f1, FontSize.h0, Color.white), [self.game.ui_sprites])
        

    def set_ui_pause(self):
        self.game.ui_sprites.empty()
        Label([320, 240], [320, 120], [250, 310], self.game_window, Text("PAUSE", Font.f1, FontSize.h2, Color.red), [self.game.ui_sprites])
        self.CONTINUE_BUTTON = Button([320, 200], [120, 40], None, Text("CONTINUE", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.RESTART_BUTTON = Button([320, 250], [120, 40], None, Text("RESTART", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.HISTORY_BUTTON = Button([320, 300], [120, 40], None, Text("HISTORY", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.HOME_BUTTON = Button([320, 350], [120, 40], None, Text("HOME", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])

    def set_ui_history(self):
        self.game.ui_sprites.empty()
        Label([320, 240], [320, 120], [250, 310], self.game_window, Text("HISTORY", Font.f1, FontSize.h1, Color.red), [self.game.ui_sprites])
        TextRender([320, 200], Text("Level1:" + str(self.game.handler.highscores[0]), Font.f1, FontSize.h0, Color.black), [self.game.ui_sprites])
        TextRender([320, 250], Text("Level2:" + str(self.game.handler.highscores[1]), Font.f1, FontSize.h0, Color.black), [self.game.ui_sprites])
        TextRender([320, 300], Text("Level3:" + str(self.game.handler.highscores[2]), Font.f1, FontSize.h0, Color.black), [self.game.ui_sprites])
        self.BACK_BUTTON = Button([270, 350], [80, 35], None, Text("BACK", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.HOME_BUTTON = Button([370, 350], [80, 35], None, Text("HOME", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])

    def set_ui_victory(self):
        self.game.ui_sprites.empty()
        TextRender([320, 290], Text("HighScore:" + str(self.game.handler.highscores[self.game.index]), Font.f1, FontSize.h1, Color.white), [self.game.ui_sprites])
        TextRender([320, 320], Text("Score:" + str(self.game.handler.score), Font.f1, FontSize.h1, Color.white), [self.game.ui_sprites])
        self.RESTART_BUTTON = Button([220, 400], [150, 55], None, Text("RESTART", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.HOME_BUTTON = Button([420, 400], [150, 55], None, Text("HOME", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])

    def set_ui_gameover(self):
        self.game.ui_sprites.empty()
        TextRender([320, 290], Text("HighScore:" + str(self.game.handler.highscores[self.game.index]), Font.f1, FontSize.h1, Color.white), [self.game.ui_sprites])
        TextRender([320, 320], Text("Score:" + str(self.game.handler.score), Font.f1, FontSize.h1, Color.white), [self.game.ui_sprites])
        self.RETRY_BUTTON = Button([220, 400], [150, 55], None, Text("RETRY", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])
        self.HOME_BUTTON = Button([420, 400], [150, 55], None, Text("HOME", Font.f1, FontSize.h0, Color.white, Color.green), [self.game.ui_sprites])

    def update(self):
        text = Text("SCORE:" + str(self.game.handler.score), Font.f1, FontSize.h0, Color.white)
        self.SCORE_LABEL.change_text(text, [[self.game.ui_sprites]])
        

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, scale, image=None, text=None, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load("resources/images/button.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, scale).convert_alpha()
        if image is not None:
            self.image = pygame.transform.scale(image, scale).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.mouse_pos = [0, 0]
        self.text_render = None
        if text is not None:
            self.base_color, self.hovering_color = text.base_color, text.hovering_color
            self.text_render = TextRender(self.rect.center, text, *groups)

    def check_for_input(self):
        if self.mouse_pos[0] in range(self.rect.left, self.rect.right) and self.mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self):
        if self.mouse_pos[0] in range(self.rect.left, self.rect.right) and self.mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            self.text_render.change_color(self.hovering_color)
        else:
            self.text_render.change_color(self.base_color)
    
    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        if self.text_render is not None:
            self.change_color()

class Label(pygame.sprite.Sprite):
    def __init__(self, pos, text_pos, scale, image=None, text=None, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(image, scale).convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.text_pos, self.text = text_pos, text
        self.text_render = TextRender(self.text_pos, self.text, *groups)

    def change_text(self, text, *groups):
        self.text_render.kill()
        self.text_render = TextRender(self.text_pos, text, *groups)

class TextRender(pygame.sprite.Sprite):
    def __init__(self, pos, text,*groups):
        super().__init__(*groups)
        self.content, self.font, self.fontsize, self.base_color = text.content, text.font, text.fontsize, text.base_color
        self.text_render = pygame.font.Font(self.font, self.fontsize).render(self.content, True, self.base_color)
        self.image = self.text_render
        self.rect = self.image.get_rect(center=pos)
    
    def change_color(self, color):
        self.text_render = pygame.font.Font(self.font, self.fontsize).render(self.content, True, color)
        self.image = self.text_render

class Text():
    def __init__(self, content=None, font=Font.f1, fontsize=FontSize.h0, base_color=Color.white, hovering_color=Color.green):
        self.content = content
        self.font = font
        self.fontsize = fontsize
        self.base_color, self.hovering_color = base_color, hovering_color

# khởi tạo và vẽ thanh HP
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("resources/images/healthbar.png").convert_alpha()
        self.rect = self.image.get_rect(center=(110, 15))
        self.healthvalue = Preset.hp_castle

    def set_health(self, *groups):
        for value in range(self.healthvalue):
            Health([value + 12, 15], *groups)
            
class Health(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("resources/images/health.png").convert_alpha()
        self.rect = self.image.get_rect(center=(pos))
