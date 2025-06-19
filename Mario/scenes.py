import math
import numpy as np
import pygame as pg
from graphics_operator import get_images


class Scenehandler:

    """
    handles scenes: intro, 
    other scenes: game
    """

    __images = None

    @staticmethod
    def init(screen_size: tuple[int, int]):
        Scenehandler.__images = get_images("intro")
        Scenehandler.__images["background"] = pg.transform.scale(Scenehandler.__images["background"], screen_size)
        for i in range(1, 6):
            Scenehandler.__images[f"coin_f{i}"] = pg.transform.scale(
                Scenehandler.__images[f"coin_f{i}"], 
                (
                    int(screen_size[0] * 0.04),
                    int(screen_size[0] * 0.04)
                )
            )
            Scenehandler.__images[f"mario_f{i}"] = pg.transform.scale(
                Scenehandler.__images[f"mario_f{i}"], 
                (
                    int(screen_size[0] * 0.1),
                    int(screen_size[0] * 0.1)
                )
            )
        Scenehandler.__images["grass_full_block"] = pg.transform.scale(
            Scenehandler.__images["grass_full_block"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        Scenehandler.__images["grass_left_edge"] = pg.transform.scale(
            Scenehandler.__images["grass_left_edge"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        Scenehandler.__images["grass_right_edge"] = pg.transform.scale(
            Scenehandler.__images["grass_right_edge"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        Scenehandler.__images["grass_top"] = pg.transform.scale(
            Scenehandler.__images["grass_top"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        Scenehandler.__images["grass_left_corner"] = pg.transform.scale(
            Scenehandler.__images["grass_left_corner"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        Scenehandler.__images["grass_right_corner"] = pg.transform.scale(
            Scenehandler.__images["grass_right_corner"], 
            (
                int(screen_size[0] * 0.08),
                int(screen_size[0] * 0.08)
            )
        )
        
        Scenehandler.__intro_font = pg.font.Font("./Mario/Minecraft.ttf", int(screen_size[1] / 1.5))

        

    def __init__(self, camera_pos: np.ndarray = np.array([0, 0], dtype=np.float32), camera_follow_speed: float = 0.06) -> None:
        self.__image = None
        self.__current_tick = 0
        self.__current_scene = "intro"
        self.__camera_pos = camera_pos
        self.__wanted_camera_pos = camera_pos.copy()
        self.__camera_follow_speed = camera_follow_speed
        
            
    def set_scene(self, scene: str):
        self.__current_scene = scene
    
    def set_camera_follow_speed(self, speed: float):
        self.__camera_follow_speed = speed

    def get_image(self):
        return self.__image

    def get_current_scene(self):
        return self.__current_scene
    
    def render(self, screen_size):
        self.__camera_pos += (self.__wanted_camera_pos - self.__camera_pos) * self.__camera_follow_speed
        match self.__current_scene:
            case "intro":
                self.__render_intro(screen_size)
    
    def __render_intro(self, screen_size):
        self.__current_tick += 1
        block_size = self.__images["grass_full_block"].get_width()
        if self.__current_tick < 25:
            self.__image = self.__images["background"].copy()

            text_alpha = max(0, min(255, self.__current_tick*2 - 250))
            if text_alpha > 0:
                string = "Mario"
                colors = [
                    (255, 50, 50),
                    (50, 50, 255),
                    (50, 255, 50),
                    (255, 255, 50),
                    (255, 50, 255),
                ]
                x = screen_size[0]//2 - self.__intro_font.size(string)[0]//2
                for i in range(len(string)):
                    letter = string[i]
                    letter_image = self.__intro_font.render(letter, True, colors[i])
                    letter_image.set_alpha(text_alpha)
                    self.__image.blit(letter_image, (x, screen_size[1]/2.4 - letter_image.get_height()//2))
                    x += letter_image.get_width()

            for x in range(2, screen_size[0]//block_size - 1):
                for y in range(5, screen_size[1]//block_size + 1):
                    self.__image.blit(self.__images["grass_full_block"], (x * block_size, y * block_size))
            for x in range(2, screen_size[0]//block_size - 1):
                self.__image.blit(self.__images["grass_top"], (x * block_size, 4 * block_size))
            for y in range(5, screen_size[1]//block_size + 1):
                self.__image.blit(self.__images["grass_left_edge"], (block_size, y * block_size))
                self.__image.blit(self.__images["grass_right_edge"], ((screen_size[0]//block_size - 1) * block_size, y * block_size))
            self.__image.blit(self.__images["grass_left_corner"], (block_size, 4 * block_size))
            self.__image.blit(self.__images["grass_right_corner"], ((screen_size[0]//block_size - 1) * block_size, 4 * block_size))
            
            

            coin_frame_num = max(1, ((self.__current_tick - 100)//5))
            if coin_frame_num <= 5:
                self.__image.blit(self.__images[f"coin_f{coin_frame_num}"], (screen_size[0]//2 - self.__images["coin_f1"].get_width()//2, screen_size[1]//20))
            
            mario_start_y = 4*block_size - self.__images["mario_f1"].get_height() + 2
            mario_y = math.sin(max(0, min(math.pi, self.__current_tick/20 - 4.5)))*(mario_start_y - screen_size[1]//20 - self.__images["coin_f1"].get_height())
            mario_screen_y = mario_start_y - mario_y
            mario_frame_num = max(1,(math.ceil(math.sin(max(0, min(math.pi, self.__current_tick/20 - 4.5)))*5)))
            if mario_frame_num <= 5:
                self.__image.blit(self.__images[f"mario_f{mario_frame_num}"], (screen_size[0]//2 - self.__images["mario_f1"].get_width()//2, mario_screen_y))
            
            

            fade_alpha = max(0, min(255, 1500 - self.__current_tick*14))
            if fade_alpha > 0:
                fade_surface = pg.Surface((screen_size[0], screen_size[1]), pg.SRCALPHA)
                fade_surface.fill((0, 0, 0, fade_alpha))
                self.__image.blit(fade_surface, (0, 0))
        else:
            self.__current_scene = "game"
            self.__current_tick = 0

        
    
    def get_camera_position(self):
        return self.__camera_pos

    def move_camera(self, distance: np.ndarray):
        self.__wanted_camera_pos += distance
    
    def reset_camera(self):
        self.__wanted_camera_pos = np.array([0, 0])

    def set_camera_position(self, position: np.ndarray):
        self.__wanted_camera_pos = position