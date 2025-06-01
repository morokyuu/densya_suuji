import pygame
import time

class FontRenderer:
    def __init__(self, screen, font_name=None, font_size=30, color=(255, 255, 255), antialias=True):
        self.screen = screen
        self.font = pygame.font.Font(font_name, font_size)
        self.color = color
        self.antialias = antialias

    def render(self, text: str):
        surface = self.font.render(text, self.antialias, self.color)
        rect = surface.get_rect()
        return surface, rect

    def draw_center(self, text, center_pos):
        text_surf, text_rect = self.render(text)
        text_rect.center = center_pos
        self.screen.blit(text_surf, text_rect)

    def draw_left(self, surface, text, topleft_pos):
        text_surf, text_rect = self.render(text)
        text_rect.topleft = topleft_pos
        self.screen.blit(text_surf, text_rect)





if __name__ == "__main__":

    WIDTH,HEIGHT = 640,480

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("電車シミュレータ")
    
    font_name = "C:/Windows/Fonts/meiryo.ttc"
    fntr = FontRenderer(screen, font_name=font_name,font_size=40)
    sfntr = FontRenderer(screen, font_name=font_name,font_size=30,color=(120,200,100))
    
    screen.fill((0, 0, 0))

    fntr.draw_center("hogehoge",(WIDTH//2,HEIGHT//2))
    sfntr.draw_center("12345",(WIDTH//2,HEIGHT//2+50))

    pygame.display.flip()

    time.sleep(3)
