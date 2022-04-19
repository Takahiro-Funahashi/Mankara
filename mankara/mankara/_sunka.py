import pygame

from ._board import *  # nopep8
from ._common import game_common  # nopep8
from ._def import *  # nopep8


class sunka(BoardSurface):
    def __init__(self):
        super().__init__()

        # self._init_peaces_ = 8
        self.title = "Sunka"
        self.isHelp = False

        self.player = 0

        self._init_board_()

    def _init_game_board_(self):
        self.init_pygame(
            title_name=self.title,
            font_size=self.font_size)

        self.draw_background()
        self.draw_board_frame()
        self.init_peaces()
        self.peaces_group.draw(self.game_screen)

    def run(self):
        self._init_game_board_()

        self.isLoop = True

        while self.isLoop:
            self.draw_counter()
            pygame.display.update()

            if not self.event_pygame():
                self.isLoop = False
                break

            self.sprite_group.update(self.player, list(range(6)))
            self.sprite_group.draw(self.game_screen)
            self.peaces_group.draw(self.game_screen)

            if self.isHelp:
                self.help_screen()

        self.judge()

        pygame.quit()

        return

    def mouse_left_clicked(self, event):
        """ マウス左クリックイベント

        """
        super().mouse_left_clicked(event)
        ret = self.pos_check(event.pos)
        if ret:
            p, n = ret
            self.select_pocket(p, n)

        return

    def select_pocket(self, p, n):
        def _set_coords_(t, num):
            # 対象のポケット及びゴールの座標を取得
            sx, sy, ex, ey = self.coords_borad[t][num]

            x = random.randrange(
                sx+PEACE_SIZE*1.5, ex-PEACE_SIZE*1.5, 5)
            y = random.randrange(
                sy+PEACE_SIZE*1.5, ey-PEACE_SIZE*1.5, 5)

            return x, y

        if self.player == p and n < POCKET_NUMBER-1:

            redraw_peaces_list = list()

            # 石を動かした最後のポジションを記録する
            finish = None

            # turn:陣地
            # number:ポケット(0-5)、ゴール(6)
            turn, number = p, n

            # 指定ポケットの石を動かす石の数とする。
            move_num = self.game_board[p][n]
            if not move_num:
                return

            # 指定ポケットの石を取り出し0にする。
            self.game_board[turn][number] = 0

            # ひとつずつ動かしていく
            for _ in range(move_num):
                # 次のポケットとするためにインクリメント
                number += 1

                finish = (number, turn)

                # ポケット及びゴールの石をひとつずつ置いていく
                self.game_board[turn][number] += 1

                # 対象のポケット及びゴールの座標を取得し、再配置座標を決定
                x, y = _set_coords_(turn, number)

                redraw_peaces_list.append(
                    {
                        "src_num": (p, n),
                        "dst_num": (turn, number),
                        "pos": (x, y),
                    }
                )

                # 次のポケットの判定
                if all(
                    [
                        number == POCKET_NUMBER-1,  # ゴールであるなら
                        turn == p,  # 自陣
                    ]
                ):
                    # 次回は陣地変更
                    number = -1
                    turn = 1 - turn
                elif all(
                    [
                        number == POCKET_NUMBER-2,  # ゴール一歩手前
                        turn != p,  # 相手陣地
                    ]
                ):
                    # 次回は陣地変更
                    number = -1
                    turn = 1 - turn

            # 自陣の石がなくなったら終了
            # ポケットで石置きが終了したら、プレイヤーターン変更
            if finish[0] != POCKET_NUMBER-1:
                num, t = finish
                if self.game_board[t][num] == 1:
                    t_num = POCKET_NUMBER-2-num
                    if self.game_board[1-t][t_num]:
                        get_p0 = self.game_board[t][num]
                        get_p1 = self.game_board[1-t][t_num]
                        self.game_board[t][
                            POCKET_NUMBER - 1] += get_p0 + get_p1

                        self.game_board[t][num] = 0
                        self.game_board[1-t][t_num] = 0

                        for _ in range(get_p0):
                            x, y = _set_coords_(t, POCKET_NUMBER-1)
                            redraw_peaces_list.append(
                                {
                                    "src_num": (t, num),
                                    "dst_num": (t, POCKET_NUMBER-1),
                                    "pos": (x, y),
                                }
                            )

                        for _ in range(get_p1):
                            x, y = _set_coords_(t, POCKET_NUMBER-1)
                            redraw_peaces_list.append(
                                {
                                    "src_num": (1-t, t_num),
                                    "dst_num": (t, POCKET_NUMBER-1),
                                    "pos": (x, y),
                                }
                            )

                self.player = 1 - self.player

            if any(
                [
                    sum(self.game_board[0][:POCKET_NUMBER-1]) == 0,
                    sum(self.game_board[1][:POCKET_NUMBER-1]) == 0,
                ]
            ):
                self.isLoop = False

            self.redraw_peaces(redraw_peaces_list)
        return

    def redraw_peaces(self, redraw_peaces_list):
        if redraw_peaces_list:
            for peace in redraw_peaces_list:
                p, n = peace["src_num"]
                num_p, num_n = peace["dst_num"]
                x, y = peace["pos"]
                for img in self.peaces:
                    ret = img.pos_check([p, n])
                    if ret:
                        img.update([num_p, num_n], [x, y])
                        img.draw(self.game_screen)
                        break

    def click_help_button(self):
        if self.title in game_rule:
            help_text = game_rule[self.title]
            print(help_text)
            self.isHelp = True
        return

    def help_screen(self):
        pygame.quit()
        self.isHelp = False
        pygame.time.wait(2000)
        self._init_board_()
        self._init_game_board_()
        return

    def judge(self):
        screen_w, screen_h = self.screen_size

        msg_w, msg_h = 300, 48

        rect = pygame.draw.rect(
            surface=self.game_screen,
            color='black',
            rect=[screen_w/2-msg_w/2, screen_h/2-msg_h/2, msg_w, msg_h],
            width=0
        )

        p0_num = sum(self.game_board[0])
        p1_num = sum(self.game_board[1])

        if p0_num > p1_num:
            msg = 'Player 0 Win!!'
        if p1_num > p0_num:
            msg = 'Player 1 Win!!'
        if p1_num == p0_num:
            msg = 'Draw!!'

        self.game_font = pygame.font.Font(None, 60)
        char = self.game_font.render(msg, True, 'white')
        self.game_screen.blit(
            char, [screen_w/2-msg_w/2+10, screen_h/2-msg_h/2+5])
        pygame.display.update()
        pygame.time.wait(2000)
