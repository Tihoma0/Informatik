from abc import abstractmethod, ABC
from typing import Callable 
import math
import numpy as np
import pygame as pg
from enum import Enum

class Component(ABC):

    def draw(self, screen: pg.Surface, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        pass

    def update(self, mouse_pos: tuple[int, int], mouse_buttons: tuple[bool, bool, bool], camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        pass

    def get_bottom(self) -> int:
        pass


class Label(Component):

    def __init__(self, image: pg.Surface, pos: tuple[int, int], size: tuple[int, int] | None = None):
        if size is not None:
            image = pg.transform.scale(image, size)
        self.__image = image
        self.__pos = pos
        self.__rect = pg.Rect(self.__pos[0], self.__pos[1], self.__image.get_width(), self.__image.get_height())
    
    def draw(self, screen: pg.Surface, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        screen.blit(self.__image, (int(self.__pos[0] - camera_position[0]), int(self.__pos[1] - camera_position[1])))

    def get_bottom(self):
        return self.__rect.bottom

class Button(Component):

    def __init__(self,
                 rect: pg.Rect,
                 command: Callable[[int], None],
                 id: int,
                 colors: list[tuple[int, int, int]] | tuple[int, int, int] | None = None, 
                 text: str = None, 
                 font: pg.font.Font = None, 
                 textcolors: list[tuple[int, int, int]] = [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
                 scales: tuple[int, int, int] = (1, 1, 1), 
                 image: pg.Surface = None, 
                 resize_image = True, 
                 border_radius: int = 0) -> None:
        self.__rect = rect
        self.__default_rect = rect.copy()
        self.__scales = scales
        self._current_tick = 0
        if colors is not None and isinstance(colors[0], int):
            self.__colors = [
                (colors[0], colors[1], colors[2]), # normal
                (min(255, colors[0] + 30), min(255, colors[1] + 30), min(255, colors[2] + 30)), # hovered
                (min(255, colors[0] + 50), min(255, colors[1] + 50), min(255, colors[2] + 50)) # clicked
            ]
        else:
            self.__colors = colors
        self.__command: Callable[[int], None] = command
        self.__id = id
        self.__state = 0 # 0: normal, 1: hovered, 2: clicked
        self.__previous_state = 0
        self.__text = text
        self.__font = font if font is not None else pg.font.SysFont("arial", 32)
        self.__color = self.__colors[0] if colors is not None else None
        self.__textcolors = textcolors
        self.__textcolor = (0, 0, 0)
        if resize_image and image != None:
            image = pg.transform.scale(image, self.__rect.size)
        self.__image = image
        self.__border_radius = border_radius
        

    def __get_clicked(self, mousepos: tuple[int, int], mousebuttondown: bool):
        self.__state = 0
        if self.__rect.collidepoint(mousepos):
            self.__state = 1
            if mousebuttondown:
                self.__state = 2

    def update(self, mousepos: tuple[int, int], mousebuttons: tuple[bool, bool, bool], camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        mousepos = (int(mousepos[0] - camera_position[0]), int(mousepos[1] - camera_position[1]))
        self.__get_clicked(mousepos, mousebuttons[0])
        if self.__color is not None:
            self.__color = self.__colors[self.__state]
        if self.__textcolors is not None:
            self.__textcolor = self.__textcolors[self.__state]
        if self.__previous_state != self.__state:
            self.__previous_state = self.__state
            if self.__state == 2 and self.__command is not None:
                self.__command(self.__id)

    def draw(self, screen: pg.Surface, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        self.__scale = self.__scales[self.__state]
        self.__rect = pg.Rect(
            int(self.__default_rect.x - self.__default_rect.width * self.__scale / 2 - camera_position[0]),
            int(self.__default_rect.y - self.__default_rect.height * self.__scale / 2 - camera_position[1]),
            int(self.__default_rect.width * self.__scale),
            int(self.__default_rect.height * self.__scale)
        )
        if self.__color is not None:
            pg.draw.rect(screen, self.__color, self.__rect, border_radius=self.__border_radius)
        if self.__image is not None:
            if self.__scale == 1:
                screen.blit(self.__image, self.__rect.topleft)
            else:
                screen.blit(pg.transform.scale(self.__image, (self.__image.get_width() * self.__scale, self.__image.get_height() * self.__scale)), self.__rect.topleft)
        textsurface: pg.Surface = self.__font.render(self.__text, False, self.__textcolor)
        textRect = textsurface.get_rect(center = self.__rect.center)
        screen.blit(textsurface, textRect)

    def get_bottom(self) -> int:
        return self.__rect.bottom

    def set_text(self, text: str):
        self.__text = text
    
    def has_mouse_inside(self, mousepos: tuple[int, int], camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)) -> bool:
        mousepos = (int(mousepos[0] - camera_position[0]), int(mousepos[1] - camera_position[1]))
        return self.__rect.collidepoint(mousepos)

class VerticalScrollbar(Component):
    def __init__(self, thumb_rect: pg.Rect, track_rect: pg.Rect, max_value: int = None, min_value: int = 0, has_rounded_edges: bool = True, wanted_mouse_state_pointer: list[int] = [1]):
        self.__thumb_rect = thumb_rect
        self.__track_rect = track_rect
        self.__max_value = max_value if max_value is not None else track_rect.height
        self.__min_value = min_value
        self.__value = (track_rect.height - thumb_rect.height) / (self.__max_value - min_value) * (track_rect.y - thumb_rect.y)
        self.__has_rounded_edges = has_rounded_edges
        self.__mouse_drag_start_pos: tuple[int, int] = None
        self.__thumb_y_pos_on_drag_start = self.__thumb_rect.y
        self.__is_dragged = False
        self.__wanted_mouse_state_pointer = wanted_mouse_state_pointer
        self.__mouse_pressed_before = False
    
    def update(self, mouse_pos: tuple[int, int], mouse_buttons: tuple[bool, bool, bool], camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        rect_on_screen = self.__thumb_rect.copy()
        rect_on_screen.y -= camera_position[1]
        rect_on_screen.x -= camera_position[0]
        if self.__thumb_rect.collidepoint(mouse_pos):
            self.__wanted_mouse_state_pointer[0] = 2
        if not mouse_buttons[0]:
            self.__mouse_drag_start_pos = None
            self.__is_dragged = False
        if rect_on_screen.collidepoint(mouse_pos) and mouse_buttons[0] and not self.__mouse_pressed_before:
            self.__is_dragged = True
        if self.__is_dragged:
            if self.__mouse_drag_start_pos is None:
                self.__mouse_drag_start_pos = mouse_pos
                self.__thumb_y_pos_on_drag_start = self.__thumb_rect.y
            else:
                self.__thumb_rect.y = mouse_pos[1] - self.__mouse_drag_start_pos[1] + self.__thumb_y_pos_on_drag_start
                self.__thumb_rect.y = min(max(self.__thumb_rect.y, self.__track_rect.y), self.__track_rect.y + self.__track_rect.height - self.__thumb_rect.height)
                self.__value = (self.__max_value - self.__min_value) * (self.__thumb_rect.y - self.__track_rect.y) /(self.__track_rect.height - self.__thumb_rect.height) + self.__min_value
        self.__mouse_pressed_before = mouse_buttons[0]

    def render(self, screen: pg.Surface, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        track_rect_on_screen = self.__track_rect.copy()
        track_rect_on_screen.y -= camera_position[1]
        track_rect_on_screen.x -= camera_position[0]
        thumb_rect_on_screen = self.__thumb_rect.copy()
        thumb_rect_on_screen.y -= camera_position[1]
        thumb_rect_on_screen.x -= camera_position[0]
        pg.draw.rect(screen, (0, 0, 0), track_rect_on_screen, border_radius = 10 if self.__has_rounded_edges else 0)
        pg.draw.rect(screen, (255, 255, 255), thumb_rect_on_screen, border_radius = 10 if self.__has_rounded_edges else 0)

    def set_max_value(self, max_value: int):
        self.__max_value = max_value
    
    def set_min_value(self, min_value: int):
        self.__min_value = min_value
    
    def get_max_value(self):
        return self.__max_value
    
    def get_min_value(self):
        return self.__min_value

    def get_value(self):
        return self.__value

    def set_value(self, value: int):
        self.__value = max(min(value, self.__max_value), self.__min_value)
        self.__thumb_rect.y = self.__track_rect.y + (self.__track_rect.height - self.__thumb_rect.height) * (self.__value - self.__min_value) / (self.__max_value - self.__min_value)

    def get_bottom(self) -> int:
        return self.__track_rect.bottom

    def is_dragged(self) -> bool:
        return self.__is_dragged

class VerticalScrollPane(Component):

    def __init__(self, rect: pg.Rect, scrollbar: VerticalScrollbar = None, border_width: int = 1, background_color: tuple[int, int, int] = (100, 100, 100), border_color: tuple[int, int, int] = (255, 255, 255), has_rounded_edges: bool = False, has_border: bool = True, scroll_speed: int = 40, wanted_mouse_state_pointer: list[int] = [1]):
        self.__rect = rect
        print(wanted_mouse_state_pointer, "Vertzgv cal")
        self.__scrollbar = scrollbar if scrollbar is not None else VerticalScrollbar(pg.Rect(self.__rect.width - 10 - border_width, border_width, 10, self.__rect.height//6 - border_width*2), pg.Rect(self.__rect.width - 10 - border_width, border_width, 10, self.__rect.height - border_width*2), wanted_mouse_state_pointer = wanted_mouse_state_pointer)
        self.__components: list[Component] = []
        self.__surface = pg.Surface((self.__rect.width, self.__rect.height), pg.SRCALPHA)
        self.__border_width = border_width
        self.__background_color = background_color
        self.__border_color = border_color
        self.__has_rounded_edges = has_rounded_edges
        self.__has_border = has_border
        self.__scroll_speed = scroll_speed
    
    def add_component(self, component: Component):
        self.__components.append(component)
        if component.get_bottom() > self.__scrollbar.get_max_value():
            self.__scrollbar.set_max_value(component.get_bottom() - self.__rect.height + 100)

    
    def remove_component(self, component: Component):
        self.__components.remove(component)

    def update(self, mouse_pos: tuple[int, int], mouse_buttons: tuple[bool, bool, bool], mouse_wheel: int = 1, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        camera_position = camera_position.copy()
        camera_position -= [self.__rect.x, self.__rect.y]
        self.__scrollbar.update(mouse_pos, mouse_buttons, camera_position)
        if pg.Rect(int(self.__rect.x - camera_position[0]), int(self.__rect.y-camera_position[1]), self.__rect.width, self.__rect.height).collidepoint(mouse_pos):
            self.__scrollbar.set_value(self.__scrollbar.get_value() - mouse_wheel*self.__scroll_speed)
        for components in self.__components:
            components.update(mouse_pos, mouse_buttons, camera_position)

    def draw(self, screen: pg.Surface, camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        self.__surface.fill((0, 0, 0, 0))
        if self.__has_rounded_edges:
            pg.draw.rect(self.__surface, self.__background_color, pg.Rect(0, 0, self.__rect.width, self.__rect.height), border_radius=5)
            if self.__has_border:
                pg.draw.rect(self.__surface, self.__border_color, pg.Rect(0, 0, self.__rect.width, self.__rect.height), self.__border_width, border_radius=5)
        else:
            pg.draw.rect(self.__surface, self.__background_color, pg.Rect(0, 0, self.__rect.width, self.__rect.height))
            if self.__has_border:
                pg.draw.rect(self.__surface, self.__border_color, pg.Rect(0, 0, self.__rect.width, self.__rect.height), self.__border_width)
        offset = [0, 0]
        offset[1] += self.__scrollbar.get_value()
        for components in self.__components:
            components.draw(self.__surface, offset)
        self.__scrollbar.render(self.__surface, (0, 0))
        screen.blit(self.__surface, (int(self.__rect.x - camera_position[0]), int(self.__rect.y - camera_position[1])))


    def get_scrollbar(self) -> VerticalScrollbar:
        return self.__scrollbar










