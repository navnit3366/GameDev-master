import pygame
from Window import window_width, window_height
from Button import Button
from pygame.locals import *
from TextView import TextView
import sys
from execute import selectGame

bg_color = (128, 128, 128)
black = (0, 0, 0)
blue = (0, 50, 255)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 0)

board_width = 500
grid_size = 30

fps = 60
fps_clock = pygame.time.Clock()
is_show = True


def omokGame():
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Omok game")
    surface.fill(white)

    omok = Omok(surface)
    menu = Menu(surface)
    while True:
        run_game(surface, omok, menu)
        menu.is_continue(omok)


def run_game(surface, omok, menu):
    omok.init_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                menu.terminate()
            elif event.type == MOUSEBUTTONUP:
                if not omok.check_board(event.pos):
                    if menu.check_rect(event.pos, omok):
                        omok.init_game()

        back_button = Button(surface, "Back", 20, (255, 255, 255), (window_width - 220, window_height - 7 * 60),
                             (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        back_button.onClickListener(menu.back)
        undo_button = Button(surface, "Undo", 20, (255, 255, 255), (window_width - 220, window_height - 6 * 60),
                             (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        undo_button.onClickListener(omok.undo)
        undoall_button = Button(surface, "Undo All", 20, (255, 255, 255), (window_width - 220, window_height - 5 * 60),
                                (180, 50), (0, 0, 255),
                                (0, 200, 255), 3)
        undoall_button.onClickListener(omok.undo_all)
        redo_button = Button(surface, "Redo", 20, (255, 255, 255), (window_width - 220, window_height - 4 * 60),
                             (180, 50), (0, 0, 255),
                             (0, 200, 255), 3)
        redo_button.onClickListener(omok.redo)
        new_button = Button(surface, "New Game", 20, (255, 255, 255), (window_width - 220, window_height - 3 * 60),
                            (180, 50), (0, 0, 255),
                            (0, 200, 255), 3)
        new_button.onClickListener(omokGame)
        menu.set_omok(omok)
        hide_button = Button(surface, None, 20, (255, 255, 255), (window_width - 220, window_height - 2 * 60),
                             (180, 50),
                             (0, 0, 255),
                             (0, 200, 255), 3)
        # print(is_show)
        if is_show:
            hide_button.setText("Show Number")
        else:
            hide_button.setText("Hide Number")
        menu.set_button(hide_button)
        hide_button.onClickListener(menu.show_hide)
        quit_button = Button(surface, "Quit", 20, (255, 255, 255), (window_width - 220, window_height - 60), (180, 50),
                             (0, 0, 255),
                             (0, 200, 255), 3)
        quit_button.onClickListener(menu.terminate)

        if omok.is_gameover:
            return

        pygame.display.update()
        fps_clock.tick(fps)


class Omok:
    def __init__(self, surface):
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.menu = Menu(surface)
        self.rule = Rule(self.board)
        self.surface = surface
        self.pixel_coords = []
        self.set_coords()
        self.set_image_font()
        self.is_show = None
        self.textview = TextView(self.surface, None, "fonts/ELAND_Choice_M.ttf", 20, None, None)

    def init_game(self):
        self.turn = black_stone
        self.draw_board()
        self.menu.show_msg(empty)
        self.init_board()
        self.coords = []
        self.redos = []
        self.backs = []
        self.id = 1
        self.is_gameover = False

    def set_image_font(self):
        black_img = pygame.image.load('images/omokImages/black.png')
        white_img = pygame.image.load('images/omokImages/white.png')
        self.last_w_img = pygame.image.load('images/omokImages/white_a.png')
        self.last_b_img = pygame.image.load('images/omokImages/black_a.png')
        self.board_img = pygame.image.load('images/omokImages/board.png')
        self.font = pygame.font.Font("fonts/ELAND_Choice_M.ttf", 14)
        self.black_img = pygame.transform.scale(black_img, (grid_size, grid_size))
        self.white_img = pygame.transform.scale(white_img, (grid_size, grid_size))

    def init_board(self):
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] = 0

    def draw_board(self):
        self.surface.blit(self.board_img, (window_width // 6, window_height // 6))

    def draw_image(self, img_index, x, y):
        img = [self.black_img, self.white_img, self.last_b_img, self.last_w_img]
        self.surface.blit(img[img_index], (x, y))

    def show_number(self, x, y, stone, number):
        colors = [white, black, red, red]
        color = colors[stone]
        # print("self.text : ", self.textview.__dict__)
        self.menu.make_text(self.font, str(number), color, None, y + 15, x + 15, 1, textview=self.textview)

    def hide_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.draw_image(i % 2, x, y)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2 + 2, x, y)

    def show_numbers(self):
        for i in range(len(self.coords)):
            x, y = self.coords[i]
            self.show_number(x, y, i % 2, i + 1)
        if self.coords:
            x, y = self.coords[-1]
            self.draw_image(i % 2, x, y)
            self.show_number(x, y, i % 2 + 2, i + 1)

    def draw_stone(self, coord, stone, increase):
        x, y = self.get_point(coord)
        self.board[y][x] = stone
        self.hide_numbers()
        if self.is_show:
            self.show_numbers()
        self.id += increase
        self.turn = 3 - self.turn

    # todo : undo 메서드 제대로 작동 안됨
    def undo(self):
        if not self.coords:
            return
        self.draw_board()
        coord = self.coords.pop()
        self.redos.append(coord)
        self.draw_stone(coord, empty, -1)

    def undo_all(self):
        if not self.coords:
            return
        self.id = 1
        self.turn = black_stone
        while self.coords:
            coord = self.coords.pop()
            self.redos.append(coord)
        self.init_board()
        self.draw_board()

    def redo(self):
        if not self.redos:
            return
        coord = self.redos.pop()
        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)

    def set_coords(self):
        for y in range(board_size):
            for x in range(board_size):
                self.pixel_coords.append((x * grid_size + 25 + window_width // 6, y * grid_size + 25 + window_height // 6))

        print(self.pixel_coords)

    def get_coord(self, pos):
        for coord in self.pixel_coords:
            x, y = coord
            rect = pygame.Rect(x, y, grid_size, grid_size)
            if rect.collidepoint(pos):
                return coord
        return None

    def get_point(self, coord):
        x, y = coord
        x = (x - 25 - window_width // 6) // grid_size
        y = (y - 25 - window_height // 6) // grid_size
        return x, y

    def check_board(self, pos):
        coord = self.get_coord(pos)
        if not coord:
            return False
        x, y = self.get_point(coord)
        print(self.board)
        if self.board[y][x] != empty:
            return True

        self.coords.append(coord)
        self.draw_stone(coord, self.turn, 1)
        if self.check_gameover(coord, 3 - self.turn):
            self.is_gameover = True
        if len(self.redos):
            self.redos = []
        return True

    def check_gameover(self, coord, stone):
        x, y = self.get_point(coord)
        if self.id > board_size * board_size:
            self.show_winner_msg(stone)
            return
        elif 5 <= self.rule.is_gameover(x, y, stone):
            self.show_winner_msg(stone)
            return True
        return False

    def show_winner_msg(self, stone):
        for i in range(3):
            self.menu.show_msg(stone)
            pygame.display.update()
            pygame.time.delay(200)
            self.menu.show_msg(empty)
            pygame.display.update()
            pygame.time.delay(200)
        self.menu.show_msg(stone)


class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.Font('fonts/ELAND_Choice_M.ttf', 20)
        self.surface = surface
        self.draw_menu()
        self.omok = None
        self.button = None

    def draw_menu(self):
        top, left = window_height - 30, window_width - 200
        self.back_rect = self.make_text(self.font, 'Back', blue, None, top - 180, left)
        self.new_rect = self.make_text(self.font, 'New Game', blue, None, top - 30, left)
        self.quit_rect = self.make_text(self.font, 'Quit Game', blue, None, top, left)
        self.show_rect = self.make_text(self.font, 'Hide Number  ', blue, None, top - 60, left)
        self.undo_rect = self.make_text(self.font, 'Undo', blue, None, top - 150, left)
        self.uall_rect = self.make_text(self.font, 'Undo All', blue, None, top - 120, left)
        self.redo_rect = self.make_text(self.font, 'Redo', blue, None, top - 90, left)

    def show_msg(self, msg_id):
        msg = {
            empty: '                                    ',
            black_stone: 'Black win!!!',
            white_stone: 'White win!!!',
            tie: 'Tie',
        }
        center_x = window_width - (window_width - board_width) // 2
        self.make_text(self.font, msg[msg_id], black, white, 130, center_x + 50, 1)

    def make_text(self, font, text, color, bgcolor, top, left, position=0, textview=None):
        if textview is None:
            surf = font.render(text, False, color, bgcolor)
            rect = surf.get_rect()
            # print("rect : ", rect.__class__)
            if position:
                rect.center = (left, top)
            else:
                rect.topleft = (left, top)
            self.surface.blit(surf, rect)
            return rect
        else:
            textview.setText(text)
            textview.setTextColor(color)
            textview.setTextPosition((left, top))
            textview.showText()

    def set_omok(self, omok):
        self.omok = omok

    def set_button(self, button):
        self.button = button

    def show_hide(self, omok=None):
        global is_show
        top, left = window_height - 90, window_width - 200
        # todo : flicking(show/hide 번갈아 표시되는 것) 현상 제거하기
        if omok is None:
            if self.omok.is_show:
                self.omok.is_show = False
                is_show = False
                self.omok.hide_numbers()
            elif not self.omok.is_show:
                self.omok.is_show = True
                is_show = True
                self.omok.show_numbers()
        else:
            if omok.is_show:
                self.make_text(self.font, 'Show Number', blue, bg_color, top, left)
                omok.hide_numbers()
                omok.is_show = False
            else:
                self.make_text(self.font, 'Hide Number  ', blue, bg_color, top, left)
                omok.show_numbers()
                omok.is_show = True

    def check_rect(self, pos, omok):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.show_rect.collidepoint(pos):
            self.show_hide(omok)
        elif self.undo_rect.collidepoint(pos):
            omok.undo()
        elif self.uall_rect.collidepoint(pos):
            omok.undo_all()
        elif self.redo_rect.collidepoint(pos):
            omok.redo()
        elif self.quit_rect.collidepoint(pos):
            self.terminate()
        elif self.back_rect.collidepoint(pos):
            self.back()
        return False

    def back(self):
        selectGame()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def is_continue(self, omok):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == MOUSEBUTTONUP:
                    if self.check_rect(event.pos, omok):
                        return
            pygame.display.update()
            fps_clock.tick(fps)


board_size = 15
empty = 0
black_stone = 1
white_stone = 2
last_b_stone = 3
last_a_stont = 4
tie = 100


class Rule(object):
    def __init__(self, board):
        self.board = board

    def is_invalid(self, x, y):
        return x < 0 or x >= board_size or y < 0 or y >= board_size

    def is_gameover(self, x, y, stone):
        x1, y1 = x, y
        list_dx = [-1, 1, -1, 1, 0, 0, 1, -1]
        list_dy = [0, 0, -1, 1, -1, 1, -1, 1]
        for i in range(0, len(list_dx), 2):
            cnt = 1
            for j in range(i, i + 2):
                dx, dy = list_dx[j], list_dy[j]
                x, y = x1, y1
                while True:
                    x, y = x + dx, y + dy
                    if self.is_invalid(x, y) or self.board[y][x] != stone:
                        break
                    else:
                        cnt += 1
            if cnt >= 5:
                return cnt
        return cnt


if __name__ == "__main__":
    omokGame()

