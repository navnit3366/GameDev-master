from tkinter import *
import sys
import pygame
from PIL import Image

from Button import Button
from execute import initTwoCardFlipGame, omokGame, initRandomNumberGame
from Window import window_width, window_height

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)
background_color = WHITE
screen_width = 1024
screen_height = 512

screen_center = window_width / 2, window_height / 3


class Window:
    def __init__(self, window_title, window_size):
        self.window_width, self.window_height = window_size
        self.window_title = window_title
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def __new__(cls, window_title, window_size):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Window, cls).__new__(cls)
            cls.instance.__init__(window_title, window_size)
        return cls.instance

    def setWindowTitle(self, window_title):
        self.window_title = window_title
        pygame.display.set_caption(self.window_title)

    def setWindowSize(self, window_size):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def getWindow(self):
        return self.window

    def fillWindowBackgroundColor(self, window_background_color):
        self.window.fill(window_background_color)


def initGame():
    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    imageString = "images/pygame.png"
    image = Image.open(imageString)
    image_width, image_height = image.size
    image_center = image_width / 2, image_height / 2
    initialImage = pygame.image.load(imageString)
    initialImagePos = screen_center[0] - image_center[0], screen_center[1] - image_center[1]

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill(background_color)

        # 스크린 원하는 좌표에 이미지 찍기
        screen.blit(initialImage, initialImagePos)

        mouse = pygame.mouse.get_pos()

        # 버튼 만들기
        button1_size = 2 * image_width / 5, image_height / 2
        button1_center = window_width / 2 - 3 * image_width / 10, 2 * window_height / 3
        button1_pos = window_width / 2 - 3 * image_width / 10 - image_width / 5, 2 * window_height / 3 - image_height / 4
        button2_size = 2 * image_width / 5, image_height / 2
        button2_center = window_width / 2 + 3 * image_width / 10, 2 * window_height / 3
        button2_pos = window_width / 2 + 3 * image_width / 10 - image_width / 5, 2 * window_height / 3 - image_height / 4

        startButton = Button(screen, "시작하기", 40, BLACK, button1_pos, button1_size, (255, 100, 0), (255, 0, 0))
        startButton.onClickListener(selectGame)
        quitButton = Button(screen, "그만하기", 40, BLACK, button2_pos, button2_size, (0, 255, 100), (0, 255, 200))
        quitButton.onClickListener(sys.exit)

        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


def selectGame():
    # 스크린 기본 설정
    background_color = WHITE
    screen_width = window_width
    screen_height = window_height
    screen_center = window_width / 2, screen_height / 3

    # pygame 초기화
    pygame.init()

    # 스크린 객체 저장
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Game")

    # 게임 시간을 위한 Clock 생성
    clock = pygame.time.Clock()

    playing = True
    while playing:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 스크린 배경색 칠하기
        screen.fill(background_color)

        # 버튼 만들기
        button_size = (200, 80)
        back_button = Button(screen, "뒤로가기", 20, BLACK, (window_width - 140, window_height - 60), (120, 50), (0, 255, 0), (0, 255, 100))
        back_button.onClickListener(initGame)
        two_card_flip_game_button = Button(screen, "두카드 뒤집기 게임", 20, BLACK, (window_width / 2 - button_size[0] / 2, window_height / 4 - button_size[1] / 2), button_size, (255, 255, 0), (255, 255, 200))
        two_card_flip_game_button.onClickListener(initTwoCardFlipGame)
        omok_game_button = Button(screen, "오목 게임", 20, BLACK, (window_width / 2 - button_size[0] / 2, 2 * window_height / 4 - button_size[1] / 2), button_size, (255, 255, 0), (255, 255, 200))
        omok_game_button.onClickListener(omokGame)
        random_number_game_button = Button(screen, "랜덤 숫자 게임", 20, BLACK,
                                  (window_width / 2 - button_size[0] / 2, 3 * window_height / 4 - button_size[1] / 2),
                                  button_size, (255, 255, 0), (255, 255, 200))
        random_number_game_button.onClickListener(initRandomNumberGame)
        # 작업한 내용 갱신하기
        pygame.display.flip()

        # 1초에 60번의 빈도로 순환하기
        clock.tick(60)


if __name__ == "__main__":
    initGame()
