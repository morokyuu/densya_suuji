import threading
import time
from timer import TimeoutWatcher



class StateControl:
    def __init__(self):
        self.cur_spd = 0
        self.spd_lim = 0
        self.state = 0

        self.stop_event = threading.Event()

        self.thread = threading.Thread(target=self._loop)
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
                    print("running")
                    time.sleep(0.3)
                print("done")
                self.state = 2

            elif self.state == 2:
                # result disp
                print("start result disp state")
                tw = TimeoutWatcher(1)
                while not tw.is_timeout():
                    print("running")
                    time.sleep(0.3)
                print("done")
                self.state = 0

stc = StateControl()

time.sleep(2)
stc.inform_sign(30)
time.sleep(1)
stc.inform_sign(50)
time.sleep(5)

stc.stop()
pass
