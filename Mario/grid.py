import os
import debugger
from gui import Button, Label, VerticalScrollPane
import numpy as np
import pygame as pg
import math
from graphics_operator import get_images, resize_all

class Grid:

    __default_tile_size = 70
    current_tile_size = 70
    __images = None

    @staticmethod
    def load_from_file(path: str) -> 'Grid':
        if (not os.path.exists(path)):
            raise Exception(f"File {path} does not exist")
        with open(path, "r") as file:
            data = eval(file.read())
            result = Grid()
            result.__dict = data
            return result
    
    @staticmethod
    def get_default_tile_size() -> int:
        return Grid.__default_tile_size


    @staticmethod
    def init(image_folder_name: str = "World"):
        Grid.__images = resize_all((Grid.current_tile_size, Grid.current_tile_size), get_images(image_folder_name))

    def __init__(self) -> None:
        self.__dict: dict[str, any] = {}
        self.__time = 0
    
    def save_to_file(self, path: str):
        abs_path = os.path.abspath(path)
        print(abs_path)
        with open(abs_path, "w") as file:
            file.write(str(self.__dict))
    
    def __get_key_by_coord(self, coord) -> str:
        return coord
    
    def get(self, pos: tuple[int, int]) -> any:
        return self.__dict.get(self.__get_key_by_coord(pos), None)
    
    def set(self, pos: tuple[int, int], value: any):
        self.__dict[self.__get_key_by_coord(pos)] = value
    
    
    def draw(self, screen: pg.Surface, camera_pos: np.ndarray):
        self.__time += 0.1
        screen_width, screen_height = screen.get_size()
        debugger.primary_log("tile_size: " + str(self.current_tile_size))
        min_tile_x = math.floor((camera_pos[0] - screen_width/2)/self.current_tile_size)
        max_tile_x = math.ceil((camera_pos[0] + screen_width/2)/self.current_tile_size)
        min_tile_y = math.floor((camera_pos[1] - screen_height/2)/self.current_tile_size)
        max_tile_y = math.ceil((camera_pos[1] + screen_height/2)/self.current_tile_size)
        for x in range(min_tile_x, max_tile_x):
            for y in range(min_tile_y, max_tile_y):
                screen_x = x * self.current_tile_size - camera_pos[0] + screen_width/2
                screen_y = y * self.current_tile_size - camera_pos[1] + screen_height/2
                tile = self.get((x, y))
                if tile is None:
                    continue
                if(tile == "flag_green"):
                    tile = "flag_green_f" + str(int((self.__time+x*12033.324731 + y*334982.24032))%4+1)
                image = Grid.__images["blocks"][tile]
                
                if image is None:
                    continue
                screen.blit(image, (int(screen_x), int(screen_y)))

print(os.listdir("./Mario/images/World/blocks"))
class GridWorker:

    __all_tiles = None
    __all_images = None
    

    @staticmethod
    def init():
        
        GridWorker.__all_tiles = os.listdir("./Mario/images/World/blocks")
        GridWorker.__all_images = get_images("World")["blocks"]
        GridWorker.__all_tiles.remove("flag_green_f1.png")
        GridWorker.__all_tiles.remove("flag_green_f2.png")
        GridWorker.__all_tiles.remove("flag_green_f3.png")
        GridWorker.__all_tiles.remove("flag_green_f4.png")
        GridWorker.__all_tiles.append("flag_green")


    def __init__(self, grid: Grid, screen: pg.Surface, wanted_mouse_state_pointer: list[int], camera_pos: np.ndarray) -> None:
        self.__grid = grid
        width, height = screen.get_size()
        self.__scroll_pane: VerticalScrollPane = VerticalScrollPane(pg.Rect(0, 0, min(width/2, 100), height), background_color=(180, 180, 255), has_border=False, wanted_mouse_state_pointer=wanted_mouse_state_pointer)
        for i in range(len(self.__all_tiles)):
            tile = self.__all_tiles[i].split(".")[0]
            if tile == "flag_green":
                tile = "flag_green_f1"
            image: pg.Surface = self.__all_images[tile].copy()
            self.__scroll_pane.add_component(Button(pg.Rect(40, i*60 + 30, 40, 40), self.__on_click, i, image = image.copy(), scales=[1, 1.5, 1]))
        self.__dragged_tile = None
        self.__place_mode = "hold" # drag and drop, hold
        self.__place_mode_switch_button = Button(pg.Rect(width - 280, 50, 500, 60), command=self.__on_click, id = -2, colors=(200, 200, 200), text="Place mode: hold", font=pg.font.Font("./Mario/Minecraft.ttf", 28), textcolors=[(0, 0, 0), (0, 0, 0), (0, 0, 0)], scales=[1, 1.1, 1], border_radius=20)
        self.__camera_mode_switch_button = Button(pg.Rect(width - 280, 150, 500, 60), command=self.__on_click, id = -3, colors=(200, 200, 200), text="Camera mode: player", font=pg.font.Font("./Mario/Minecraft.ttf", 28), textcolors=[(0, 0, 0), (0, 0, 0), (0, 0, 0)], scales=[1, 1.1, 1], border_radius=20)
        self.__camera_pos = camera_pos.copy()
        self.__camera_mode = "player" # player, free
        self.__mouse_pos_before = (0, 0)

    def __on_click(self, id: int):
        if id >= 0:
            self.__dragged_tile = self.__all_tiles[id].split(".")[0]
        else: 
            match id:
                case -2:
                    if self.__place_mode == "drag and drop":
                        self.__place_mode = "hold"
                    else:
                        self.__place_mode = "drag and drop"
                    self.__place_mode_switch_button.set_text(f"Place mode: {self.__place_mode}")
                case -3:
                    if self.__camera_mode == "player":
                        self.__camera_mode = "free"
                    else:
                        self.__camera_mode = "player"
                    self.__camera_mode_switch_button.set_text(f"Camera mode: {self.__camera_mode}")
        
    def update(self, keys: list[bool], mouse_pos: tuple[int, int], mouse_buttons: tuple[bool, bool, bool], mouse_wheel: int = 0, screen_size: tuple[int, int] = (0, 0), player_camera_position: np.ndarray = np.array([0, 0], dtype=np.float32), wanted_mouse_state_pointer: list[int] = [0, 0, 0]):
        mouse_delta = (mouse_pos[0] - self.__mouse_pos_before[0], mouse_pos[1] - self.__mouse_pos_before[1])
        self.__mouse_pos_before = mouse_pos
        if self.__camera_mode == "player":
            self.__camera_pos = player_camera_position.copy()
        elif self.__camera_mode == "free":
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                wanted_mouse_state_pointer[0] = 3
                self.__camera_pos -= mouse_delta
        self.__scroll_pane.update(mouse_pos, mouse_buttons, mouse_wheel)
        if not self.__place_mode_switch_button.has_mouse_inside(mouse_pos) and not self.__camera_mode_switch_button.has_mouse_inside(mouse_pos) and mouse_pos[0] > min(screen_size[0]/1.95, 105) and not self.__scroll_pane.get_scrollbar().is_dragged():
            if self.__place_mode == "drag and drop":
                if not mouse_buttons[0] and self.__dragged_tile is not None:
                    self.__grid.set((math.floor((mouse_pos[0] + self.__camera_pos[0] - screen_size[0]/2)/Grid.current_tile_size), math.floor((mouse_pos[1] + self.__camera_pos[1] - screen_size[1]/2)/Grid.current_tile_size)), self.__dragged_tile)
                    self.__dragged_tile = None
                if mouse_buttons[0] and self.__dragged_tile is None:
                    self.__grid.set((math.floor((mouse_pos[0] + self.__camera_pos[0] - screen_size[0]/2)/Grid.current_tile_size), math.floor((mouse_pos[1] + self.__camera_pos[1] - screen_size[1]/2)/Grid.current_tile_size)), None)
            elif self.__place_mode == "hold":
                if mouse_buttons[0]:
                    self.__grid.set((math.floor((mouse_pos[0] + self.__camera_pos[0] - screen_size[0]/2)/Grid.current_tile_size), math.floor((mouse_pos[1] + self.__camera_pos[1] - screen_size[1]/2)/Grid.current_tile_size)), self.__dragged_tile)
                if mouse_buttons[2]:
                    self.__dragged_tile = None

        self.__place_mode_switch_button.update(mouse_pos, mouse_buttons)
        self.__camera_mode_switch_button.update(mouse_pos, mouse_buttons)


    def render(self, screen: pg.Surface, mouse_pos: tuple[int, int]):
        self.__grid.draw(screen, self.__camera_pos)
        self.__scroll_pane.draw(screen)
        self.__place_mode_switch_button.draw(screen)
        self.__camera_mode_switch_button.draw(screen)
        if self.__dragged_tile is not None:
            if self.__dragged_tile == "flag_green":
                drawn_tile = "flag_green_f1"
            else:
                drawn_tile = self.__dragged_tile
            screen.blit(pg.transform.scale(self.__all_images[drawn_tile], (Grid.current_tile_size, Grid.current_tile_size)), (mouse_pos[0] - Grid.current_tile_size/2, mouse_pos[1] - Grid.current_tile_size/2))

    def get_camera_pos(self) -> np.ndarray:
        return self.__camera_pos
    
    def get_camera_mode(self) -> str:
        return self.__camera_mode


