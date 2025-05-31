import threading
import time

class TimeLimitedTask:
    def __init__(self,duration,task_func):
        self.timeout_event = threading.Event()
        self.stop_event = threading.Event()

        self.task_func = task_func
        timer_thread = threading.Thread(target=self.monitor_time, args=(duration, self.timeout_event))
        timer_thread.start()
        self.thread = threading.Thread(target=self._loop)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()

    def monitor_time(self,duration, event):
        start_time = time.perf_counter()
        while not event.is_set():
            if time.perf_counter() - start_time >= duration:
                event.set()
                break

    def _loop(self):
        while not self.timeout_event.is_set():
            self.task_func()
        print("timeout")


class TimeoutWatcher:
    def __init__(self,duration):
        self.duration = duration
        self.stop_event = threading.Event()
#        self.event = event
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

#    def handler_sign_found(self,duration):
#        timer_thread = threading.Thread(target=monitor_time, args=(duration, self.timeout_event))
#        timer_thread.start()

    def _loop(self):
        while not self.stop_event.is_set():
            print("start timer")
            tw = TimeoutWatcher(2)
            while not tw.flag:
                print("main")
                time.sleep(0.7)
#        while not self.stop_event.is_set():
#            if self.sign_event.is_set():
#                # sign found
#                pass

stc = StateControl()

time.sleep(6)
stc.stop()
pass
