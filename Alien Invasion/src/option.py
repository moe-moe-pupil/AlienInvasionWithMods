import pygame
from my_enum.color_enum import ColorEnum

color_enum = ColorEnum()




def do_nothing():
    pass


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 1, textColor)
    return newText


class Option():
    def __init__(self, idx, name, text, font, size, color, fun=do_nothing, can_selected=True, height = 80):
        self.name = name
        self.idx = idx
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.content = text_format(text, font, size, color)
        self.func = fun
        self.can_selected = can_selected
        self.height = height

    def update(self):
        self.content = text_format(self.text, self.font, self.size, self.color)

    def selected(self):
        self.color = color_enum.white
        self.update()

    def unselected(self):
        self.color = color_enum.black
        self.update()

    def trigger(self):
        self.func()


