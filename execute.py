import pygame


def initGame():
    import initalGame
    return initalGame.initGame()


def selectGame():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(10)
    import initalGame
    return initalGame.selectGame()


def initTwoCardFlipGame():
    import twoCardFlipGame
    return twoCardFlipGame.initTwoCardFlipGame()


def runTwoCardFlipGame():
    import twoCardFlipGame
    return twoCardFlipGame.runTwoCardFlipGame()


def omokGame():
    import omokGame
    return omokGame.omokGame()


def initRandomNumberGame():
    import randomNumberGame
    return randomNumberGame.initRandomNumberGame()