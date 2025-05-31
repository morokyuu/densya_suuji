import threading
import time

class TimeoutWatcher:
    def __init__(self,duration):
        self.duration = duration
        self.stop_event = threading.Event()
        self.flag = False
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()

    def _watch(self):
        start_time = time.perf_counter()
        while not self.stop_event.is_set():
            if time.perf_counter() - start_time >= self.duration:
                print("timeout event")
                self.stop_event.set()
                self.flag = True
                break
            
    def is_timeout(self):
        return self.flag


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

    def _loop(self):
        while not self.stop_event.is_set():
            print("start timer")
            tw = TimeoutWatcher(2)
            while not tw.flag:
                print("running")
                time.sleep(0.7)
            print("done")

stc = StateControl()

time.sleep(6)
stc.stop()
pass
