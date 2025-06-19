import math
import debugger
from graphics_operator import get_images, scale_all
from grid import Grid
import numpy as np
import pygame as pg


class Player:
    
    __collision_horizontal_width = 0.34 * 42 * Grid.current_tile_size / 40 # für die horizontale kollosion muss er breiter sein, da er sonst an den vertikalen Wänden hängen bleibt
    __collision_vertical_width = 0.25 * 42 * Grid.current_tile_size  / 40
    __collision_horizontal_height = 0.7 * 42 * Grid.current_tile_size / 40 # für die horizontale kollosion muss er niedriger sein, da er sonst an den horizontalen hindernissen hängen bleibt
    __collision_vertical_height = 0.84 * 42 * Grid.current_tile_size / 40
    __all_images = scale_all(Grid.current_tile_size/48, get_images("mario"))

    __time_step = 0.1
    __air_resistance = 0.0003
    __friction = 0.005
    __lateral_resistance = 0.03
    __jump_power = 7.5 * (Grid.current_tile_size / 40)**0.5
    __acceleration = 0.015 * Grid.current_tile_size / 40

    __gameover_y_velocity = Grid.current_tile_size / 3.2


    __traversable_cell_states = [
        "railing_bright", 
        "railing_bright_left", 
        "railing_bright_right", 
        "railing", 
        "railing_left", 
        "railing_right", 
        "stick_orange", 
        "stick_blue", 
        "stick_grey", 
        "stick_pink",  
        "stick_yellow", 
        "dec_grass_1_left", 
        "dec_grass_1", 
        "dec_grass_1_right", 
        "dec_grass_2_left", 
        "dec_grass_2", 
        "dec_grass_2_right",
        "ball_green",
        "ball_grey",
        "flag_s_top",
        "flag_s",
        "flag_green",
    ]

    def __init__(self, pos: tuple[int, int], grid: Grid) -> None:
        self.__grid = grid
        self.__GRAVITY = np.array([0, 0.2], dtype=np.float32)
        self.__velocity = np.array([0, 0], dtype=np.float32)
        self.__start_pos = np.array(pos, dtype = np.float32)*Grid.current_tile_size
        self.__pos = np.array(pos, dtype = np.float32)*Grid.current_tile_size # pos ist die Mitte vom Spieler
        self.__camera_position = self.__pos.copy()
        self.__camera_follow_speed = 0.015
        self.__collided = {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False
        }
        

        self.__image = self.__all_images["go3"]
        self.__is_flipped = False
        self.__is_running = False
        self.__current_frame = 0
        self.__current_time = 0


    def __handle_collision(self):
        if self.__velocity[1] > self.__gameover_y_velocity:
            self.__pos = self.__start_pos.copy()
            self.__velocity = np.array([0, 0], dtype=np.float32)
            self.__camera_position = self.__pos.copy()
        self.__collided = {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False
        }
        min_horizontal_tile_x = math.floor((self.__pos[0] - self.__collision_horizontal_width/2)/Grid.current_tile_size)
        max_horizontal_tile_x = math.ceil((self.__pos[0] + self.__collision_horizontal_width/2))//Grid.current_tile_size # ich habe keine Ahnung, warum es nicht math.ceil((self.__pos[0] + self.__collision_horizontal_width/2)/Grid.current_tile_size) ist. Aber SO funktioniert es.
        min_vertical_tile_x = math.floor((self.__pos[0] - self.__collision_vertical_width/2)/Grid.current_tile_size)
        max_vertical_tile_x = math.ceil((self.__pos[0] + self.__collision_vertical_width/2)/Grid.current_tile_size)

        min_horizontal_tile_y = math.floor((self.__pos[1] - self.__collision_horizontal_height/2)/Grid.current_tile_size)
        max_horizontal_tile_y = math.ceil((self.__pos[1] + self.__collision_horizontal_height/2)/Grid.current_tile_size)
        min_vertical_tile_y = math.floor((self.__pos[1] - self.__collision_vertical_height/2)/Grid.current_tile_size)
        max_vertical_tile_y = math.floor((self.__pos[1] + self.__collision_vertical_height/2)/Grid.current_tile_size) # hier habe ich auch keine Ahnung, warum es nicht math.ceil ist. Es wäre doch der logischste Scritt

        for y in range(min_horizontal_tile_y, max_horizontal_tile_y):
            tile = self.__grid.get((min_horizontal_tile_x, y))
            if tile is not None and tile not in self.__traversable_cell_states:
                self.__collided["left"] = True
            tile = self.__grid.get((max_horizontal_tile_x, y))
            if tile is not None and tile not in self.__traversable_cell_states:
                self.__collided["right"] = True
            
        for x in range(min_vertical_tile_x, max_vertical_tile_x):
            tile = self.__grid.get((x, min_vertical_tile_y))
            if tile is not None and tile not in self.__traversable_cell_states:
                self.__collided["top"] = True
            tile = self.__grid.get((x, max_vertical_tile_y))
            if tile is not None and tile not in self.__traversable_cell_states:
                self.__collided["bottom"] = True
    
    def update(self, keys: list[bool], camera_mode: str = "player", camera_position: np.ndarray = np.array([0, 0], dtype=np.float32)):
        debugger.primary_log("Grid position: " + str((int(self.__pos[0]/Grid.current_tile_size), int(self.__pos[1]/Grid.current_tile_size))))
        self.__current_time += 1
        if abs(self.__velocity[0]) > self.__acceleration:
            self.__is_flipped = self.__velocity[0] < 0
        if keys[pg.K_LCTRL]:
            self.__is_running = True
            self.__acceleration = 0.018
        else:
            self.__is_running = False
            self.__acceleration = 0.005
        for i in range(math.ceil(1/self.__time_step)):
            self.move(keys)
            if(keys[pg.K_a] and not self.__collided["left"]):
                self.__velocity[0] -= self.__acceleration
                self.__pos[0] -= self.__acceleration
            if(keys[pg.K_d] and not self.__collided["right"]):
                self.__velocity[0] += self.__acceleration
                self.__pos[0] += self.__acceleration
        self.__velocity *= 1.0 - self.__air_resistance
        if camera_mode == "player":
            self.__camera_position -= (self.__camera_position - self.__pos)*self.__camera_follow_speed
        elif camera_mode == "free":
            self.__camera_position = camera_position.copy()

    def move(self, keys: list[bool]):
        self.__handle_collision()
        if(self.__collided["bottom"] or self.__collided["top"] or self.__collided["left"] or self.__collided["right"]):
            self.__velocity *= 1.0 - self.__friction*self.__time_step
        self.__velocity += self.__GRAVITY*self.__time_step
        if(self.__collided["bottom"]):
            self.__velocity[1] = 0
            if(keys[pg.K_SPACE] and self.__current_time):
                self.__velocity[1] = -self.__jump_power
        if(self.__collided["top"]):
            self.__velocity[1] = 0.1
            self.__pos[1] = math.ceil((self.__pos[1]-self.__collision_vertical_height/2)/Grid.current_tile_size)*Grid.current_tile_size + self.__collision_vertical_height/2
        if(self.__collided["left"]):
            self.__velocity[0] = 0
            self.__pos[0] = math.ceil((self.__pos[0]-self.__collision_horizontal_width/2)/Grid.current_tile_size)*Grid.current_tile_size + self.__collision_horizontal_width/2
        if(self.__collided["right"]):
            self.__velocity[0] = 0
            self.__pos[0] = math.floor((self.__pos[0]-self.__collision_horizontal_width/2)/Grid.current_tile_size + 1)*Grid.current_tile_size - self.__collision_horizontal_width/2-1
        self.__velocity[0] *= 1.0 - self.__lateral_resistance*self.__time_step
        self.__pos += self.__velocity*self.__time_step
        
    def get_camera_position(self) -> np.ndarray:
        return self.__camera_position

    def __animate(self):
        if(self.__is_running and abs(self.__velocity[0])>2):
            self.__current_frame += abs(self.__velocity[0]/20)
            image_id = "walk" + str(int(self.__current_frame+6)%12 + 1)
        else:
            self.__current_frame += abs(self.__velocity[0]/14)
            image_id = "go" + str(int(self.__current_frame)%8 + 1)
        if abs(self.__velocity[0]) < self.__acceleration: 
            image_id = "go3"     # go3 als Standbild
            self.__current_frame = 2
        if not self.__collided["bottom"]:
            image_id = "jump"
        self.__image = pg.transform.flip(self.__all_images[image_id], self.__is_flipped, False)
        
    
    def draw(self, screen: pg.Surface, screen_size: tuple[int, int]):
        self.__animate()
        image_width = self.__image.get_width()
        screen.blit(
            self.__image,
            (
                int(screen_size[0] // 2 + self.__pos[0] - self.__camera_position[0] - image_width/2),
                int(screen_size[1] // 2 + self.__pos[1] - self.__camera_position[1] - self.__collision_horizontal_height/2 + 1)
            )
        )
    
    def draw_hitbox(self, screen: pg.Surface):
        screen_size = screen.get_size()
        rect = pg.Rect(
            int(self.__pos[0] - self.__camera_position[0] - self.__collision_horizontal_width/2 + screen_size[0] // 2),
            int(self.__pos[1] - self.__camera_position[1] - self.__collision_vertical_height/2 + screen_size[1] // 2),
            int(self.__collision_horizontal_width),
            int(self.__collision_vertical_height)
        )
        pg.draw.rect(screen, (0, 0, 0), rect)
    
    def set_pos(self, pos: tuple[float, float]):
        self.__pos = np.array(pos, dtype=np.float32)//Grid.current_tile_size
        self.__camera_position = self.__pos.copy()
