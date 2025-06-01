import pygame
import threading
import time

WIDTH,HEIGHT = 640,480

GREEN = (0,180,0)
GLAY = (128,128,128)
CYAN = (0,240,240)
ORANGERED = (255,69,0)
FORESTGREEN = (34,139,34)
BROWN = (139,69,19)

FPS = 30

class Train:
    def __init__(self,screen):
        self.screen = screen
        self.pos = (120,124)
        self.height = 50
        self.length = 163

    def _wheel(self,x):
        wheel_d = 10
        pos = self.pos[0] + x, self.pos[1] + self.height + wheel_d
        pygame.draw.circle(self.screen, (100,100,130), pos, wheel_d)
        pos = self.pos[0] + x + 22, self.pos[1] + self.height + wheel_d
        pygame.draw.circle(self.screen, (100,100,130), pos, wheel_d)

        x += (self.length - (wheel_d*2 + 22))
        pos = self.pos[0] + x, self.pos[1] + self.height + wheel_d
        pygame.draw.circle(self.screen, (100,100,130), pos, wheel_d)
        pos = self.pos[0] + x + 22, self.pos[1] + self.height + wheel_d
        pygame.draw.circle(self.screen, (100,100,130), pos, wheel_d)

    def _car(self):
        self._wheel(10)
        rect_size = (self.length, self.height)
        pygame.draw.rect(self.screen, ORANGERED, pygame.Rect(*self.pos,*rect_size))

    def draw(self):
        self._car()

class Trees:
    def __init__(self,screen):
        self.screen = screen
        self.x = WIDTH + 40
        self.y = 140 

    def draw(self):
        width = 40
        height = 83 
        points = [
            (self.x, self.y),
            (self.x + width//2, self.y + width),
            (self.x - width//2, self.y + width)
        ]
        pygame.draw.polygon(self.screen, FORESTGREEN, points)
        rect_size = (8,50)
        pygame.draw.rect(self.screen, BROWN, pygame.Rect(self.x-4,self.y+40,*rect_size))
        

    def update(self):
        self.x -= 3

class Landscape:
    def __init__(self,screen):
        self.screen = screen
        self.pos = (0,124 + 50 + 20)
        self.height = 50
        self.length = 163

    def draw(self):
        skypos = (0,0)
        rect_size = (WIDTH,300)
        pygame.draw.rect(self.screen, CYAN, pygame.Rect(*skypos,*rect_size))
        rect_size = (WIDTH,130)
        pygame.draw.rect(self.screen, BROWN, pygame.Rect(*self.pos,*rect_size))



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("電車シミュレータ")
        self.clock = pygame.time.Clock()

        self.landscp = Landscape(self.screen)
        self.train = Train(self.screen)
        self.tree = Trees(self.screen)

        self.running = True
        self.speed = 0

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        self.cleanup()
        print("cleanup")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False

        if keys[pygame.K_UP]:
            self.speed += 1
            time.sleep(0.03)
            if self.speed > 100:
                self.speed = 100
        elif keys[pygame.K_DOWN]:
            self.speed -= 1
            time.sleep(0.03)
            if self.speed < 0:
                self.speed = 0

    def update(self):
        pass

    def draw(self):
        self.screen.fill((100, 0, 0))

        self.landscp.draw()
        self.tree.draw()
        self.train.draw()

        self.tree.update()

        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        print("quit")
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

