import pygame


class TextView:
    def __init__(self, surface, text="Hello World!", text_font="fonts/ELAND_Choice_M.ttf", text_size=50, text_color=(0, 0, 0), text_position=(100, 100), text_background=None):
        self._surface = surface
        self._text = text
        self._text_font = text_font
        self._text_size = text_size
        self._text_color = text_color
        self._text_position = text_position
        self._text_background = text_background
        self.text_object = pygame.font.Font(self._text_font, self._text_size)
        self.text_rect = None

    def setSurface(self, surface):
        self._surface = surface

    def getSurface(self):
        return self._surface

    def setText(self, text):
        self._text = text

    def setTextFont(self, text_font):
        self._text_font = text_font

    def setTextSize(self, text_size):
        self._text_size = text_size

    def setTextColor(self, text_color):
        self._text_color = text_color

    def setTextPosition(self, text_position):
        self._text_position = text_position

    def setTextBackground(self, text_background):
        self._text_background = text_background

    def setTextBold(self):
        self.text_object.bold = True
        self.showText()

    def setTextItalic(self):
        self.text_object.italic = True
        self.showText()

    def setTextUnderline(self):
        self.text_object.underline = True
        self.showText()

    def showText(self, center=1):
        self.text_render = self.text_object.render(self._text, True, self._text_color, self._text_background)
        self.text_rect = self.text_render.get_rect()
        if center:
            self.text_rect.center = self._text_position
        else:
            self.text_rect.topleft = self._text_position
        self._surface.blit(self.text_render, self.text_rect)
