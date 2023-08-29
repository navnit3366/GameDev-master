from TextView import TextView
import pygame


class EditText(TextView):
    def __init__(self, surface, text_size, text_color, default_color, active_color, text_box_size,
                 text_box_position):
        self.input_text = str(0)
        super().__init__(surface=surface, text=self.input_text, text_size=text_size, text_color=text_color)
        self.active = False
        self.text_box_size = text_box_size
        self.text_box_position = text_box_position
        self.text_box_rect = pygame.Rect(self.text_box_position[0],
                                         self.text_box_position[1], self.text_box_size[0], self.text_box_size[1])
        self.default_color = default_color
        self.active_color = active_color
        self.text_box_color = self.default_color
        self.setTextPosition((self.text_box_rect.x + 10, self.text_box_rect.y + 10))

    def setEditTextPosition(self, position: tuple):
        self.text_box_position = position

    def showEditTextBox(self):
        pygame.draw.rect(self.getSurface(), self.text_box_color, self.text_box_rect, 2)
        self.setText(self.input_text)
        self.showText(0)

    def initEditText(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isActive(event)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def isActive(self, event):
        if self.text_box_rect.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False

    def updateTextBoxColor(self):
        if self.active:
            self.text_box_color = self.active_color
        else:
            self.text_box_color = self.default_color

    def resetInputText(self):
        self.input_text = str(0)
