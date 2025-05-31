import pygame
import threading

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

