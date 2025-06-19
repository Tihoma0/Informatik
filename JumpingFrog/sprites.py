import pygame
import math


platformImage = pygame.image.load("JumpingFrog/images/platform.png")

class Platform:
    def __init__(self, x: int, y: int, absolutey: int, width: int, height: int) -> None:
        self.__image = pygame.transform.scale(platformImage, (width, height))
        self._rect = pygame.Rect(x, y, width, height + 7)
        self.__absolutey = absolutey
    
    def __draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__image, self._rect)

    def __move(self, currenty: int):
        self._rect.y = self.__absolutey - currenty
        
    def _update(self, screen: pygame.Surface, currenty: int):
        self.__move(currenty)
        self.__draw(screen)


class Player:
    def __init__(self, x: int, y: int, size: int) -> None:
        self.__base_image = pygame.transform.scale(pygame.image.load("JumpingFrog/images/Frog.png"), (size, size))
        self.__image = self.__base_image
        self.__size = size
        self.__currentY = 0
        self._rect = pygame.Rect(x, y, size, size//1.2)
        self.__vel_y = 0
        self.__vel_x = 0
        self.__friction = 1.05
        self.__airResistance = 1.1
        self.__abprallGeschwindigkeit = 2
        self.__acceleration = self.__size / 60
        self.__collided = {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False,
        }
        self.__GRAVITY = 0.7
        self.__jumppower = 14

    def __draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.__image, (self._rect.x, self._rect.y - 7))

    def __move(self, keys: list[bool], maxx: int = 0) -> None:
        if self.__collided["bottom"]:
            self.__vel_y = 0
            self.__vel_x /= self.__friction
            if keys[pygame.K_SPACE]:
                self.__vel_y = -self.__jumppower
        else:
            self.__vel_y+=self.__GRAVITY
        if self._rect.y > 200 or self.__vel_y > 0:
            self._rect.y += self.__vel_y
        else: self.__currentY += self.__vel_y

        if self.__collided["top"] and self.__vel_y < 0:
            self.__vel_x /= self.__friction
            self.__vel_y = -self.__vel_y

        if keys[pygame.K_a]:
            self.__vel_x -= self.__acceleration
            self.__image = self.__base_image
        if keys[pygame.K_d]:
            self.__vel_x += self.__acceleration
            self.__image = pygame.transform.flip(self.__base_image, True, False)

        self.__vel_x = min(self.__vel_x, 20)



        if self.__collided["left"]:
            self.__vel_x = self.__abprallGeschwindigkeit
        if self.__collided["right"]:
            self.__vel_x = -self.__abprallGeschwindigkeit
        
        self._rect.x += self.__vel_x
        self._rect.x = max(min(self._rect.x, maxx), 0)

        self.__vel_x /= self.__airResistance


    def __getCollosion(self, platforms: list[Platform]):
        self.__collided = {
            "left": False,
            "right": False,
            "top": False,
            "bottom": False,
        }
        for platform in platforms:
            if(self._rect.colliderect(platform._rect)):
                if self._rect.centery < platform._rect.centery + self.__vel_y:
                    self.__collided["bottom"] = True
                    self._rect.bottom = platform._rect.top + 1
                if self._rect.centery > platform._rect.centery + self.__vel_y:
                    self.__collided["top"] = True
                if self._rect.right < platform._rect.left + self.__vel_x + 2:
                    self.__collided["right"] = True
                if self._rect.left > platform._rect.right + self.__vel_x -2:
                    self.__collided["left"] = True
                

    def _update(self, screen: pygame.Surface, keys: list[bool], platforms: list[Platform], maxx: int = 0):
        self.__getCollosion(platforms)
        self.__move(keys, maxx)
        self.__draw(screen)

    def _getCurrentY(self)-> int:
        return self.__currentY
    
    def _getY(self):
        return self._rect.y
    
    def _reset(self, x: int, y: int):
        self._rect.x = x
        self._rect.y = y
        self.__vel_y = 0
        self.__vel_x = 0
        self.__currentY = 0

