import pygame
import sys
from TextView import TextView

from enum import Enum

class Pos(Enum):
    topleft = 0
    center = 1


class Button(TextView):
    def __init__(self, surface, text, text_size, text_color, button_position, button_size, default_color, active_color,
                 border_radius=0):
        super().__init__(surface=surface, text=text, text_size=text_size, text_color=text_color)
        self.button_position = button_position
        self.button_size = button_size
        self.default_color = default_color
        self.active_color = active_color
        self.border_radius = border_radius
        self.setTextPosition(
            (self.button_position[0] + self.button_size[0] // 2, self.button_position[1] + self.button_size[1] // 2))

    def setTextViewInButton(self, text_size, text_color, text_background=None):
        self.setTextSize(text_size)
        self.setTextColor(text_color)
        self.setTextBackground(text_background)

    def setDefaultColor(self, default_color):
        self.default_color: tuple = default_color

    def setActiveColor(self, active_color):
        self.active_color: tuple = active_color

    def setBorderRadius(self, border_radius):
        self.border_radius = border_radius

    def onClickListener(self, action=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        # print('x :', button_pos[0], 'y :', button_pos[1])
        if self.button_position[0] + self.button_size[0] > mouse_pos[0] > self.button_position[0] and \
                self.button_position[1] + self.button_size[1] > mouse_pos[1] > \
                self.button_position[1]:
            pygame.draw.rect(self._surface, self.active_color, (self.button_position, self.button_size), 0,
                             self.border_radius)
            if mouse_clicked[0]:
                print("Button", self._text, "Clicked")
                if action is not None:
                    action()
        else:
            pygame.draw.rect(self._surface, self.default_color, (self.button_position, self.button_size), 0,
                             self.border_radius)
        self.showText()

    def isButtonClicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        if self.button_position[0] + self.button_size[0] > mouse_pos[0] > self.button_position[0] and \
                self.button_position[1] + self.button_size[1] > mouse_pos[1] > \
                self.button_position[1]:
            if mouse_clicked[0]:
                return True
            else:
                return False
        else:
            return False

    def isMouseOnButton(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.button_position[0] + self.button_size[0] > mouse_pos[0] > self.button_position[0] and \
                self.button_position[1] + self.button_size[1] > mouse_pos[1] > \
                self.button_position[1]:
            return True
        else:
            return False
