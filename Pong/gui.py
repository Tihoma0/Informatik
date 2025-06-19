from typing import Callable
import pygame as pg
from enum import Enum

class Button:

    def __init__(self, rect: pg.Rect, colors: list[tuple[int, int, int]], command: Callable[[int], None], id: int, text: str = None, font: pg.font.Font = None, textcolors: list[tuple[int, int, int]] = None) -> None:
        self.__rect = rect
        self.__colors = colors
        self.__command: Callable[[int], None] = command
        self.__id = id
        self.__state = 0 # 0: normal, 1: hovered, 2: clicked
        self.__previous_state = 0
        self.__text = text
        self.__font = font
        self.__color = self.__colors[0]
        self.__textcolors = textcolors
        self.__textcolor = (0, 0, 0)

    def __get_clicked(self, mousepos: tuple[int, int], mousebuttondown: bool):
        self.__state = 0
        if self.__rect.collidepoint(mousepos):
            self.__state = 1
            if mousebuttondown:
                self.__state = 2

    def _update(self, mousepos: tuple[int, int], mousebuttons: tuple[bool, bool, bool]):
        self.__get_clicked(mousepos, mousebuttons[0])
        self.__color = self.__colors[self.__state]
        if self.__textcolors is not None:
            self.__textcolor = self.__textcolors[self.__state]
        if self.__previous_state != self.__state:
            self.__previous_state = self.__state
            if self.__state == 2 and self.__command is not None:
                self.__command(self.__id)


    def _draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.__color, self.__rect)
        textsurface: pg.Surface = self.__font.render(self.__text, False, self.__textcolor)
        textRect = textsurface.get_rect(center = self.__rect.center)
        screen.blit(textsurface, textRect)