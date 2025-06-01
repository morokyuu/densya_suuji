import pygame
import time

pygame.init()
pygame.mixer.init()

# 音をロード
sound_a = pygame.mixer.Sound("../sound/クイズ正解5.mp3")
sound_b = pygame.mixer.Sound("../sound/クイズ不正解1.mp3")

# 各音ごとのチャンネルを保持する辞書
sound_channels = {}

def play_sound(sound):
    ch = sound_channels.get(sound)
    if ch is None or not ch.get_busy():
        sound_channels[sound] = sound.play()

# 使い方（例）:
play_sound(sound_a)  # sound_a を再生
#play_sound(sound_b)  # sound_b を再生（別の音なので同時再生OK）
play_sound(sound_a)  # sound_a がまだ鳴っていれば無視される（重複防止）

time.sleep(3)
