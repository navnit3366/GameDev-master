from PIL import Image
import pygame
from pygame.locals import *
from Button import Button
import sys
from execute import selectGame
from Window import window_width, window_height
from Board import Board

# 짝 맞추기 게임(두카드 뒤집기 게임)
# 기본 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
back_img = Image.open('images/twoCardFlipImages/back.png')
card_width = int(back_img.width / 4)
card_height = int(back_img.height / 4)
card_horizontal_gap = 20
card_vertical_gap = 20
board_width = 4
board_height = 4


def initTwoCardFlipGame():
    pygame.init()
    surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("두카드 뒤집기 게임")
    surface.fill(WHITE)

    board = Board(surface, (card_width, card_height), (card_horizontal_gap, card_vertical_gap), (board_width, board_height))
    while True:
        runTwoCardFlipGame(surface, board)


def runTwoCardFlipGame(surface, board):
    pygame.display.set_caption("두카드 뒤집기 게임")
    pygame.display.set_icon(pygame.image.load("images/twoCardFlipImages/back.png"))
    pygame.mixer.init()
    pygame.mixer.music.load("musics/twocardgamemusic.mp3")
    pygame.mixer.music.play(-5, 0.0)
    pygame.mixer.music.set_volume(0.01)

    mouseX = 0
    mouseY = 0  # 마우스 이벤트 발생 좌표

    board.setRandomBoard()
    first_selection = None  # 첫 클릭 좌표 저장
    surface.fill(WHITE)
    board.startGameAnimation()

    while True:  # game loop
        mouseClicked = False

        surface.fill(WHITE)  # draw window
        board.drawBoard()

        again_button = Button(surface, "다시시작", 20, BLACK, (board.surface_width - 140, board.surface_height - 200),
                             (120, 50),
                             (0, 255, 0), (0, 255, 200), 5)
        again_button.onClickListener(initTwoCardFlipGame)
        back_button = Button(surface, "뒤로가기", 20, BLACK, (board.surface_width - 140, board.surface_height - 130),
                            (120, 50),
                            (0, 0, 255), (0, 200, 255), 5)
        back_button.onClickListener(selectGame)
        quit_button = Button(surface, "게임종료", 20, BLACK, (board.surface_width - 140, board.surface_height - 60),
                            (120, 50),
                            (255, 0, 0), (255, 200, 0), 5)
        quit_button.onClickListener(sys.exit)

        for event in pygame.event.get():  # 이벤트 처리 루프
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        boxX, boxY = board.getMousePositionOnBoard(mouseX, mouseY)
        if boxX is not None and boxY is not None:
            # 마우스가 현재 박스 위에 있다.
            if not board.revealed_cards[boxX][boxY]:  # 닫힌 상자라면 하이라이트만
                board.drawHighLightCard(boxX, boxY)
            if not board.revealed_cards[boxX][boxY] and mouseClicked:
                board.revealCardsAnimation([(boxX, boxY)])
                board.revealed_cards[boxX][boxY] = True  # 닫힌 상자 + 클릭 -> 박스 열기
                if first_selection is None:  # 1번 박스 > 좌표 기록
                    first_selection = (boxX, boxY)
                else:  # 1번 박스 아님 > 2번 박스 > 짝 검사
                    icon1shape, icon1color = board.getCardAndNum(first_selection[0], first_selection[1])
                    icon2shape, icon2color = board.getCardAndNum(boxX, boxY)
                    if icon1shape is not icon2shape or icon1color is not icon2color:
                        # 서로 다름이면 둘 다 닫기
                        pygame.time.wait(1000)  # 1초
                        board.coverCardsAnimation([(first_selection[0], first_selection[1]), (boxX, boxY)])
                        board.revealed_cards[first_selection[0]][first_selection[1]] = False
                        board.revealed_cards[boxX][boxY] = False

                    # 다 오픈되었으면
                    elif board.hasWon():
                        board.gameWonAnimation()
                        pygame.time.wait(1000)
                    first_selection = None

                # 화면을 다시 그린 다음 시간 지연을 기다린다...
            pygame.display.update()


if __name__ == "__main__":
    initTwoCardFlipGame()

