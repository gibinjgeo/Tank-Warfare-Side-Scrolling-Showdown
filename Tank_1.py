import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Side Scrolling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 70)
        self.speed_x = 5
        self.jump_speed = 15
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x

        # Handle jumping
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.vel_y = -self.jump_speed

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Keep the player on the screen
        if self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20

    def shoot(self):
        # Shooting method
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def update(self):
        # Move the projectile
        self.rect.x += self.speed_x
        # Remove projectile if off-screen
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        self.rect.y = SCREEN_HEIGHT - 60
        self.speed_x = random.randint(3, 6)
        self.health = 50

    def update(self):
        # Move enemy
        self.rect.x -= self.speed_x
        # Remove enemy if off-screen
        if self.rect.right < 0:
            self.kill()

# Health bar
def draw_health_bar(player):
    pygame.draw.rect(screen, RED, (player.rect.x, player.rect.y - 20, 100, 10))
    pygame.draw.rect(screen, GREEN, (player.rect.x, player.rect.y - 20, player.health, 10))

# Score and health display
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Game loop
running = True
score = 0
font = pygame.font.Font(None, 36)

while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Spawn enemies
    if random.random() < 0.02:  # Randomly spawn enemies
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check collisions
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    if hits:
        score += 1

    # Check if player collides with enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
        if player.lives <= 0:
            running = False  # Game over

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_health_bar(player)
    draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)
    draw_text(f"Lives: {player.lives}", font, BLACK, screen, 10, 40)

    # Flip the display
    pygame.display.flip()

pygame.quit()
