import pygame
from ImageView import resizeImage
import random, sys
from TextView import TextView
from Button import Button
from execute import selectGame, initTwoCardFlipGame

BOXSIZE = 60
REVEALSPEED = 8
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Board:
    def __init__(self, surface: pygame.Surface, card_size: tuple, card_gap: tuple, board_size: tuple):
        self.surface = surface
        self.surface_width, self.surface_height = self.surface.get_size()
        self.card_width, self.card_height = card_size
        self.card_horizontal_gap, self.card_vertical_gap = card_gap
        self.board_width, self.board_height = board_size
        self.cards = self.setCards()
        self.board = self.getRandomBoard()
        self.x_margin = int((self.surface_width - (self.board_width * (self.card_width + self.card_horizontal_gap))) / 2)
        self.y_margin = int((self.surface_height - (self.board_height * (self.card_height + self.card_vertical_gap))) / 2)
        self.revealed_cards = []

    @staticmethod
    def setCards():
        cards = []
        for s in ['clover', 'dia', 'heart', 'spaid']:
            for n in range(1, 11):
                cards.append(s + str(n))
        return cards

    # 문제없음
    def resizeImageAll(self, name):
        for n in range(1, 11):
            resizeImage('images/twoCardFlipImages', f'{name}_{n}', self.card_width, self.card_height)

    # 문제없음
    # 그림 카드 만들기
    def makeCards(self, name):
        img = [None]
        for n in range(1, 11):
            img.append(
                pygame.image.load(f'images/twoCardFlipImages/{name}_{n}_{self.card_width}x{self.card_height}.png'))
        return img

    # 문제없음
    def showCards(self, image_list, pic, name, left, top):
        for n in range(1, 11):
            if pic == name + str(n):
                self.surface.blit(image_list[n], (left, top))

    # 문제없음
    def drawCard(self, card, card_x, card_y):
        left, top = self.getCardPosition(card_x, card_y)  # 보드 좌표에서 픽셀 좌표 구하기

        self.resizeImageAll('clover')
        self.resizeImageAll('dia')
        self.resizeImageAll('heart')
        self.resizeImageAll('spaid')

        cloverImg = self.makeCards('clover')
        diaImg = self.makeCards('dia')
        heartImg = self.makeCards('heart')
        spaidImg = self.makeCards('spaid')

        self.showCards(cloverImg, card, 'clover', left, top)
        self.showCards(diaImg, card, 'dia', left, top)
        self.showCards(heartImg, card, 'heart', left, top)
        self.showCards(spaidImg, card, 'spaid', left, top)

    # 문제없음
    def getCardPosition(self, boxX, boxY):
        # 좌표를 픽셀 좌표로 변환
        left = boxX * (self.card_width + self.card_horizontal_gap) + self.x_margin
        top = boxY * (self.card_height + self.card_vertical_gap) + self.y_margin
        return left, top

    # 문제없음
    def getCardAndNum(self, card_x, card_y):
        # 아이콘 값은 board[x][y][0] 에 있다.
        # 색깔 값은 board[x][y][1]에 있다.
        return self.board[card_x][card_y][0], self.board[card_x][card_y][1]

    # 문제 없음
    def drawBoard(self):
        for boxX in range(self.board_width):
            for boxY in range(self.board_height):
                left, top = self.getCardPosition(boxX, boxY)
                if not self.revealed_cards[boxX][boxY]:
                    # 닫힌 상자를 만든다.
                    resizeImage('images/twoCardFlipImages', 'back', self.card_width, self.card_height)
                    back_of_card = pygame.image.load(
                        f'images/twoCardFlipImages/back_{self.card_width}x{self.card_height}.png')
                    back_of_card_rect = back_of_card.get_rect()
                    back_of_card_rect.center = left + self.card_width // 2, top + self.card_height // 2
                    self.surface.blit(back_of_card, back_of_card_rect)
                    pygame.draw.rect(self.surface, (255, 255, 255), back_of_card_rect, 1)
                else:
                    # 열린 상자
                    card, num = self.getCardAndNum(boxX, boxY)
                    self.drawCard(card, boxX, boxY)

    # 문제없음
    def drawCardCovers(self, boxes, coverage):
        global FPSCLOCK
        # 닫히겨나 열린 상태의 상자를 그린다.
        # 상자는 요소 2개를 가진 리스트이며 xy 위치를 가진다.
        for box in boxes:
            left, top = self.getCardPosition(box[0], box[1])
            pygame.draw.rect(self.surface, (255, 255, 255), (left, top, self.card_width, self.card_height))
            card, num = self.getCardAndNum(box[0], box[1])
            self.drawCard(card, box[0], box[1])
            if coverage > 0:  # 닫힌 상태이면, 덮개만:
                resizeImage('images/twoCardFlipImages', 'back', self.card_width, self.card_height)
                back = pygame.image.load(f'images/twoCardFlipImages/back_{self.card_width}x{self.card_height}.png')
                backRect = back.get_rect()
                backRect.center = left + self.card_width // 2, top + self.card_height // 2
                self.surface.blit(back, backRect)
                pygame.draw.rect(self.surface, (255, 255, 255), backRect, 1)
        pygame.display.update()

    # 문제없음
    def revealCardsAnimation(self, cards_to_reveal):
        # 상자가 열려요
        for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
            self.drawCardCovers(cards_to_reveal, coverage)

    # 문제없음
    def coverCardsAnimation(self, cards_to_cover):
        # 상자가 닫혀요
        for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
            self.drawCardCovers(cards_to_cover, coverage)

    # 문제없음
    def setRandomBoard(self):
        self.board = self.getRandomBoard()

    # 문제없음
    def getRandomBoard(self):  # 카드 섞기
        cards = []
        pictures = random.sample(self.cards, int(self.board_width * self.board_height / 2))
        for pic in pictures:
            cards.append((pic, 1))
            # print(cards)
        random.shuffle(cards)
        # print(cards)
        num_cards_used = int(self.board_width * self.board_height / 2)
        cards = cards[:num_cards_used] * 2
        # print(cards)
        random.shuffle(cards)
        # 게임판 만들기
        board = []
        for x in range(self.board_width):
            column = []
            for y in range(self.board_height):
                column.append(cards[0])
                del cards[0]  # 추가한 아이콘을 지운다
            board.append(column)
        # print(board)
        return board

    # 문제없음
    # getBoxAtPixel을 다음 메서드로 구현
    def getMousePositionOnBoard(self, x, y):
        for boxX in range(self.board_width):
            for boxY in range(self.board_height):
                left, top = self.getCardPosition(boxX, boxY)
                box_rect = pygame.Rect(left, top, self.card_width, self.card_height)
                if box_rect.collidepoint(x, y):
                    return boxX, boxY
        return None, None

    # 문제없음
    def drawHighLightCard(self, card_x, card_y,  highlight_color=(255, 0, 0)):
        left, top = self.getCardPosition(card_x, card_y)
        pygame.draw.rect(self.surface, highlight_color, (left - 5, top - 5, self.card_width + 10, self.card_height + 10), 4)

    # 문제없음
    # 카드를 엎어놓은 상태를 저장하는 메소드
    def generateRevealedCardsData(self, val):
        boxes = []  # 열린 상자 만들기
        for n in range(self.board_width):
            boxes.append([val] * self.board_height)
        return boxes

    # 문제없음
    @staticmethod
    def splitIntoGroupsOf(group_size, the_list):
        # 2차원 리스트 생성, 최대로 group_size 만큼의 요소포함
        result = []
        for n in range(0, len(the_list), group_size):
            result.append(the_list[n:n + group_size])
        return result

    # 문제없음
    # 게임 시작할 때 일부 카드를 보여주고 시작하는 메서드
    def startGameAnimation(self):
        # 무작위로 상자를 열어서 보여준다.
        self.revealed_cards = self.generateRevealedCardsData(False)
        cards = []
        for x in range(self.board_width):
            for y in range(self.board_height):
                cards.append((x, y))
        random.shuffle(cards)
        # 처음 시작할 때 네개만 보여주기
        count_of_intro_show = 4
        card_list = random.sample(cards, count_of_intro_show)
        card_groups = self.splitIntoGroupsOf(1, card_list)
        self.drawBoard()

        for card_group in card_groups:
            self.revealCardsAnimation(card_group)
            self.coverCardsAnimation(card_group)

    # 문제없음
    # 게임이 끝나고 실행하는 메서드
    def gameWonAnimation(self):
        pygame.mixer.music.fadeout(10)
        clock = pygame.time.Clock()
        # color1, color2 = color2, color1  # 색깔 깜빡이기
        # screen.blit(cardbackimg, (0, 0))
        # pygame.display.flip()
        # pygame.time.wait(200)

        # drawBoard(board, coveredBoxes)
        # pygame.time.wait(300)

        playing = True
        while playing:
            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                    pygame.quit()
                    sys.exit()

            # 스크린 배경색 칠하기
            self.surface.fill(WHITE)

            # 버튼 만들기
            # showButtonText(DISPLAYSURF, "성공!", 50, (WINDOWWIDTH // 2, int(WINDOWHEIGHT / 2)), BLACK)
            winText = TextView(self.surface, "성공!", "fonts/ELAND_Choice_M.ttf", 50, BLACK,
                               (self.surface_width // 2, int(self.surface_height / 2)))
            winText.showText()
            againButton = Button(self.surface, "다시시작", 20, BLACK, (self.surface_width - 140, self.surface_height - 200), (120, 50),
                                 (0, 255, 0), (0, 255, 100))
            againButton.onClickListener(initTwoCardFlipGame)
            backButton = Button(self.surface, "뒤로가기", 20, BLACK, (self.surface_width - 140, self.surface_height - 130), (120, 50),
                                (0, 0, 255), (0, 100, 255))
            backButton.onClickListener(selectGame)
            quitButton = Button(self.surface, "게임종료", 20, BLACK, (self.surface_width - 140, self.surface_height - 60), (120, 50),
                                (255, 0, 0), (255, 100, 0))
            quitButton.onClickListener(sys.exit)
            # 작업한 내용 갱신하기
            pygame.display.flip()

            # 1초에 60번의 빈도로 순환하기
            clock.tick(60)

    # 문제없음
    # 카드가 다 뒤집어 졌는지 여부를 판별하는 메소드
    def hasWon(self):
        # 모든 상자가 열렸으면 True, 아니면 False
        for n in self.revealed_cards:
            if False in n:
                return False  # 닫힌게 있으면 False
        return True
