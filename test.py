import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero Adventure")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 128, 0)

# Fonts for text
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 48)

# Game variables
score = 0
lives = 3
player_health = 100

# Function to get the player's name
def get_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(WHITE)
        input_text = input_font.render(f"Enter your name: {name}", True, BLACK)
        screen.blit(input_text, (WIDTH // 2 - input_text.get_width() // 2, HEIGHT // 2 - input_text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15:
                    name += event.unicode

    return name

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:  # Fire arrow with spacebar
            self.shoot()

    def shoot(self):
        arrow = FireArrow(self.rect.centerx, self.rect.top)
        all_sprites.add(arrow)
        fire_arrows.add(arrow)

# Fire Arrow class
class FireArrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30), pygame.SRCALPHA)  # Transparent background
        pygame.draw.polygon(self.image, ORANGE, [(5, 0), (0, 20), (10, 20)])  # Arrowhead
        pygame.draw.rect(self.image, YELLOW, (3, 20, 4, 10))  # Arrow shaft
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Function to draw the health bar
def draw_health_bar(health):
    bar_width = 200
    bar_height = 20
    fill_width = (health / 100) * bar_width

    pygame.draw.rect(screen, BLACK, (10, 50, bar_width, bar_height))
    pygame.draw.rect(screen, DARK_GREEN, (10, 50, fill_width, bar_height))

    health_text = font.render(f"{health}%", True, WHITE)
    screen.blit(health_text, (bar_width // 2 - health_text.get_width() // 2 + 10, 50))

# Game setup
player_name = get_player_name()
player = Player()
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
fire_arrows = pygame.sprite.Group()

for _ in range(5):
    enemy = Enemy(speed=random.randint(3, 5))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(keys)
    fire_arrows.update()
    enemies.update()

    # Fire Arrow-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, fire_arrows, True, True)
    for hit in hits:
        score += 10
        new_enemy = Enemy(speed=random.randint(3, 5))
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    if pygame.sprite.spritecollideany(player, enemies):
        player_health -= 10
        if player_health <= 0:
            lives -= 1
            player_health = 100
            if lives == 0:
                print(f"Game Over, {player_name}! Your final score is: {score}")
                running = False

    screen.fill(WHITE)
    all_sprites.draw(screen)

    status_text = font.render(f"{player_name} | Score: {score} | Lives: {lives}", True, BLACK)
    screen.blit(status_text, (10, 10))

    draw_health_bar(player_health)
    pygame.display.flip()

pygame.quit()