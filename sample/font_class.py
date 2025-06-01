import pygame
import time

WIDTH,HEIGHT = 640,480

class FontRenderer:
    def __init__(self, font_name=None, font_size=30, color=(255, 255, 255), antialias=True):
        self.font = pygame.font.Font(font_name, font_size)
        self.color = color
        self.antialias = antialias

    def render(self, text: str):
        surface = self.font.render(text, self.antialias, self.color)
        rect = surface.get_rect()
        return surface, rect

    def draw_center(self, surface, text, center_pos):
        text_surf, text_rect = self.render(text)
        text_rect.center = center_pos
        surface.blit(text_surf, text_rect)

    def draw_left(self, surface, text, topleft_pos):
        text_surf, text_rect = self.render(text)
        text_rect.topleft = topleft_pos
        surface.blit(text_surf, text_rect)





if __name__ == "__main__":

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("電車シミュレータ")
    
    font_name = "C:/Windows/Fonts/meiryo.ttc"
    fntr = FontRenderer(font_name=font_name,font_size=40)
    sfntr = FontRenderer(font_name=font_name,font_size=30,color=(120,200,100))
    
    screen.fill((0, 0, 0))

    #screen.blit(text, (100,100))
    
    fntr.draw_center(screen,"hogehoge",(WIDTH//2,HEIGHT//2))
    
    sfntr.draw_center(screen,"12345",(WIDTH//2,HEIGHT//2+50))

    pygame.display.flip()

    time.sleep(3)
