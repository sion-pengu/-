import pygame
import requests
import sys
import random
import math

# 天気取得
def get_weather(city_name):
    api_key = "97765018c3201fde5333bf25ec8a5b72"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        weather = data["weather"][0]["main"]
        print(f"現在の天気: {weather}")
        return weather
    except Exception as e:
        print("天気データ取得エラー:", e)
        return "Clear"

# 敵の形を描画 
def draw_enemy(surface, rect, weather):
    if weather == "Clear":
        pygame.draw.circle(surface, (255, 165, 0), rect.center, rect.width // 2)
    elif weather == "Rain":
        pygame.draw.ellipse(surface, (0, 191, 255), rect)
    elif weather == "Clouds":
        pygame.draw.circle(surface, (105, 105, 105), rect.center, rect.width // 2)
    elif weather == "Snow":
        pygame.draw.circle(surface, (0, 0, 0), rect.center, rect.width // 2)  
        pygame.draw.circle(surface, (255, 255, 255), rect.center, rect.width // 2 - 2)
    else:
        pygame.draw.circle(surface, (200, 200, 200), rect.center, rect.width // 2)

# 天気によって敵の位置を変更
def setup_enemies_by_weather(weather):
    enemies = []
    float_positions = []
    if weather == "Clear":
        center_x, center_y = WIDTH // 2, 150
        radius = 100
        num_enemies = 12
        for i in range(num_enemies):
            angle = 2 * math.pi * i / num_enemies
            x = int(center_x + radius * math.cos(angle)) - enemy_size // 2
            y = int(center_y + radius * math.sin(angle)) - enemy_size // 2
            enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
            float_positions.append(float(y))
    elif weather == "Clouds":
        points = [(WIDTH // 2, 40), (WIDTH // 2 - 140, 220), (WIDTH // 2 + 140, 220)]
        def interpolate(p1, p2, steps):
            return [(
                int(p1[0] + (p2[0] - p1[0]) * i / steps),
                int(p1[1] + (p2[1] - p1[1]) * i / steps)
            ) for i in range(steps + 1)]
        all_positions = interpolate(points[0], points[1], 5) + interpolate(points[1], points[2], 5)[1:] + interpolate(points[2], points[0], 5)[1:]
        for x, y in all_positions:
            enemies.append(pygame.Rect(x - enemy_size // 2, y - enemy_size // 2, enemy_size, enemy_size))
            float_positions.append(float(y))
    elif weather == "Rain":
        for i in range(10):
            x = 60 + (i % 5) * 70 + (30 if i // 5 % 2 == 1 else 0)
            y = 60 + (i // 5) * 60
            enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
            float_positions.append(float(y))
    elif weather == "Snow":
        center_x, center_y = WIDTH // 2, 140
        offset = 70
        positions = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) <= 2:
                    x = center_x + i * offset
                    y = center_y + j * offset
                    positions.append((x, y))
        for x, y in positions:
            enemies.append(pygame.Rect(x - enemy_size // 2, y - enemy_size // 2, enemy_size, enemy_size))
            float_positions.append(float(y))
    elif weather == "Thunderstorm":
        for i in range(10):
            x = 60 + (i % 5) * 70 + (30 if i // 5 % 2 == 1 else 0)
            y = 60 + (i // 5) * 60
            enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
            float_positions.append(float(y))
    else:
        for col in range(6):
            x = 60 + col * 60
            y = 60
            enemies.append(pygame.Rect(x, y, enemy_size, enemy_size))
            float_positions.append(float(y))
    return enemies, float_positions


# 都市名入力画面 
def input_city_name():
    user_input = ""
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)
    font_small = pygame.font.SysFont("meiryo", 24)
    color = pygame.Color('lightskyblue3')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_input.strip()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        screen.fill((255, 255, 255))
        prompt_text = font_small.render("都市名を入力してください (Enterで決定)", True, (0, 0, 0))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font_small.render(user_input, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()
        clock.tick(30)

def input_weather():
    user_input = ""
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 300, 50)
    font_small = pygame.font.SysFont("meiryo", 24)
    color = pygame.Color('lightskyblue3')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.strip().capitalize() in ["Clear", "Clouds", "Rain", "Snow", "Thunderstorm"]:
                        return user_input.strip().capitalize()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        screen.fill((255, 255, 255))
        prompt_text = font_small.render("天気を入力してください (例: Clear)", True, (0, 0, 0))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font_small.render(user_input, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()
        clock.tick(30)

# 初期化
pygame.init()
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Otenki shooting")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

# 入力と天気取得 
city = input_city_name()
if city.lower() == "test":
    weather = input_weather()
else:
    weather = get_weather(city)

bg_colors = {
    "Clear": (135, 206, 235),
    "Rain": (0, 0, 0),
    "Thunderstorm": (0, 0, 0),
    "Snow": (255, 255, 255),
    "Clouds": (80, 80, 80)
}
bg_color = bg_colors.get(weather, (135, 206, 235))

# ゲーム設定 
player_radius = 20
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5
player_hit_count = 0
last_player_shot_time = 0
player_shot_interval = 200
player_bullets = []
enemy_bullets = []
bullet_speed = 5
enemy_bullet_speed = 3
enemy_fire_delay = 70
enemy_fire_timer = 0
enemy_size = 30
enemy_speed = 0.4
enemies, enemy_float_positions = setup_enemies_by_weather(weather)

running = True
game_over = False
game_clear = False

# メインループ 
while running:
    screen.fill(bg_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_clear:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_radius > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_radius < WIDTH:
            player_x += player_speed
        now = pygame.time.get_ticks()
        if now - last_player_shot_time >= player_shot_interval:
            player_bullets.append(pygame.Rect(player_x - 2, player_y - player_radius, 4, 10))
            last_player_shot_time = now

        for bullet in player_bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                player_bullets.remove(bullet)

        enemy_fire_timer += 1
        if enemy_fire_timer >= enemy_fire_delay and enemies:
            shooter = random.choice(enemies)
            enemy_bullets.append(pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 10))
            enemy_fire_timer = 0

        for bullet in enemy_bullets[:]:
            bullet.y += enemy_bullet_speed
            if bullet.top > HEIGHT:
                enemy_bullets.remove(bullet)
            elif math.hypot(bullet.centerx - player_x, bullet.centery - player_y) < player_radius:
                enemy_bullets.remove(bullet)
                player_hit_count += 1

        for i, enemy in enumerate(enemies):
            enemy_float_positions[i] += enemy_speed
            enemy.y = int(enemy_float_positions[i])
            if enemy.bottom >= HEIGHT:
                game_over = True

        for bullet in player_bullets[:]:
            for i, enemy in enumerate(enemies[:] ):
                if bullet.colliderect(enemy):
                    player_bullets.remove(bullet)
                    del enemies[i]
                    del enemy_float_positions[i]
                    break

        for i, enemy in enumerate(enemies[:] ):
            dist = math.hypot(enemy.centerx - player_x, enemy.centery - player_y)
            if dist < player_radius + enemy_size // 2:
                player_hit_count += 1
                del enemies[i]
                del enemy_float_positions[i]
                break

        segments = 3 - player_hit_count
        for i in range(segments):
            angle_start = i * 120
            pygame.draw.arc(screen, (255, 0, 0), (player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2), math.radians(angle_start), math.radians(angle_start + 120), player_radius)

        for bullet in player_bullets:
            pygame.draw.circle(screen, (255, 255, 0), bullet.center, 3)
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)
        for enemy in enemies:
            draw_enemy(screen, enemy, weather)

        if player_hit_count >= 3:
            game_over = True
        elif not enemies:
            game_clear = True
    else:
        message = "GAME OVER" if game_over else "GAME CLEAR"
        text = font.render(message, True, (255, 0, 0) if game_over else (0, 200, 0))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
