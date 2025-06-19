import pygame
import sprites
import random

pygame.init()

class Game:
    def __init__(self) -> None:

        self._width = pygame.display.Info().current_w
        self._height = pygame.display.Info().current_h-60
        self.__screen = pygame.display.set_mode((self._width, self._height), pygame.DOUBLEBUF)
        pygame.display.set_caption("Jumping Frog")
        pygame.display.set_icon(pygame.image.load("JumpingFrog/images/Frog.png"))

        self.__font = pygame.font.SysFont("Playbill", 60)
        self.__gameOver_font = pygame.font.SysFont("Playbill", 100)

        self.__clock = pygame.time.Clock()
        self.__MAX_FPS = 60

        self.__currentY = 0
        self.__highscore = self.__load()
        
        self.__background = pygame.transform.scale(pygame.image.load("JumpingFrog/images/hg.png"), (self._width, self._height))
        self.__menuTile = pygame.transform.scale(pygame.image.load("JumpingFrog/images/menuTile.png"), (500, 150))

        
        self.__maxPlatforms = 30
        self.__nextPlatformx = self._width//2
        self.__nextPlatformy = self._height/1.4
        self.__platforms = [sprites.Platform(self._width//2 - self._width//6, self._height - self._height//5, self._height - self._height //6, self._width//3, self._height //70)]
        for i in range(self.__maxPlatforms):
            self.__platforms.append(self.__createNewPlatform())

        self.__player = sprites.Player(self._width//2, self._height - self._height//5, self._width//30)
        self.__keys = pygame.key.get_pressed()

        self.__tickCount = 0
        with open("JumpingFrog/data.txt", "r") as f:
            self.__highscore = int(f.readline())

        #self.__menuTile = pygame.transform.scale(pygame.image.load("JumpingFrog/imags/menuTile.png"), (500, 150)) TODO: menuTile

        self.__running = True

    def __save(self):
        with open("JumpingFrog/data.txt", "w") as f:
            f.write(str(self.__highscore))
        
    def __load(self) -> int:
        data = 0
        with open("JumpingFrog/data.txt", "r") as f:
            data = f.readline()
        return data


    def _run(self) -> None:
        self.__mainloop()
    
    def __mainloop(self) -> None:
        while self.__running:
            self.__drawBackground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
            self.__keys = pygame.key.get_pressed()
            self.__tick()
            
            self.__tickCount += 1
            self.__clock.tick(self.__MAX_FPS)
        self.__save()
        self.__drawGameoverScreen()

    def __tick(self):
        self.__currentY = self.__player._getCurrentY()
        self.__player._update(self.__screen, self.__keys, self.__platforms, self._width)
        if self.__keys[pygame.K_s]:
            self.__screen.blit(self.__font.render("FPS: " + str(int(self.__clock.get_fps())), True, (255, 255, 255)), (10, 20))
        
        if self.__player._getY() > self._height:
            self.__gameOver()

        self.__highscore = max(int(self.__currentY//-10), self.__highscore)
        self.__updatePlatforms()
        self.__drawScore()
        pygame.display.flip()

    def __drawBackground(self):
        self.__screen.blit(self.__background, (0, self.__currentY//-2%self._height))
        self.__screen.blit(self.__background, (0, self.__currentY//-2%self._height - self._height))
    
    def __drawScore(self):
        self.__screen.blit(self.__menuTile, (self._width - self._width//3.5, 0))
        self.__screen.blit(self.__font.render("Score: " + str(int(self.__currentY//-10)), False, 0), (self._width - self._width//4, 10))
        self.__screen.blit(self.__font.render("HighScore: " + str(int(self.__highscore)), False, 0), (self._width - self._width//4, 60))


    def __updatePlatforms(self):
        for platform in self.__platforms:
            platform._update(self.__screen, self.__currentY)
            if platform._rect.y > self._height * 1.5:
                self.__platforms.remove(platform)
                self.__platforms.append(self.__createNewPlatform())

    def __createNewPlatform(self) -> sprites.Platform:
        width = random.randint(self._width//50, self._width//15)
        height = self._height //70
        result = sprites.Platform(self.__nextPlatformx, self.__nextPlatformy - self.__currentY, self.__nextPlatformy, width, height)
        self.__nextPlatformx += random.randint(- self._width//8, self._width//8)
        self.__nextPlatformy -= random.randint(self._height//13, self._height//8)
        self.__nextPlatformx = max(self._width//30, min(self._width - self._width//30, self.__nextPlatformx))

        return result
    
    def __gameOver(self):
        self.__running = False

    def __reset(self):
        self.__nextPlatformx = self._width//2
        self.__nextPlatformy = self._height/1.4
        self.__platforms = [sprites.Platform(self._width//2 - self._width//6, self._height - self._height//5, self._height - self._height //6, self._width//3, self._height //70)]
        for i in range(self.__maxPlatforms):
            self.__platforms.append(self.__createNewPlatform())
        self.__player._reset(self._width//2, self._height - self._height//5)
        self.__currentY = 0
        self.__running = True

    def __drawGameoverScreen(self):
        self.__screen.blit(self.__menuTile, (self._width//2-self.__menuTile.get_width()//2, self._height//2-100))
        self.__screen.blit(self.__menuTile, (self._width//2-self.__menuTile.get_width()//2, self._height//2+50))
        self.__screen.blit(self.__gameOver_font.render("Press R to restart", True, 0), (self._width//2-230, self._height//2-80))
        self.__screen.blit(self.__gameOver_font.render("Press Q to quit", True, 0), (self._width//2-200, self._height//2+70))
        pygame.display.flip()
        run = True
        while run:
            self.__clock.tick(self.__MAX_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.__save
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__reset()
                        self._run()
                        run = False
                    if event.key == pygame.K_q:
                        run = False
                        self.__save()
        pygame.quit()
        exit()
    


if __name__ == "__main__":
    Game()._run()