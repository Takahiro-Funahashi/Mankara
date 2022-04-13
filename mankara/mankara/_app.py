import numpy as np
import os
import pygame
import random

POCKET_NUMBER = 7

PEACE_SIZE = 32


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
    def __init__(self, is_oval, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.back_color = pygame.Color('peru')
        self.unselect_color = pygame.Color('dimgray')
        self.select_color = pygame.Color('silver')

        self.is_oval = is_oval

        if self.is_oval:
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
                    self.sel_img = self.draw_oval(rect, self.select_color)
                    self.unsel_img = self.draw_oval(rect, self.unselect_color)
                if "player" in self.oval:
                    self.player = self.oval["player"]

        else:
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
                    self.sel_img = self.draw_circle(rect, self.select_color)
                    self.unsel_img = self.draw_circle(
                        rect, self.unselect_color)
                if "player" in self.circle:
                    self.player = self.circle["player"]

        self.image = self.unsel_img
        self.rect = rect

    def update(self, events, player):
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


class BoardSurface():
    def __init__(self):
        """ 初期化
        """

        # ボードサイズ
        self.board_size = (1600, 400)
        # 縦横のオフセット幅
        self.screnn_offset = (40, 40)
        # スクリーンサイズをボードサイズとオフセットから計算
        ans = np.array(self.board_size) + (np.array(self.screnn_offset)*2)
        self.screen_size = ans.tolist()

        # フォントサイズ
        self.font_size = 24

        self._init_board_()

        return

    def _init_board_(self):
        self.player = 0

        _init_peaces_ = 4

        self.game_board = np.ones((2, POCKET_NUMBER), dtype=int)*_init_peaces_
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

        self.peaces = list(range(_init_peaces_*(POCKET_NUMBER-1)*2))

        self.sp_list = list()
        self.sprite_group = pygame.sprite.Group()

        return

    def init_pygame(self):
        """ PyGame(GUI)初期化
        """

        pygame.init()
        self.game_screen = pygame.display.set_mode(
            size=self.screen_size,
            # flags=pygame.FULLSCREEN,
        )
        pygame.display.set_caption('Mankara')

        self.game_font = pygame.font.Font(
            None, self.font_size)

        return

    def draw_background(self):
        """ 背景描画
        """

        self.game_screen.fill('silver')

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
                    }

                    sp = PocketSprite(is_oval=False, circle=circle)
                    self.sp_list.append(sp)
                    self.sprite_object[p][number] = sp

                    self.coords_borad[p][number] = \
                        cood_sx, cood_sy, cood_ex, cood_ey

        self.sprite_group.add(self.sp_list)
        self.sprite_group.draw(self.game_screen)

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


class MankaraGame(BoardSurface):
    def __init__(self):
        super().__init__()

    def run(self):
        self.init_pygame()

        self.draw_background()
        self.draw_board_frame()

        self.init_peaces()
        self.peaces_group.draw(self.game_screen)

        isLoop = True

        while isLoop:

            if self.player == 0:

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        isLoop = False
                        break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.mouse_left_clicked(event.pos):
                            isLoop = False
                            break

                if not isLoop:
                    break

                self.sprite_group.update(events, self.player)
            else:
                n = random.randint(0, 5)
                if not self.select_pocket(self.player, n):
                    isLoop = False
                    break

            self.sprite_group.draw(self.game_screen)
            self.peaces_group.draw(self.game_screen)

            pygame.display.update()

        p0_num = sum(self.game_board[0])
        p1_num = sum(self.game_board[1])

        if p0_num == p1_num:
            print('Draw!!')
        if p0_num > p1_num:
            print('Player 0 Win!!')
        if p0_num < p1_num:
            print('Player 1 Win!!')

        pygame.quit()

        return

    def mouse_left_clicked(self, pos: list):
        """ マウス左クリックイベント

        Args:
            pos (list): マウスクリック座標(x,y)
        """
        ret = self.pos_check(pos)
        if ret:
            p, n = ret
            return self.select_pocket(p, n)

        return True

    def select_pocket(self, p, n):
        if self.player == p and n < POCKET_NUMBER-1:
            move_num = self.game_board[p][n]

            coords_list = list()

            turn, number = p, n
            self.game_board[turn][number] = 0
            for _ in range(move_num):
                number += 1
                if number == POCKET_NUMBER-1:
                    sx, sy, ex, ey = self.coords_borad[turn][number]
                    if turn != self.player:
                        number = 0
                        turn = 1 - turn
                elif number > POCKET_NUMBER-1:
                    number = 0
                    turn = 1 - turn
                    sx, sy, ex, ey = self.coords_borad[turn][number]
                else:
                    sx, sy, ex, ey = self.coords_borad[turn][number]
                self.game_board[turn][number] += 1
                x = random.randrange(
                    sx+PEACE_SIZE*1.5, ex-PEACE_SIZE*1.5, 5)
                y = random.randrange(
                    sy+PEACE_SIZE*1.5, ey-PEACE_SIZE*1.5, 5)
                coords_list.append([turn, number, x, y])

            if not coords_list:
                return True

            it_coords = iter(coords_list)

            for i, img in enumerate(self.peaces):
                ret = img.pos_check([p, n])
                if ret:
                    num_p, num_n, x, y = next(it_coords)
                    img.update([num_p, num_n], [x, y])
                    img.draw(self.game_screen)

            if sum(self.game_board[self.player][:POCKET_NUMBER-1]) == 0:
                return False
            else:
                if any(
                    [
                        number != POCKET_NUMBER-1,
                        turn != self.player
                    ]
                ):
                    self.player = 1 - self.player

        return True

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


MankaraGame().run()
