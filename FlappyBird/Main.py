import pygame
import sprites
import random



class Game:
    def __init__(self) -> None:

        self._width = pygame.display.Info().current_w
        self._height = pygame.display.Info().current_h-60
        self.__screen = pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(pygame.image.load("Flappybird/bird/frame-1.png"))

        self.__font = pygame.font.SysFont("Playbill", 60)
        self.__gameOver_font = pygame.font.SysFont("Playbill", 70)

        self.__clock = pygame.time.Clock()
        self.__MAX_FPS = 30
        
        self.__sky = pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/sky.png"), (self._width, self._height/1.2))
        self.__backgrounds = [
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b1.png"), (self._width, self._height/2)),
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b2.png"), (self._width, self._height/3)),
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b3.png"), (self._width, self._height/4)),
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b4.png"), (self._width, self._height/4)),
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b5.png"), (self._width, self._height/6.5)),
            pygame.transform.scale(pygame.image.load("Flappybird/backgrounds/b6.png"), (self._width, self._height/9)),
        ]
        self.__background_x_positions = [0, 0, 0, 0, 0, 0]
        self.__background_x_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        self.__basicbackground_x_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        self.__drawedBackgrounds_count = 6
        
        self.__pipes = []
        self.__nextPipeX = random.randint(200, self._width/2)
        self.__pipeheight = self._height
        self.__pipewidth = self._width/7
        self.__maxPipeCount = 8
        self.__minPipeDistance = self._height//3

        self.__player = sprites.Player(self._height//10)
        self.__keys = pygame.key.get_pressed()

        self.__colortheme = random.randint(0, sprites.pipeimages.__len__()-1)
        self.__colorthemeStep = 1

        self.__speed = 1.0
        self.__tickCount = 0
        with open("Flappybird/data.txt", "r") as f:
            self.__highscore = int(f.readline())
        self.__currentX = 0

        self.__menuTile = pygame.transform.scale(pygame.image.load("Flappybird/menu/menuTile.png"), (500, 150))

        self.__running = True

    def __save(self):
        print("saving")
        with open("Flappybird/data.txt", "w") as f:
            f.write(str(self.__highscore))

    def _run(self) -> None:
        self.__mainloop()
    
    def __mainloop(self) -> None:
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
            self.__keys = pygame.key.get_pressed()
            self.__tick()
            self.__tickCount += 1
            self.__clock.tick(self.__MAX_FPS)
        self.__drawGameoverScreen()

    def __tick(self):
        self.__drawBackground()
        self.__speed += 0.01
        self.__player._update(self.__screen, self.__keys, self.__pipes, self)
        for i in range(len(self.__background_x_velocities)):
            self.__background_x_velocities[i] = self.__basicbackground_x_velocities[i] * self.__speed
        self.__currentX += self.__speed
        if self.__currentX % self.__colorthemeStep == 0:
            self.__colortheme = random.randint(0, sprites.pipeimages.__len__()-1)
        self.__update_pipes()
        self.__create_pipes()
        self.__highscore = max(self.__tickCount, self.__highscore)
        self.__screen.blit(self.__menuTile, (self._width-self.__menuTile.get_width()-10, 10))
        self.__screen.blit(self.__font.render("Score: " + str(int(self.__tickCount)), True, 0), (self._width - 450, 20))
        self.__screen.blit(self.__font.render("Highscore: " + str(int(self.__highscore)), True, 0), (self._width - 450, 80))
        if self.__keys[pygame.K_s]:
            self.__screen.blit(self.__font.render("FPS: " + str(int(self.__clock.get_fps())), True, (255, 255, 255)), (10, 20))
        pygame.display.flip()

    def __drawBackground(self):
        if(self.__tickCount % 100 == 0 and self.__tickCount > 10):
            self.__drawedBackgrounds_count = int(max(min(self.__clock.get_fps()/3, len(self.__backgrounds)), 1))   #je schneller desto mehr Hintergründe
        self.__screen.blit(self.__sky, (0, 0))
        for i in range(self.__drawedBackgrounds_count):
            self.__screen.blit(self.__backgrounds[i], (int(self.__background_x_positions[i]%self._width), int(self._height-self.__backgrounds[i].get_height())))
            self.__screen.blit(self.__backgrounds[i], (int(self.__background_x_positions[i]%self._width-self._width), int(self._height-self.__backgrounds[i].get_height())))
            self.__background_x_positions[i] -= self.__background_x_velocities[i]
            
    def __update_pipes(self):
        for i in range(len(self.__pipes)):
            self.__pipes[i]._update(self.__screen, self.__speed)

    def __create_pipes(self):
        if(len(self.__pipes) < self.__maxPipeCount):
            pipey = random.randint(self._height-self._height//2, self._height-self._height//8)
            pipedistance = random.randint(self.__minPipeDistance, self._height-self._height//8)
            self.__pipes.append(sprites.Pipe(self.__nextPipeX-self.__currentX, pipey, self.__pipewidth, self.__pipeheight, self.__colortheme))
            self.__pipes.append(sprites.Pipe(self.__nextPipeX - self.__currentX, max(pipey-pipedistance, self._height//8)-self.__pipeheight, self.__pipewidth, self.__pipeheight, self.__colortheme))
            self.__nextPipeX += random.randint(self._width//3.5, self._width//1.5)
        
        for pipe in self.__pipes:
            if(pipe._rect.x <= -pipe._rect.width):
                self.__pipes.remove(pipe)

    def _gameOver(self):
        self.__running = False

    def __drawGameoverScreen(self):
        self.__screen.blit(self.__menuTile, (self._width//2-self.__menuTile.get_width()//2, self._height//2-100))
        self.__screen.blit(self.__menuTile, (self._width//2-self.__menuTile.get_width()//2, self._height//2+50))
        self.__screen.blit(self.__gameOver_font.render("Press R/SPACE to restart", True, 0), (self._width//2-220, self._height//2-63))
        self.__screen.blit(self.__gameOver_font.render("Press Q/ESC to quit", True, 0), (self._width//2-180, self._height//2+85))
        pygame.display.flip()
        run = True
        while run:
            self.__clock.tick(self.__MAX_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.__save
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        self.__reset()
                        self.__mainloop()
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        run = False
                        self.__save()
        pygame.quit()
        exit()
    
    def __reset(self):
        self.__pipes = []
        self.__nextPipeX = random.randint(200, self._width/2)
        self.__background_x_positions = [0, 0, 0, 0, 0, 0]
        self.__background_x_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        self.__speed = 1.0
        self.__tickCount = 0
        self.__currentX = 0
        self.__running = True
        self.__colortheme = random.randint(0, sprites.pipeimages.__len__()-1)
        self.__player = sprites.Player(self._height//10)

if(__name__ == "__main__"):
    pygame.init()
    game = Game()
    game._run()
        