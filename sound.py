import pygame
import threading
from pyo import *


class SoundPlayer:
    def __init__(self, filepath: str):
        pygame.init()
        pygame.mixer.init()
        self.filepath = filepath
        pygame.mixer.music.load(self.filepath)

    def play(self, loop=False):
        pygame.mixer.music.play(-1 if loop else 0)
        if not loop:
            threading.Thread(target=self._wait_until_finished, daemon=True).start()

    def stop(self):
        pygame.mixer.music.stop()

    def _wait_until_finished(self):
        """再生が終わるまで待機（別スレッドで実行）"""
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)



class MotorSound:
    def __init__(self, base_freq=300.0, freq_scale=5.0, volume=0.2):
        # 音の周波数 = base_freq + speed * freq_scale
        self.base_freq = base_freq
        self.freq_scale = freq_scale

        # Pyoサーバー起動
        self.server = Server().boot()
        self.server.start()

        # 再生用周波数信号（初期値）
        self._freq = Sig(self.base_freq)

        # サイン波発振器
        self._osc = Sine(freq=self._freq, mul=volume)

        # 初期状態ではオフ
        self._is_playing = False

    def on(self):
        if not self._is_playing:
            self._osc.out()
            self._is_playing = True

    def off(self):
        if self._is_playing:
            self._osc.stop()
            self._is_playing = False

    def set_speed(self, speed: float):
        freq = self.base_freq + speed * self.freq_scale
        self._freq.setValue(freq)

    def __del__(self):
        self.server.stop()
        self.server.shutdown()




