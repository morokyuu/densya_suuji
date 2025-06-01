import pygame
import time


class SoundPlayer:
    def __init__(self, filepath: str):
        self.sound_channels = {} # 各音ごとのチャンネルを保持する辞書
        self.filepath = filepath
        self.sound = pygame.mixer.Sound(self.filepath)

    def play(self):
        ch = self.sound_channels.get(self.sound)
        if ch is None or not ch.get_busy():
            self.sound_channels[self.sound] = self.sound.play()



pygame.init()
pygame.mixer.init()

# 音をロード
sound_a = SoundPlayer("../sound/クイズ正解5.mp3")
sound_b = SoundPlayer("../sound/クイズ不正解1.mp3")

sound_a.play()
sound_a.play()

time.sleep(3)
