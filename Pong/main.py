import math
import pygame as pg
from gui import Button
from enum import Enum
from random import randint, choice

pg.init()

class Paddle:

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0, color: tuple[int, int, int] = (255, 255, 255), maxYVelocity: tuple[float, float] = (-3, 3), maxYMovement: tuple[int, int] = (0, 0), keyForUpMoving: int = pg.K_UP, keyForDownMoving = pg.K_DOWN, acceleration: float = 1.0) -> None:
        self._rect = pg.Rect(x, y, width, height)
        self.__color = color
        self._velY = 0.0
        self.__maxYMovement = maxYMovement
        self.__K_up = keyForUpMoving
        self.__k_down = keyForDownMoving
        self.__acceleration = acceleration
        self.__maxVelocity = maxYVelocity

    def _setColor(self, color: tuple[int, int, int] = (255, 255, 255)):
        self.__color = color

    def _draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.__color, (self._rect.x, self._rect.y + 5, self._rect.width, self._rect.height - 10))
    
    def _update(self, keys: list[bool]):
        if(keys[self.__k_down]):
            self._velY += self.__acceleration
        if(keys[self.__K_up]):
            self._velY -= self.__acceleration

        self._velY = max(self.__maxVelocity[0], min(self.__maxVelocity[1], self._velY))

        self._velY /= 1.1
        self._rect.y = max(self.__maxYMovement[0], min(self.__maxYMovement[1] - self._rect.height, self._rect.y + self._velY))
        

class Ball:

    def __init__(self, x: int, y: int, radius: int, color: tuple[int, int, int], velocity: list[int, int]) -> None:
        self.__position = [x, y]
        self.__radius = radius
        self.__color = color
        self.__velocity = velocity
        self.__accelerarionOnTouchWithPaddle = -1 - 0.01
        self.__rect = pg.Rect(x - radius, y - radius, radius*2, radius*2)
        self.__score = 0

    def _draw(self, screen: pg.Surface):
        pg.draw.circle(screen, self.__color, self.__position, self.__radius)
        pg.draw.rect(screen, (255, 0, 0), self.__rect)

    def _update(self, paddles: list[Paddle], maxY: int = 0, timestep: float = 1.0):
        if self.__position[1] < 0:
            self.__position[1] = 1
            self.__velocity[1] *= -1
        if self.__position[1] > maxY:
            self.__position[1] = maxY - 1
            self.__velocity[1] *= -1
        for paddle in paddles:
            if paddle._rect.colliderect(self.__rect):
                if self.__rect.centerx > paddle._rect.centerx:
                    self.__rect.left = paddle._rect.right + 1
                else:
                    self.__rect.right = paddle._rect.left - 1
                self.__position[0] = self.__rect.centerx
                self.__velocity[0] *= self.__accelerarionOnTouchWithPaddle
                self.__velocity[1] += (paddle._velY - self.__velocity[1])/2
                self.__score += 1
            
        self.__position[0] += self.__velocity[0]*timestep
        self.__position[1] += self.__velocity[1]*timestep
        self.__rect.centerx = self.__position[0]
        self.__rect.width = self.__radius*2 + abs(self.__velocity[0]*timestep)
        self.__rect.centery = self.__position[1]

    def get_score(self) -> int:
        return self.__score

    def get_x(self) -> int:
        return self.__rect.centerx
        

class BUTTON_ID(Enum):
    QUIT = 1
    TEST = 2
    RESTART = 4



class Game:

    def __init__(self):
        self.__width = pg.display.Info().current_w
        self.__height = pg.display.Info().current_h - 60

        self.__screen = pg.display.set_mode((self.__width, self.__height))
        pg.display.set_caption("Pong")
        pg.display.set_icon(pg.image.load("Pong/icon.png"))

        self.__font = pg.font.SysFont("Sans MS", 150, True)
        self.__score_color = (255, 255, 255)

        self.__clock = pg.time.Clock()
        self.__MAX_FPS = 6000

        self.__keys = pg.key.get_pressed()
        self.__mousepos = pg.mouse.get_pos()
        self.__mousebuttons = pg.mouse.get_pressed()

        self.__tickCount = 0
        self.__score = 0
        self.__data = self.__load()
        if self.__data == "":
            self.__data = "0"
        self.__highscore = int(self.__data)
        self.__running = False

        self.__paddles = [
            Paddle(x = self.__width/1.1, y = self.__height//2 - self.__height//20, width = 30, height = self.__height//8, color = (255, 100, 10), maxYMovement = (0, self.__height), acceleration=self.__height/600.0, maxYVelocity = (-self.__height//50, self.__height//50)),
            Paddle(x = self.__width - self.__width/1.1, y = self.__height//2 - self.__height//20, width = 30, height = self.__height//8, color = (255, 100, 10), maxYMovement = (0, self.__height), acceleration=self.__height/600.0, maxYVelocity = (-self.__height//50, self.__height//50), keyForDownMoving=pg.K_s, keyForUpMoving=pg.K_w)
        ]
        ballColor = (255, 100, 100)
        ball_direction = choice([randint(-100, 100)/100000  + math.pi, randint(-100, 100)/100000])
        ballVelocity = [math.cos(ball_direction)*self.__width/300, math.sin(ball_direction)*self.__width/500]
        self.__ball = Ball(self.__width//2, self.__height//2 - 0, 10, ballColor, ballVelocity)

        # menu
        self.__menu_buttons = [
            Button(pg.Rect(self.__width//2 - self.__width//7 - self.__width//10, self.__height//2 - self.__height//10/2, self.__width//7, self.__height//10), [(100, 100, 100), (150, 150, 150), (255,255, 255)], self._button_function, BUTTON_ID.QUIT, "Quit", pg.font.SysFont("Sans MS", 40), [(255, 255, 255), (0, 0, 0), (0, 0, 0)]),
            Button(pg.Rect(self.__width//2 + self.__width//10, self.__height//2 - self.__height//10/2, self.__width//7, self.__height//10), [(100, 100, 100), (150, 150, 150), (255,255, 255)], self._button_function, BUTTON_ID.RESTART, "Restart", pg.font.SysFont("Sans MS", 40), [(255, 255, 255), (0, 0, 0), (0, 0, 0)])
        ]

        self.__timestep = 0.01  # iterativer Physiklöser
    
    def _button_function(self, id: int):
        match id:
            case BUTTON_ID.QUIT:
                self.__save()
                quit()
            case BUTTON_ID.TEST:
                self.__game_over()
            case BUTTON_ID.RESTART:
                self.__restart()

    def __save(self):
        with open("Pong/data.txt", "w") as f:
            f.write(str(self.__highscore))
        
    def __load(self) -> int:
        data = 0
        with open("Pong/data.txt", "r") as f:
            data = f.readline()
        return data
    
    def _run(self) -> None:
        self.__running = True
        self.__mainloop()
    
    def __mainloop(self) -> None:
        while self.__running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
            self.__poll_events()
            self.__tick()
            self.__render()
            
            self.__tickCount += 1
            self.__clock.tick(self.__MAX_FPS)
        self.__save()
        pg.quit()
        quit()

    def __poll_events(self):
        self.__keys = pg.key.get_pressed()
        self.__mousepos = pg.mouse.get_pos()
        self.__mousebuttons = pg.mouse.get_pressed()

    def __tick(self):
        self.__highscore = max(self.__score, self.__highscore)
        self.__score_color = (255, 255, 0) if self.__score== self.__highscore else (255, 255, 255)
        for paddle in self.__paddles:
            paddle._update(self.__keys)
        for i in range(math.ceil(1/self.__timestep)):
            self.__ball._update(self.__paddles, self.__height, self.__timestep)
        self.__score = self.__ball.get_score()
        if not 0 < self.__ball.get_x() < self.__width:
            self.__game_over()
            

    def __render(self):
        self.__screen.fill(0)
        if self.__keys[pg.K_f]:
            self.__screen.blit(self.__font.render("FPS: " + str(int(self.__clock.get_fps())), True, (255, 255, 255)), (10, 20))
        for paddle in self.__paddles:
            paddle._draw(self.__screen)
        self.__ball._draw(self.__screen)
        text = self.__font.render(str(self.__score) + " / " + str(self.__highscore), False, self.__score_color)
        self.__screen.blit(text, (self.__width//2 - text.get_width()//2, 20))
        for button in self.__menu_buttons:
                button._update(self.__mousepos, self.__mousebuttons)
        pg.display.flip()

    def __game_over(self):
        self.__running = False
        gameover_running = True
        while gameover_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameover_running = False
            self.__poll_events()
            for button in self.__menu_buttons:
                button._update(self.__mousepos, self.__mousebuttons)
                button._draw(self.__screen)
            pg.display.flip()
            self.__clock.tick(self.__MAX_FPS)
        self.__save()
        pg.quit()
        quit()

    def __restart(self):
        self.__paddles = [
            Paddle(x = self.__width/1.1, y = self.__height//2 - self.__height//20, width = 30, height = self.__height//8, color = (255, 100, 10), maxYMovement = (0, self.__height), acceleration=self.__height/600.0, maxYVelocity = (-self.__height//50, self.__height//50)),
            Paddle(x = self.__width - self.__width/1.1, y = self.__height//2 - self.__height//20, width = 30, height = self.__height//8, color = (255, 100, 10), maxYMovement = (0, self.__height), acceleration=self.__height/600.0, maxYVelocity = (-self.__height//50, self.__height//50), keyForDownMoving=pg.K_s, keyForUpMoving=pg.K_w)
        ]
        ballColor = (255, 100, 100)
        ball_direction = choice([randint(-100, 100)/100 + math.pi, randint(-100, 100)/100])
        ballVelocity = [math.cos(ball_direction)*self.__width/300, math.sin(ball_direction)*self.__width/500]
        self.__ball = Ball(self.__width//2, self.__height//2 - 0, 10, ballColor, ballVelocity)
        self.__score = 0
        self._run()


if __name__ == "__main__":
    game = Game()
    game._run()