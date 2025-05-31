import pygame
import sys
import threading
import time
from timer import TimeoutWatcher
from sound import SoundPlayer

WIDTH, HEIGHT = 640, 480
FPS = 30

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)



class Triangle:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT // 2
        self.speed_x = 5
        self.speed_y = 5

    def update(self, keys):
        self.x += self.speed_x
        if self.x > WIDTH:
            self.x = -20

        if keys[pygame.K_UP]:
            self.y -= self.speed_y
        if keys[pygame.K_DOWN]:
            self.y += self.speed_y

    def draw(self, surface):
        points = [
            (self.x, self.y),
            (self.x + 20, self.y - 15),
            (self.x + 20, self.y + 15)
        ]
        pygame.draw.polygon(surface, (255, 255, 0), points)


class BouncingCircle:
    def __init__(self):
        self.x = WIDTH // 2
        self.base_y = HEIGHT // 3
        self.y = self.base_y
        self.radius = 15
        self.direction = 1
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.motion_loop)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def motion_loop(self):
        while not self.stop_event.is_set():
            self.y += self.direction * 2
            if self.y > self.base_y + 20 or self.y < self.base_y - 20:
                self.direction *= -1
            time.sleep(0.03)

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 255), (self.x, int(self.y)), self.radius)



class StateControl:
    def __init__(self):
        self.cur_spd = 0
        self.spd_lim = 0
        self.state = 0

        self.stop_event = threading.Event()

        self.thread = threading.Thread(target=self._loop)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def inform_sign(self,new_spd):
        if self.state == 1:
            self.stop()
            raise("already in input state")
        if self.state == 2:
            self.stop()
            raise("already in result disp state")
        self.spd_lim = new_spd
        print(f"spd_lim={self.spd_lim}")
        self.state = 1

    def inform_curspd(self,new_spd):
        self.cur_spd = new_spd

    def _loop(self):
        while not self.stop_event.is_set():

            if self.state == 0:
                print("main")
                time.sleep(0.5)

            elif self.state == 1:
                # sign found
                print("start input state")
                tw = TimeoutWatcher(3)
                while not tw.is_timeout():
                    print("input state")
                    time.sleep(0.3)
                print("done")
                self.state = 2

            elif self.state == 2:
                # result disp
                print("start result disp state")

                result = ""
                if self.cur_spd > self.spd_lim:
                    result = "over limit"
                elif self.cur_spd < self.spd_lim * 0.8:
                    result = "delay occured"
                else:
                    result = "successed"

                tw = TimeoutWatcher(1)
                while not tw.is_timeout():
                    print(result)
                    time.sleep(0.3)
                print("done")
                self.state = 0

class Signs:
    def __init__(self):
        self.timer = 0
        self.INTERVAL = 200-1
        self.signs = [20,45,65,45,30]
        self.sidx = 0

    def is_found(self):
        self.timer += 1
        #print(self.timer)
        if self.timer > self.INTERVAL:
            self.timer = 0

            self.sidx += 1
            if self.sidx > len(self.signs)-1:
                self.sidx = 0
            return True
        return False

    @property
    def sign(self):
        return self.signs[self.sidx]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("電車シミュレータ")
        self.clock = pygame.time.Clock()

        self.running = True
        self.speed = 0

        self.stc = StateControl()
        self.stc.start()

        self.signs = Signs()

        self.font = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 80)
        self.yomifont = pygame.font.Font("C:/Windows/Fonts/meiryo.ttc", 50)

        self.bell = SoundPlayer("./sound/Bell.mp3")


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
        self.stc.inform_curspd(self.speed)

        if self.signs.is_found():
            self.stc.inform_sign(self.signs.sign)
            self.bell.play()

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.text = self.font.render(f"{self.speed}",True,WHITE)
        self.screen.blit(self.text, (int(WIDTH*0.17),int(HEIGHT*0.7)))

        pygame.display.flip()

    def cleanup(self):
        self.stc.stop()
        pygame.quit()
        print("quit")
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

