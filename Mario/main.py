from threading import Thread

from setup import setup
setup()
import numpy as np
import pygame as pg

import debugger
from player import Player
from scenes import Scenehandler
from grid import Grid, GridWorker

from graphics_operator import pygame_to_pil

"""
TODO:
    - GUI Menu
    - Saving
    - Loading
"""
import os

print(os.listdir("./"))

class Game:

    def __init__(self) -> None:
        self.__width, self.__height = self.__size = pg.display.Info().current_w, pg.display.Info().current_h - 80
        self.__screen = pg.display.set_mode(self.__size, pg.DOUBLEBUF | pg.RESIZABLE)
        Scenehandler.init(self.__size)
        pg.display.set_caption("Mario")

        self.__screen.fill(0)
        pg.display.flip()
        debugger.setup()

        self.__grid = None
        self.__player = None
        self.__MAX_FPS = 60
        self.__clock = pg.time.Clock()
        self.__keys = pg.key.get_pressed()
        self.__wanted_mouse_state_pointer = [2] # list works as pointer
        self.__mouse_state_before = 1
        self.__mouse_pos = pg.mouse.get_pos()
        self.__mouse_buttons = pg.mouse.get_pressed()
        self.__mouse_wheel = 0
        self.__scene_handler = Scenehandler()

        self.__running = False

        self.__grid_worker = None

        self.__setupThread = Thread(target=self.__setup)

        
    def start(self):
        self.__running = True
        self.__setupThread.start()
        self.__mainloop()
    
    def __setup(self):
        Grid.init()
        GridWorker.init()
        self.__grid = Grid.load_from_file("./Mario/levels/grid.map")
        self.__player = Player((0.5, 0), self.__grid)
        if self.__grid.get((0, 1)) is None:
            self.__grid.set((0, 1), "grass_top")
        self.__grid_worker = GridWorker(self.__grid, self.__screen, self.__wanted_mouse_state_pointer, self.__player.get_camera_position())
        
        

    def __mainloop(self):
        while self.__running:
            if(self.__scene_handler.get_current_scene() == "game" and self.__setupThread.is_alive()):
                self.__setupThread.join()
            self.__poll_events()
            self.__tick()
            self.__render()
            self.__clock.tick(self.__MAX_FPS)
            debugger.print_log(self.__keys)
        self.__quit()

    def __poll_events(self):
        self.__mouse_wheel = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__running = False
            elif event.type == pg.VIDEORESIZE:
                self.__width, self.__height = self.__size = event.size
            elif event.type == pg.MOUSEWHEEL:
                self.__mouse_wheel = event.y
        self.__keys = pg.key.get_pressed()
        self.__handle_mouse()
    
    def __render(self):
        debugger.primary_log("FPS: " + str(int(self.__clock.get_fps())))
        current_scene = self.__scene_handler.get_current_scene()
        self.__screen.fill((100, 100, 255))
        if current_scene != "game":
            self.__scene_handler.render(self.__size)
            image: pg.Surface = self.__scene_handler.get_image()
            self.__screen.blit(image, (0, 0))
        else:
            self.__player.draw(self.__screen, self.__size)
            self.__grid_worker.render(self.__screen, self.__mouse_pos)
        pg.display.flip()
    
    def __handle_mouse(self):
        if self.__mouse_state_before != self.__wanted_mouse_state_pointer[0]:
            self.__mouse_state_before = self.__wanted_mouse_state_pointer[0]
            #match self.__wanted_mouse_state_pointer[0]:
            #    case 1:
            #        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            #    case 2:
             #       pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
              #  case 3:
               #     pg.mouse.set_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)
                #case 4:
                 #   pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEWE)
                #case 5:
                 #   pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZENS)
        self.__mouse_pos = pg.mouse.get_pos()
        self.__mouse_buttons = pg.mouse.get_pressed()
        self.__wanted_mouse_state_pointer[0] = 1
        
    
    def __tick(self):
        current_scene = self.__scene_handler.get_current_scene()
        if current_scene == "game":
            self.__player.update(self.__keys, self.__grid_worker.get_camera_mode(), self.__grid_worker.get_camera_pos())
            self.__grid_worker.update(self.__keys, self.__mouse_pos, self.__mouse_buttons, self.__mouse_wheel, self.__size, self.__player.get_camera_position(), self.__wanted_mouse_state_pointer)
    
    def __quit(self):
        self.__grid.save_to_file("./Mario/levels/grid.map")

        



if __name__ == "__main__":
    pg.init()
    
    game = Game()
    game.start()
