import pygame
import sys

class FontRenderer:
    def __init__(self, screen, font_name=None, font_size=100, color=(0, 0, 0), antialias=True):
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

    def draw_left(self, text, topleft_pos):
        text_surf, text_rect = self.render(text)
        text_rect.topleft = topleft_pos
        self.screen.blit(text_surf, text_rect)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("中央に標識")
clock = pygame.time.Clock()

# 白背景の画面、黒文字
font_renderer = FontRenderer(screen, font_size=100, color=(0, 0, 0))

# 白い標識のサイズと位置
sign_size = 200
sign_rect = pygame.Rect(0, 0, sign_size, sign_size)
sign_rect.center = (320, 240)  # 画面中央

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((150, 150, 150))  # グレー背景

    # 白い正方形（標識）
    pygame.draw.rect(screen, (255, 255, 255), sign_rect)

    # 中心に「45」
    font_renderer.draw_center("45", sign_rect.center)

    pygame.display.flip()
    clock.tick(60)
