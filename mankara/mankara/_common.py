import os
import pygame
from ._log import get_logger  # nopep8


class game_common():
    def __init__(
        self,
        screen_size=(300, 400),
        log_path: str = os.getcwd() + "/logs/log_game.log",
        log_level: str = "INFO"
    ):
        self.logger = get_logger(
            log_path=log_path,
            log_level=log_level
        )

        self.screen_size = screen_size

        self.help_button = None

        return

    def init_pygame(self, title_name, font_size):
        """ PyGame(GUI)初期化
        """
        self.font_size = font_size

        pygame.init()
        self.game_screen = pygame.display.set_mode(
            size=self.screen_size,
            # flags=pygame.FULLSCREEN,
        )
        pygame.display.set_caption(title_name)

        self.game_font = pygame.font.Font(
            None, self.font_size)

        return

    def draw_background(self, color='darkgreen'):
        """ 背景描画
        """

        self.game_screen.fill(color)
        return

    def event_pygame(self):
        isRet = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                isRet = False
                break
            # マウスボタンクリック
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 左ボタンクリック
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_left_clicked(event)
                # 右ボタンクリック
                elif event.button == pygame.BUTTON_RIGHT:
                    self.mouse_right_clicked(event)
            # マウスボタンリリース
            if event.type == pygame.MOUSEBUTTONUP:
                # 左ボタンリリース
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_left_release(event)
                # 右ボタンリリース
                elif event.button == pygame.BUTTON_RIGHT:
                    self.mouse_right_release(event)
            # マウスモーション
            if event.type == pygame.MOUSEMOTION:
                self.mouse_move_on(event)
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_wheel(event)
        return isRet

    def quit(self):
        pygame.quit()

    def mouse_left_clicked(self, event):
        x, y = event.pos
        if self.help_button:
            rect = self.help_button
            if rect:
                if rect.collidepoint(event.pos):
                    self.click_help_button()
        return

    def mouse_right_clicked(self, event):
        x, y = event.pos
        return

    def mouse_left_release(self, event):
        x, y = event.pos
        return

    def mouse_right_release(self, event):
        x, y = event.pos
        return

    def mouse_move_on(self, event):
        x, y = event.pos
        return

    def mouse_wheel(self, event):
        print('wheel:', event.x, event.y)
        return

    def click_help_button(self):
        return
