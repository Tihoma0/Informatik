import math
from typing import Any
import pygame
pygame.init()

pipeimages = [
            pygame.image.load("Flappybird/Pipes/blue.png"),
            pygame.image.load("Flappybird/Pipes/green.png"),
            pygame.image.load("Flappybird/Pipes/grey.png"),
            pygame.image.load("Flappybird/Pipes/purple.png"),
            pygame.image.load("Flappybird/Pipes/red.png"),
            pygame.image.load("Flappybird/Pipes/yellow.png"),
        ]

class Pipe:
    def __init__(self, x: int, y: int, width: int, height: int, colortheme: int) -> None:
        self.__image = pygame.transform.scale(pipeimages[colortheme], (width, height))
        self._rect = pygame.Rect(x, y, width, height)
        self.__x = x #because of the handling of pygame.Rects, the x and y vales are integers -> this is a float

    def __draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__image, (self.__x, self._rect.y))

    def __move(self, speed: float):
        self.__x -= speed
        self._rect.x = self.__x

    def _update(self, screen: pygame.Surface, speed: float):
        self.__move(speed)
        self.__draw(screen)

class Player:
    def __init__(self, size: int) -> None:
        self.__images = [
            pygame.transform.scale(pygame.image.load("Flappybird/bird/frame-1.png"), (size, size)),
            pygame.transform.scale(pygame.image.load("Flappybird/bird/frame-2.png"), (size, size)),
        ]
        self.__size = size
        self.__image = self.__images[0]
        self._rect = pygame.Rect(100, pygame.display.Info().current_h//2, size, size//1.2)
        self.__vel_y = 0
        self.__startx = 100
        self.__GRAVITY = 1.2
        self.__spacePressed = False
        self.__tickCount = 0
        self.__spacetickCount = 0

    def __draw(self, screen: pygame.Surface) -> None:
        if self.__vel_y < 0:
            self.__image = self.__images[1]
        else:
            self.__image = self.__images[0]
        screen.blit(self.__image, (self._rect.x, self._rect.y-5))

    def __move(self, keys: list[bool]) -> None:
        self.__vel_y+=self.__GRAVITY
        self.__spacetickCount += 1
        if(self.__spacetickCount >5 and not keys[pygame.K_SPACE]):
            self.__spacePressed = False
            self.__spacetickCount = 0
        
        if(keys[pygame.K_SPACE] and self.__vel_y > -4 and not self.__spacePressed):
            self.__spacePressed = True
            self.__spacetickCount = 0
            self.__vel_y = -self.__size/6
        self._rect.y += self.__vel_y
        self._rect.x = self.__startx + math.cos(self.__tickCount/40)*40

    def __getCollosion(self, pipes: list[Pipe], game):
        if self._rect.y < 0:
            game._gameOver()
        elif self._rect.y > game._height:
            game._gameOver()
        for pipe in pipes:
            if(self._rect.colliderect(pipe._rect)):
                game._gameOver()

    def _update(self, screen: pygame.Surface, keys: list[bool], pipes: list[Pipe], game):
        self.__move(keys)
        self.__getCollosion(pipes, game)
        self.__draw(screen)
        self.__tickCount += 1

