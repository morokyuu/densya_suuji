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
        self.flag = False
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()

    def halt(selt):
        self.stop_event.set()

    def _watch(self):
        start_time = time.perf_counter()
        while not self.stop_event.is_set():
            if time.perf_counter() - start_time >= self.duration:
                self.stop_event.set()
                self.flag = True
                break
            
    def is_timeout(self):
        return self.flag



