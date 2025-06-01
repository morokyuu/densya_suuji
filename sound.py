import pygame
import threading
from pyo import *


class SoundPlayer:
    def __init__(self, filepath: str):
        self.sound_channels = {} # 各音ごとのチャンネルを保持する辞書
        self.filepath = filepath
        self.sound = pygame.mixer.Sound(self.filepath)

    def play(self):
        ch = self.sound_channels.get(self.sound)
        if ch is None or not ch.get_busy():
            self.sound_channels[self.sound] = self.sound.play()


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

    def close(self):
        self.server.stop()
        self.server.shutdown()




