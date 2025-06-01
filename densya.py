import pygame
import sys
import threading
import time
from timer import TimeoutWatcher
from sound import MotorSound
from sound import SoundPlayer
from enum import Enum
from font import FontRenderer

## sound effect from
## https://soundeffect-lab.info/

WIDTH, HEIGHT = 640, 480
FPS = 30

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)


RESULT_DISP_DURATION = 0.8

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


class SC_State(Enum):
    RUN = 0
    SIGN = 1
    RESULT = 2

class Result(Enum):
    SUCCESS = 0
    OVERLIM = 1
    DELAYED = 2

class StateControl:
    def __init__(self):
        self.cur_spd = 0
        self.spd_lim = 0
        self.state = SC_State.RUN
        self.result = Result.SUCCESS

        self.stop_event = threading.Event()

        self.thread = threading.Thread(target=self._loop)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def inform_sign(self,new_spd):
        if self.state == SC_State.SIGN:
            self.stop()
            raise("already in input state")
        if self.state == SC_State.RESULT:
            self.stop()
            raise("already in result disp state")
        self.spd_lim = new_spd
        print(f"spd_lim={self.spd_lim}")
        self.state = SC_State.SIGN

    def inform_curspd(self,new_spd):
        self.cur_spd = new_spd
    
    def get_state(self):
        return self.state, self.result

    def _loop(self):
        while not self.stop_event.is_set():

            if self.state == SC_State.RUN:
                print("main")
                time.sleep(0.3)

            elif self.state == SC_State.SIGN:
                # sign found
                print("start input state")
                tw = TimeoutWatcher(2)
                while not tw.is_timeout():
                    print("input state")
                    time.sleep(0.3)
                print("done")
                self.state = SC_State.RESULT

            elif self.state == SC_State.RESULT:
                # result disp
                print("start result disp state")

                if self.cur_spd > self.spd_lim:
                    print("over limit")
                    self.result = Result.OVERLIM
                elif self.cur_spd < self.spd_lim * 0.8:
                    print("delay occured")
                    self.result = Result.DELAYED
                else:
                    print("successed")
                    self.result = Result.SUCCESS

                tw = TimeoutWatcher(RESULT_DISP_DURATION)
                while not tw.is_timeout():
                    print(self.result)
                    time.sleep(0.3)
                print("done")
                self.state = SC_State.RUN


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


class SpeedMeter:
    def __init__(self,screen):
        font_name = "C:/Windows/Fonts/meiryo.ttc"
        self.fnt_spd = FontRenderer(screen,font_name=font_name,font_size=70)
        self.fnt_yomi = FontRenderer(screen,font_name=font_name,font_size=30)

    def draw(self,speed):
        meter_pos = (int(WIDTH*0.17),int(HEIGHT*0.7))
        self.fnt_spd.draw_center(f"{speed}",meter_pos)
        self.fnt_yomi.draw_center("はやさ",(meter_pos[0],meter_pos[1]+85))


class SignDisplay:
    def __init__(self,screen):
        self.screen = screen
        self.size = 100
        self.bg_color = (255,255,255)
        self.border_color = (0, 0, 0)
        self.border_width = 4
        font_name = "C:/Windows/Fonts/meiryo.ttc"
        self.fnt_spd = FontRenderer(screen,font_name=font_name,font_size=70,color=(0,0,0))

    def draw(self,speed):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (int(WIDTH*0.84),int(HEIGHT*0.7))
        pygame.draw.rect(self.screen, self.bg_color, rect)
        pygame.draw.rect(self.screen, self.border_color, rect, width=self.border_width)
        self.fnt_spd.draw_center(f"{speed}", rect.center)



class ResultDisplay:
    def __init__(self,screen):
        self.snd_success = SoundPlayer("./sound/クイズ正解5.mp3")
        self.snd_delayed = SoundPlayer("./sound/警告音1.mp3")
        self.snd_overlim = SoundPlayer("./sound/クイズ不正解1.mp3")

        self.result_msg = {
                Result.SUCCESS:"successed",
                Result.OVERLIM:"over limit",
                Result.DELAYED:"delayed"
                }
        self.result_sound = {
                Result.SUCCESS:self.snd_success.play,
                Result.OVERLIM:self.snd_overlim.play,
                Result.DELAYED:self.snd_delayed.play
                }

        font_name = "C:/Windows/Fonts/meiryo.ttc"
        self.fnt_result = FontRenderer(screen,font_name=font_name,font_size=60)

    def show(self,result):
        self.fnt_result.draw_center(f"{self.result_msg[result]}",(WIDTH//2,HEIGHT//2))
        self.result_sound[result]()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("電車シミュレータ")
        self.clock = pygame.time.Clock()

        self.running = True
        self.speed = 0
        self.spd_meter = SpeedMeter(self.screen)
        self.res_display = ResultDisplay(self.screen)
        self.sign_display = SignDisplay(self.screen)

        self.stc = StateControl()
        self.stc.start()

        self.signs = Signs()

        self.snd_bell = SoundPlayer("./sound/Bell.mp3")
        self.snd_bell.play()

        self.motor = MotorSound()
        self.motor.on()


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

        self.motor.set_speed(self.speed)

        if self.signs.is_found():
            self.stc.inform_sign(self.signs.sign)
            self.snd_bell.play()



    def draw(self):
        self.screen.fill((0, 0, 0))

        state,result = self.stc.get_state()
        if state == SC_State.SIGN:
            self.sign_display.draw(self.signs.sign)
        elif state == SC_State.RESULT:
            self.res_display.show(result)

        self.spd_meter.draw(self.speed)
        #self._draw_speed_meter(self.speed)

        pygame.display.flip()

    def cleanup(self):
        self.stc.stop()
        pygame.quit()
        self.motor.close()
        print("quit")
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()



