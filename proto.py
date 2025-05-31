import threading
import time
from timer import TimeoutWatcher



class StateControl:
    def __init__(self):
        self.cur_spd = 0
        self.spd_lim = 0

        self.stop_event = threading.Event()
        self.sign_event = threading.Event()

        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def inform_sign(self,new_spd):
        self.spd_lim = new_spd
        print(f"spd_lim={self.spd_lim}")
        self.sign_event.set()

    def _loop(self):
        while not self.stop_event.is_set():
            print("main")
            time.sleep(0.2)
            if self.sign_event.is_set():
                self.sign_event.clear()
                print("start timer")
                tw = TimeoutWatcher(2)
                while not tw.is_timeout():
                    print("running")
                    time.sleep(0.7)
                print("done")

stc = StateControl()

time.sleep(2)
stc.inform_sign(30)
time.sleep(3)
stc.inform_sign(50)
time.sleep(3)

stc.stop()
pass
