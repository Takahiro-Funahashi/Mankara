import numpy as np
import os
import pygame
import random

from ._common import game_common  # nopep8
from ._def import *  # nopep8


class PeaceSprite(pygame.sprite.Sprite):
    def __init__(self, name, pos, num, surface):
        pygame.sprite.Sprite.__init__(self)
        path = os.getcwd() + '/mankara/images/'
        file_name = path+name
        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PEACE_SIZE, PEACE_SIZE))

        width = self.image.get_width()
        height = self.image.get_height()

        self.pos = pos
        x, y = pos
        self.num = num  # [p,n]

        self.rect = pygame.Rect(x, y, width, height)

        surface.blit(self.image, self.rect)

        self.move_x, self.move_y = 0, 0

    def pos_check(self, num=None):
        if num:
            if self.num == num:
                return num

    def update(self, num, pos):
        if pos:
            x, y = pos
            cx, cy = self.pos
            self.move_x, self.move_y = x-cx, y-cy
            self.pos = (x, y)
            self.num = num

        return

    def draw(self, surface):
        if self.rect:
            self.rect.move_ip(self.move_x, self.move_y)
            self.move_x, self.move_y = 0, 0


class PocketSprite(pygame.sprite.Sprite):
    """ ポケットを描画するSpriteクラス
    """

    def __init__(self, is_oval, **kwargs):
        """ 初期化

        Args:
            is_oval (bool): 長方円の場合True、円の場合False
        """

        pygame.sprite.Sprite.__init__(self)

        self.back_color = pygame.Color('peru')
        self.unselect_color = pygame.Color('dimgray')
        self.select_color = pygame.Color('silver')

        self.is_oval = is_oval
        self.number = None

        if self.is_oval:
            # 長方円の場合、辞書型でovalキーでパラメータが渡される
            if "oval" in kwargs:
                self.oval = kwargs['oval']
                if all(
                    [
                        "size" in self.oval,
                        "pos" in self.oval,
                    ]
                ):
                    size = self.oval["size"]
                    pos = self.oval["pos"]
                    w, h = size
                    x, y = pos
                    rect = pygame.Rect(x, y, w, h)
                    # 選択時イメージ
                    self.sel_img = self.draw_oval(rect, self.select_color)
                    # 非選択時イメージ
                    self.unsel_img = self.draw_oval(rect, self.unselect_color)
                if "player" in self.oval:
                    self.player = self.oval["player"]
                if "number" in self.oval:
                    self.number = self.oval["number"]

        else:
            # 円の場合、辞書型でcircleキーでパラメータが渡される
            if "circle" in kwargs:
                self.circle = kwargs['circle']
                if all(
                    [
                        "size" in self.circle,
                        "pos" in self.circle,
                    ]
                ):
                    size = self.circle["size"]
                    pos = self.circle["pos"]
                    w, h = size
                    x, y = pos
                    rect = pygame.Rect(x, y, w, h)
                    # 選択時イメージ
                    self.sel_img = self.draw_circle(rect, self.select_color)
                    # 非選択時イメージ
                    self.unsel_img = self.draw_circle(
                        rect, self.unselect_color)
                if "player" in self.circle:
                    self.player = self.circle["player"]
                if "number" in self.circle:
                    self.number = self.circle["number"]

        self.image = self.unsel_img
        self.rect = rect

    def update(self, player, number_list: list = None):
        """ マウスオーバー時に選択色に変更

        Args:
            player (_type_): _description_
        """

        if number_list is not None:
            if self.number not in number_list:
                return

        if self.player == player:
            pos = pygame.mouse.get_pos()
            hit = self.rect.collidepoint(pos)
            if hit:
                self.image = self.sel_img
            else:
                self.image = self.unsel_img
        else:
            self.image = self.unsel_img

        return

    def draw_oval(self, rect, color):
        """ 長方円の描画

        Args:
            rect (_type_): _description_
            color (_type_): _description_

        Returns:
            _type_: _description_
        """

        img = pygame.Surface(rect.size)
        img.fill(self.back_color)
        # circle
        if 'circle' in self.oval:
            circle = self.oval['circle']
            circle1, circle2 = circle

            if all(
                [
                    "cx" in circle1,
                    "cy" in circle1,
                    "radius" in circle1,
                ]
            ):
                cx = circle1["cx"]
                cy = circle1["cy"]
                radius = circle1["radius"]

                pygame.draw.circle(
                    surface=img,
                    color=color,
                    center=(cx, cy),
                    radius=radius,
                )

            if all(
                [
                    "cx" in circle2,
                    "cy" in circle2,
                    "radius" in circle2,
                ]
            ):
                cx = circle2["cx"]
                cy = circle2["cy"]
                radius = circle2["radius"]

                pygame.draw.circle(
                    surface=img,
                    color=color,
                    center=(cx, cy),
                    radius=radius,
                )
        if 'rect' in self.oval:
            rect = self.oval['rect']
            if all(
                [
                    "sx" in rect,
                    "sy" in rect,
                    "size" in rect,
                ]
            ):
                sx = rect['sx']
                sy = rect['sy']
                w, h = rect['size']
                pygame.draw.rect(
                    surface=img,
                    color=color,
                    rect=pygame.Rect(
                        sx, sy,
                        w, h,
                    ),
                    border_radius=0,
                )

        return img

    def draw_circle(self, rect, color):
        """ 円の描画

        Args:
            rect (_type_): _description_
            color (_type_): _description_

        Returns:
            _type_: _description_
        """

        img = pygame.Surface(rect.size)
        img.fill(self.back_color)
        if 'circle' in self.circle:
            circle = self.circle['circle']

            if all(
                [
                    "cx" in circle,
                    "cy" in circle,
                    "radius" in circle,
                ]
            ):
                cx = circle["cx"]
                cy = circle["cy"]
                radius = circle["radius"]

                pygame.draw.circle(
                    surface=img,
                    color=color,
                    center=(cx, cy),
                    radius=radius,
                )
        return img


class BoardSurface(game_common):
    def __init__(self):
        """ 初期化
        """

        self.help_button = None

        # ボードサイズ
        self.board_size = (1600, 400)
        # 縦横のオフセット幅
        self.screnn_offset = (40, 40)
        # スクリーンサイズをボードサイズとオフセットから計算
        ans = np.array(self.board_size) + (np.array(self.screnn_offset)*2)
        self.screen_size = ans.tolist()

        super().__init__(screen_size=self.screen_size)

        # フォントサイズ
        self.font_size = 24

        self._init_peaces_ = 4

        return

    def _init_board_(self):
        self.player = 0

        self.game_board = np.ones(
            (2, POCKET_NUMBER), dtype=int)*self._init_peaces_
        self.game_board[0][POCKET_NUMBER-1] = 0
        self.game_board[1][POCKET_NUMBER-1] = 0

        self.coords_borad = [
            list(range(POCKET_NUMBER)),
            list(range(POCKET_NUMBER)),
        ]
        self.sprite_object = [
            list(range(POCKET_NUMBER)),
            list(range(POCKET_NUMBER)),
        ]

        self.peaces = list(range(self._init_peaces_*(POCKET_NUMBER-1)*2))

        self.sp_list = list()
        self.sprite_group = pygame.sprite.Group()

        return

    def init_peaces(self):
        for i, _ in enumerate(self.peaces):
            index = random.randint(0, 4)
            if index == 0:
                name = 'blue.gif'
            if index == 1:
                name = 'green.gif'
            if index == 2:
                name = 'orange.gif'
            if index == 3:
                name = 'red.gif'
            if index == 4:
                name = 'yellow.gif'

            p = int(i/(len(self.peaces)/2))
            n = int((i % (len(self.peaces)/2)) % (POCKET_NUMBER-1))
            sx, sy, ex, ey = self.coords_borad[p][n]
            x = random.randrange(sx+PEACE_SIZE*1.5, ex-PEACE_SIZE*1.5, 5)
            y = random.randrange(sy+PEACE_SIZE*1.5, ey-PEACE_SIZE*1.5, 5)

            img = PeaceSprite(name, pos=[x, y], num=[
                              p, n], surface=self.game_screen)
            self.peaces[i] = img

        self.peaces_group = pygame.sprite.Group(self.peaces)

    def draw_board_frame(self):
        """ 盤面枠の描画
        """
        screen = self.game_screen
        offset_x, offset_y = self.screnn_offset
        board_w, board_h = self.board_size

        line_width = 2
        bcolor = 'peru'

        # 盤面背景
        pygame.draw.rect(
            surface=screen,
            color=bcolor,
            rect=pygame.Rect(
                offset_x, offset_y,
                board_w, board_h,
            ),
            border_radius=0,
        )

        # 盤面外枠
        pygame.draw.lines(
            surface=screen,
            color=bcolor,
            closed=True,
            points=[
                (offset_x, offset_y),
                (board_w+offset_x-1, offset_y),
                (board_w+offset_x-1, board_h+offset_y-1),
                (offset_x, board_h+offset_y-1),
            ],
            width=line_width,
        )

        offset = 20

        spos = (offset_x, offset_y)

        for p in range(2):
            w_unit = board_w/(POCKET_NUMBER+1)

            h_unit = board_h/2

            for number in range(POCKET_NUMBER):
                if number == POCKET_NUMBER-1:
                    size = (w_unit, board_h)
                    if p == 0:
                        spos = (offset_x, offset_y)

                        radius = w_unit/2-offset
                        cx = w_unit*1/2
                        cy = h_unit*1/2
                        cood_sy = offset_y+cy-radius

                        circle1 = {
                            "cx": cx,
                            "cy": cy,
                            "radius": radius
                        }

                        cy = h_unit + h_unit*1/2

                        circle2 = {
                            "cx": cx,
                            "cy": cy,
                            "radius": radius
                        }

                        sx = cx-radius
                        w = radius*2
                        cood_sx = offset_x+w_unit*POCKET_NUMBER+sx
                        cood_ex = offset_x+w_unit*POCKET_NUMBER+sx+w

                        sy = board_h/2-h_unit/2
                        h = board_h/2
                        cood_ey = offset_y+sy+h+radius

                        rect = {
                            "sx": sx,
                            "sy": sy,
                            "size": (w, h)
                        }

                        oval = {
                            "size": size,
                            "pos": spos,
                            "circle": [circle1, circle2],
                            "rect": rect,
                            "player": p,
                            "number": number,
                        }

                        sp = PocketSprite(is_oval=True, oval=oval)
                        self.sp_list.append(sp)
                        self.sprite_object[p][number] = sp

                        self.coords_borad[p][number] = \
                            cood_sx, cood_sy, cood_ex, cood_ey

                    elif p == 1:
                        spos = (offset_x + w_unit*POCKET_NUMBER, offset_y)

                        radius = w_unit/2-offset
                        cx = w_unit*1/2
                        cy = h_unit*1/2
                        cood_sy = offset_y+cy-radius

                        circle1 = {
                            "cx": cx,
                            "cy": cy,
                            "radius": radius
                        }

                        cy = h_unit + h_unit*1/2

                        circle2 = {
                            "cx": cx,
                            "cy": cy,
                            "radius": radius
                        }

                        sx = cx-radius
                        w = radius*2
                        cood_sx = offset_x+sx
                        cood_ex = offset_x+sx+w

                        sy = board_h/2-h_unit/2
                        h = board_h/2
                        cood_ey = offset_y+sy+h+radius

                        rect = {
                            "sx": sx,
                            "sy": sy,
                            "size": (w, h)
                        }

                        oval = {
                            "size": size,
                            "pos": spos,
                            "circle": [circle1, circle2],
                            "rect": rect,
                            "player": p,
                            "number": number,
                        }

                        sp = PocketSprite(is_oval=True, oval=oval)
                        self.sp_list.append(sp)
                        self.sprite_object[p][number] = sp

                        self.coords_borad[p][number] = \
                            cood_sx, cood_sy, cood_ex, cood_ey

                else:
                    size = (w_unit, h_unit)

                    if p == 0:
                        pos = number+1
                    elif p == 1:
                        pos = (POCKET_NUMBER-1)-number

                    cx = w_unit*1/2
                    cy = h_unit*1/2
                    pos_x = offset_x+w_unit*(pos)
                    pos_y = offset_y+h_unit*(1-p)
                    spos = (pos_x, pos_y)

                    radius = w_unit/2-offset

                    cood_sx = cx+pos_x-radius
                    cood_sy = cy+pos_y-radius

                    cood_ex = cx+pos_x+radius
                    cood_ey = cy+pos_y+radius

                    circle = {
                        "cx": cx,
                        "cy": cy,
                        "radius": radius,
                    }

                    circle = {
                        "size": size,
                        "pos": spos,
                        "circle": circle,
                        "player": p,
                        "number": number,
                    }

                    sp = PocketSprite(is_oval=False, circle=circle)
                    self.sp_list.append(sp)
                    self.sprite_object[p][number] = sp

                    self.coords_borad[p][number] = \
                        cood_sx, cood_sy, cood_ex, cood_ey

        self.sprite_group.add(self.sp_list)
        self.sprite_group.draw(self.game_screen)

        screen_w, _ = self.screen_size

        rect = pygame.draw.rect(
            surface=self.game_screen,
            color='gray',
            rect=[screen_w-70, 10, 50, 20],
            width=0
        )
        char = self.game_font.render("help", True, 'black')
        self.game_screen.blit(char, [screen_w-60, 10])

        self.help_button = rect

        return

    def pos_check(self, pos):

        x, y = pos

        for p in range(2):
            for n in range(POCKET_NUMBER):
                rect = self.coords_borad[p][n]
                sx, sy, ex, ey = rect
                if all(
                    [
                        x > sx, x < ex, y > sy, y < ey
                    ]
                ):
                    return p, n

    def draw_counter(self):
        bcolor = 'peru'

        for p in range(2):
            for number in range(POCKET_NUMBER):
                cood_sx, cood_sy, cood_ex, cood_ey = \
                    self.coords_borad[p][number]
                peace_number = self.game_board[p][number]

                text = self.game_font.render(
                    str(peace_number),
                    False,
                    'white',
                    bcolor
                )
                self.game_screen.blit(
                    text,
                    [(cood_sx+cood_ex)/2-5, cood_sy-16]
                )
