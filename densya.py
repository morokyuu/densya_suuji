import pygame
import sys
import threading
import time

# 初期設定
pygame.init()
WIDTH, HEIGHT = 640, 480
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("横スクロールする三角形と揺れる青い丸")
clock = pygame.time.Clock()

# 三角形の初期状態
triangle_x = 0
triangle_y = HEIGHT // 2
triangle_speed_x = 5
triangle_speed_y = 5

# 青い丸の位置（共有変数）
circle_x = WIDTH // 2
circle_base_y = HEIGHT // 3
circle_y = circle_base_y
circle_radius = 15

# スレッドで制御する揺れの関数
def circle_motion():
    global circle_y
    direction = 1
    while True:
        circle_y += direction * 2
        if circle_y > circle_base_y + 20 or circle_y < circle_base_y - 20:
            direction *= -1
        time.sleep(0.03)  # 約33FPSの動き

# スレッド起動
circle_thread = threading.Thread(target=circle_motion, daemon=True)
circle_thread.start()

# メインループ
running = True
while running:
    clock.tick(FPS)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        triangle_y -= triangle_speed_y
    if keys[pygame.K_DOWN]:
        triangle_y += triangle_speed_y

    # 横スクロール処理
    triangle_x += triangle_speed_x
    if triangle_x > WIDTH:
        triangle_x = -20  # 左から再登場

    # 描画処理
    screen.fill((0, 0, 0))  # 背景を黒にする

    # 三角形描画
    triangle_points = [
        (triangle_x, triangle_y),
        (triangle_x + 20, triangle_y - 15),
        (triangle_x + 20, triangle_y + 15)
    ]
    pygame.draw.polygon(screen, (255, 255, 0), triangle_points)

    # 青い丸の描画
    pygame.draw.circle(screen, (0, 0, 255), (circle_x, int(circle_y)), circle_radius)

    pygame.display.flip()

# 終了処理
pygame.quit()
sys.exit()

