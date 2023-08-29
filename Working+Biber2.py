#memory Puzzle

import random, pygame, sys
from PIL import Image
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 60 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 4 # number of columns of icons
BOARDHEIGHT = 4 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)


pics = []
for i in range(1, 11):
    pics.append('clover' + str(i))
for i in range(1, 11):
    pics.append('dia' + str(i))
for i in range(1, 11):
    pics.append('heart' + str(i))
for i in range(1, 11):
    pics.append('spaid' + str(i))

assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("musics/twocardgamemusic.mp3")
    pygame.mixer.music.play(-5,0.0)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    mouseX = 0
    mouseY = 0
    pygame.display.set_caption('두카드 뒤집기 게임')
    pygame.display.set_icon(pygame.image.load('images/twoCardFlipImages/back.png'))
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # 첫 클릭 좌표 저장
    DISPLAYSURF.fill(WHITE)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(WHITE)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type ==KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        boxX, boxY = getBoxAtPixel(mouseX, mouseY)
        if boxX is not None and boxY is not None:
            if not revealedBoxes[boxX][boxY]:
                drawHighlightBox(boxX,boxY)
            if not revealedBoxes[boxX][boxY] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxX, boxY)])
                revealedBoxes[boxX][boxY] = True
                if firstSelection is None:
                    firstSelection = (boxX, boxY)
                else:
                    icon1shape, icon1color = getPicAndNum(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getPicAndNum(mainBoard, boxX, boxY)
                    if icon1shape is not icon2shape or icon1color is not icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxX, boxY)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxX][boxY] =False
                    elif hasWon(revealedBoxes):
                       gameWonAnimation(mainBoard)
                       pygame.time.wait(2000)

                       #게임판 재설정
                       mainBoard = getRandomizedBoard()
                       revealedBoxes = generateRevealedBoxesData(False)

                       #잠깐 공개
                       drawBoard(mainBoard, revealedBoxes)
                       pygame.display.update()
                       pygame.time.wait(1000)

                       #게임 시작
                       startGameAnimation(mainBoard)
                       pygame.mixer.music.play(-5,0.0)
                    firstSelection = None #1번 박스 리셋

                #화면을 다시 그린 다음 시간 지연을 기다린다..
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def hasWon(revealedBoxes):
    #모든 상자가 열렸으면 True, 아니면 False
    for i in revealedBoxes:
        if False in i:
            return False #  닫힌게 있으면 False
    return True


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH) :
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    global pics
    cards=[]
    #photoList=[None]*8
    #for i in range(8) :
        #photoList[i]="pic/"+pics[i]
    for pic in pics:
        for num in range(1,2):
            cards.append((pic,num))
    random.shuffle(cards)
    numCardsUsed = int(BOARDWIDTH * BOARDHEIGHT /2)
    cards = cards[:numCardsUsed]*2
    random.shuffle(cards)
    
   
 

        #게임판 만들기
    board=[]
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(cards[0])
            del cards[0] #추가한 아이콘을 지운다
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    #2차원 리스트 생성. 최대로 groupSize만큼의 요소 포함)
    result = []
    for i in range(0, len(theList),groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    #좌표를 픽셀좌표로 변환
    left = boxx*(BOXSIZE+GAPSIZE) +XMARGIN
    top = boxy*(BOXSIZE+GAPSIZE) +YMARGIN
    return(left, top)

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawCard(pic, num, boxx, boxy):
    quarter = int(BOXSIZE*0.25)
    half= int(BOXSIZE*0.5)
    eight = int(BOXSIZE*0.125)
    

    left,top=leftTopCoordsOfBox(boxx,boxy) #보드 좌표에서 픽셀 좌표 구하기
    
    #그림 카드 만들기
    
    biber1Img = pygame.image.load('pic/biber1.png')
    biber2Img = pygame.image.load('pic/biber2.png')
    biber3Img = pygame.image.load('pic/biber3.png')
    biber4Img = pygame.image.load('pic/biber4.png')
    biber5Img = pygame.image.load('pic/biber5.png')
    biber6Img = pygame.image.load('pic/biber6.png')
    biber7Img = pygame.image.load('pic/biber7.png')
    biber8Img = pygame.image.load('pic/biber8.png')
       
    if pic == 'biber1':
        DISPLAYSURF.blit(biber1Img, (left+eight, top+eight))
    elif pic =='biber2':
        DISPLAYSURF.blit(biber2Img, (left+eight, top+eight))
    elif pic =='biber3':
        DISPLAYSURF.blit(biber3Img, (left+eight, top+eight))
    elif pic =='biber4':
        DISPLAYSURF.blit(biber4Img, (left+eight, top+eight))
    elif pic =='biber5' :
        DISPLAYSURF.blit(biber5Img, (left+eight, top+eight))
    elif pic =='biber6' :
        DISPLAYSURF.blit(biber6Img, (left+eight, top+eight))
    elif pic =='biber7':
        DISPLAYSURF.blit(biber7Img, (left+eight, top+eight))
    elif pic =='biber8':
        DISPLAYSURF.blit(biber8Img, (left+eight, top+eight))

def getPicAndNum(board, boxx, boxy):
    # 아이콘 값은 board[x][y][0]에 있다
    # 색깔 값은 board[x][y][1]에 있다
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    # 닫히거나 열린 상태의 상자를 그린다
    # 상자는 요소 2개를 가진 리스트이며 xy 위치를 가진다
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        pic, num = getPicAndNum(board, box[0], box[1])
        drawCard(pic, num, box[0], box[1])
        if coverage > 0: # 닫힌 상태이면, 덮개만!
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # 상자가 열려요
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # 상자가 닫혀요
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # 모든 상자를 상태에 맞추어 그리기
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # 닫힌 상자를 만든다
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # 열린 상자
                pic, num = getPicAndNum(board, boxx, boxy)
                drawCard(pic, num, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # 무작위로 상자를 열어서 보여준다
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxlist=random.sample(boxes, 4)
    boxGroups = splitIntoGroupsOf(1, boxlist)
    drawBoard(board, coveredBoxes)
    
    for boxGroup in boxGroups:
        
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # 승리하면 배경색을 깜빡인다
    coveredBoxes = generateRevealedBoxesData(True)
    
    global BOXSIZE 
    w=640
    h=480
    size=(w+BOXSIZE, h+BOXSIZE)
    biber0Img=pygame.image.load('pic/0.png')
    screen = pygame.display.set_mode(size)
    
    pygame.mixer.music.fadeout(10)
    
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1# swap colors
        screen.blit(biber0Img,(0,0))
        pygame.display.flip()
        pygame.time.wait(300)
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
        

if __name__ == '__main__':
    main()
