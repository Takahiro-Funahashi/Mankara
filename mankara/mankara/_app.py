import pygame

from ._board import *  # nopep8
from ._common import game_common  # nopep8
from ._def import *  # nopep8
from ._mankara_basic import *  # nopep8
from ._mankara_easy import *  # nopep8
from ._karaha import *  # nopep8
from ._sunka import *  # nopep8


class Mankara(game_common):
    def __init__(self):
        """ 初期化
        """
        super().__init__()

        self.title_manu = [
            "Mankara Basic",
            "Mankara Easy",
            "Karaha",
            "Sunka",
            "Owari",
            "Exit",
        ]

        return

    def draw_title_menu(self):
        self.logger.debug('draw title')

        W, H = 0, 1
        offset_h = 20
        space = 15
        self.bottm_size = self.screen_size[W]*0.9, 30
        screen = self.game_screen

        self.title_bottom = dict()

        for i, text in enumerate(self.title_manu):
            set_dict = dict()
            sy = offset_h + space*i + self.bottm_size[H]*i
            sx = (self.screen_size[W]-self.bottm_size[W])/2
            w = self.bottm_size[W]
            h = self.bottm_size[H]

            rect = pygame.draw.rect(
                surface=screen,
                color='gray',
                rect=(sx, sy, w, h),
                width=0
            )

            set_dict.setdefault('Rect', rect)

            char = self.game_font.render(text, True, 'black')
            tw, th = self.game_font.size(text)

            tx = sx+(self.bottm_size[W]-tw)/2
            ty = sy+(self.bottm_size[H]-th)/2

            screen.blit(char, [tx, ty])

            set_dict.setdefault('Text', char)

            self.title_bottom.setdefault(text, set_dict)

        return

    def run(self):
        """ タイトル画面の実行ループ
        """

        self.isLoop = True
        self.game_mode = 'title'
        isInit = True
        while(self.isLoop):
            if isInit:
                # GUI画面初期化
                self.init_pygame(title_name="Game Menu", font_size=24)
                # 背景描画
                self.draw_background()

                self.draw_title_menu()
                # GUI描画更新
                pygame.display.update()

                isInit = False

            # GUIイベント処理
            self.event_pygame()

            if self.switch_game_mode():
                isInit = True

        return

    def quit(self):
        pygame.quit()
        self.isLoop = False

        return

    def mouse_left_clicked(self, event):
        if self.title_bottom:
            for key, val in self.title_bottom.items():
                rect = val['Rect']
                if rect:
                    if rect.collidepoint(event.pos):
                        self.game_mode = key
        return

    def switch_game_mode(self):
        mode = self.game_mode
        if mode in self.title_bottom:
            if mode == 'Exit':
                self.quit()
            else:
                pygame.quit()
                if mode == 'Mankara Basic':
                    mankara_basic().run()
                if mode == 'Mankara Easy':
                    mankara_easy().run()
                if mode == 'Karaha':
                    karaha().run()
                if mode == 'Sunka':
                    sunka().run()
                if mode == 'Owari':
                    pass

            self.game_mode = 'title'

            return True

        return False
