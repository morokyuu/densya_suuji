import pygame
import sys
import threading
import time

WIDTH, HEIGHT = 640, 480
FPS = 30


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
        self.stop_event = threading.Event()
        self.sign_event = threading.Event()
        self.thread = threading.Thread(target=self._loop)
        self.cur_spd = 0
        self.spd_lim = 0

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def key_input(self,keys):
        if keys[pygame.K_UP]:
            self.cur_spd += 1
        elif keys[pygame.K_DOWN]:
            self.cur_spd -= 1
        print(f"cur {self.cur_spd}")

    def sign(self,new_spd):
        self.spd_lim = new_spd
        self.sign_event.set()

    def monitor_time(self,duration, event):
        start_time = time.perf_counter()
        while not event.is_st():
            if time.perf_counter() - start_time >= duration:
                event.set()
                break

    def handler_sign_found(self,duration):
        timer_thread = threading.Thread(target=monitor_time, args=(duration, timeout_event))
        timer_thread.start()

    def _loop(self):
        while not self.stop_event.is_set():
            if self.sign_event.is_set():

                # sign found

                pass


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("クラス構造：三角形と青い丸")
        self.clock = pygame.time.Clock()
        self.running = True

        self.triangle = Triangle()
        self.circle = BouncingCircle()
        self.circle.start()

        self.stc = StateControl()
        self.stc.start()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        self.cleanup()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.running = False
        self.stc.key_input(keys)
        self.triangle.update(keys)

    def update(self):
        pass  # 現状、三角形はキーで更新される。必要なら他のロジック追加。

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.triangle.draw(self.screen)
        self.circle.draw(self.screen)
        pygame.display.flip()

    def cleanup(self):
        self.circle.stop()
        self.stc.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()

