import sys
import pygame
import math
from pygame.locals import *
from Window import window_width, window_height, window_center_x, window_center_y
from ImageView import resizeImage
from Button import Button
from EditText import EditText
import random
from TextView import TextView
from execute import selectGame

BRIGHTBLUE = (0, 50, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = WHITE

# 초당 프레임 수 : 많을 수록 빠르다
# FRAME PER SECOND
FPS = 120
AMPLITUDE = 30
# 기본 시작 셋업
surface = pygame.display.set_mode((window_width, window_height))

bag = pygame.image.load("images/randomNumberImages/bag_186x218.png")
bag_width, bag_height = bag.get_size()
bag_update_string = resizeImage("images/randomNumberImages", "bag", int(bag_width * 1.5), int(bag_height * 1.5), 1)
bag = pygame.image.load(bag_update_string)
bag_width, bag_height = bag.get_size()
bag_pos_x = int(window_width / 3)
bag_pos_y = int(window_height / 8)

marvel = pygame.image.load("images/randomNumberImages/marvel.png")
marvel_width, marvel_height = marvel.get_size()
marvel_update_string = resizeImage("images/randomNumberImages", "marvel", int(marvel_width / 3), int(marvel_height / 3),
                                   1)
marvel = pygame.image.load(marvel_update_string)
marvel_width, marvel_height = marvel.get_size()

marvel_start_point = (int(bag_pos_x + bag_width / 2), int(bag_pos_y))
marvel_end_point = (int(window_width / 5), 2000)
show_marvel = False

# edittext

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('orange')


class Transfer:
    def __init__(self):
        self.value = 0

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

class RandomNumberBoard:
    def __init__(self):
        pass

def marvelAnimation():
    global latest_marvel_pos_x, latest_marvel_pos_y
    surface.fill(BGCOLOR)
    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
    for x in range(marvel_start_point[0], marvel_end_point[0], -1):
        surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
        a = 4
        a1 = int(
            (marvel_end_point[1] - marvel_start_point[1]) / (marvel_end_point[0] ** 2 - marvel_start_point[0] ** 2))
        b = 440
        c = marvel_start_point[1] - (marvel_start_point[0] ** 2) * a1
        y = int(a * ((x - b) ** 2) + c)
        y /= window_height
        surface.fill(BGCOLOR)
        showBag()
        surface.blit(marvel, (x, y))
        latest_marvel_pos_x, latest_marvel_pos_y = x, y
        pygame.display.update()
    randomizeNumber()


def showMarvel():
    global latest_marvel_pos_x, latest_marvel_pos_y
    surface.blit(marvel, (latest_marvel_pos_x, latest_marvel_pos_y))


def showBag():
    surface.blit(bag, (int(window_width / 3), int(window_height / 8)))


def mixAnimation():
    for step in range(360):
        surface.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        yPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        surface.blit(bag, (bag_pos_x, int(yPos) + bag_pos_y))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()
    for step in range(360):
        surface.fill(BGCOLOR)
        # 움직이는 공을 그립니다. math.sin()
        xPos = -1 * math.sin(7 * step * math.pi / 180) * AMPLITUDE
        # 푸른색 공을 그려줍니다.
        surface.blit(bag, (int(xPos) + bag_pos_x, bag_pos_y))
        # 디스플레이 업데이트 해준다.
        pygame.display.update()
    edittext.resetInputText()


edittext = EditText(surface, 32, (0, 0, 0), color_passive, color_active, (300, 50),
                    (int((bag_pos_x + bag_width) / 2) - 20, bag_pos_y + bag_height + 50))
number = 0
check_text = TextView(surface, "", text_size=30, text_color=(0, 0, 0),
                      text_position=(int(6 * window_width / 7), int(window_height / 6)))
typed_number = edittext.input_text

transfer = Transfer()


def check():
    global number, check_text, typed_number
    print("number :", number)

    typed_number = transfer.getValue()
    print("edittext.input_text :", edittext.input_text)
    print("typed_number :", typed_number)
    if type(int(typed_number)) == int:
        print("here", typed_number)
        if int(typed_number) == 0:
            zero_text = TextView(surface, "숫자를 입력하세요!", text_size=30, text_color=(0, 0, 0),
                                 text_position=(int(6 * window_width / 7), int(window_height / 6)))
            check_text = zero_text
        if int(typed_number) == number:
            correct_text = TextView(surface, "정답입니다!", text_size=30, text_color=(0, 0, 0),
                                    text_position=(int(6 * window_width / 7), int(window_height / 6)))
            check_text = correct_text
        elif int(typed_number) > number:
            down_text = TextView(surface, "그보다 아래입니다!", text_size=30, text_color=(0, 0, 0),
                                 text_position=(int(6 * window_width / 7), int(window_height / 6)))
            check_text = down_text
        elif int(typed_number) < number:
            up_text = TextView(surface, "그보다 위입니다!", text_size=30, text_color=(0, 0, 0),
                               text_position=(int(6 * window_width / 7), int(window_height / 6)))
            check_text = up_text


def randomizeNumber():
    global number
    number = random.randint(1, 100)


def initRandomNumberGame():
    pygame.init()
    pygame.display.set_caption("랜덤 숫자 게임")
    surface.fill(pygame.Color("white"))
    while True:
        randomNumberGame()


def randomNumberGame():
    # 메인 루프
    global show_marvel
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            edittext.initEditText(event)


        # 배경을 칠합니다.
        surface.fill(BGCOLOR)

        surface.blit(bag, (int(window_width / 3), int(window_height / 8)))
        mix_button = Button(surface, "숫자 구슬 섞기", 20, (0, 0, 0), (50, int(window_height / 7)), (200, 60), (0, 255, 0),
                            (0, 255, 100), 4)
        mix_button.onClickListener(mixAnimation)
        if mix_button.isButtonClicked():
            show_marvel = False
        show_marvel_button = Button(surface, "구슬 꺼내기", 20, (0, 0, 0), (50, 2 * int(window_height / 7) + 20), (200, 60),
                                    (0, 255, 0), (0, 255, 100), 4)
        show_marvel_button.onClickListener(marvelAnimation)
        show_marvel_button.onClickListener(check)
        if show_marvel_button.isButtonClicked():
            show_marvel = True
        if show_marvel:
            showMarvel()
        surface.blit(bag, (int(window_width / 3), int(window_height / 8)))

        edittext.updateTextBoxColor()
        edittext.showEditTextBox()
        edittext.text_box_rect.w = max(100, edittext.text_render.get_width() + 10)

        typed_number = int(float(edittext.input_text))
        transfer.setValue(typed_number)
        check_button = Button(surface, "확인", 20, (0, 0, 0),
                              (edittext.text_box_rect.x + edittext.text_box_rect.size[0], edittext.text_box_rect.y),
                              (100, edittext.text_box_rect.size[1] + 1), color_passive, color_active)
        check_button.onClickListener(check)
        check_text.showText()

        back_button = Button(surface, "뒤로가기", 20, BLACK, (window_width - 140, window_height - 130),
                             (120, 50),
                             (0, 0, 255), (0, 200, 255), 5)
        back_button.onClickListener(selectGame)
        quit_button = Button(surface, "게임종료", 20, BLACK, (window_width - 140, window_height - 60),
                             (120, 50),
                             (255, 0, 0), (255, 200, 0), 5)
        quit_button.onClickListener(sys.exit)

        pygame.display.update()


