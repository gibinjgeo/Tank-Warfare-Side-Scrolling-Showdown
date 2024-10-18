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
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Load and scale the background image to fill the screen
background_image = pygame.image.load("bg.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to get the player's name
def get_player_name():
    name = ""
    input_active = True
    font = pygame.font.Font(None, 48)

    # Load and scale the intro image to fill the screen
    intro_image = pygame.image.load("intro_image.png").convert()
    intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while input_active:
        # Draw the intro image as the background
        screen.blit(intro_image, (0, 0))

        # Render the input text
        input_text = font.render(f"Enter your name: {name}", True, BLACK)
        input_rect = input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(input_text, input_rect)

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
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode

    return name

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the tank image
        self.original_image = pygame.image.load("tank.png").convert_alpha()
        # Scale the tank image while maintaining aspect ratio
        self.image = self.scale_image(self.original_image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 70)
        self.speed_x = 5
        self.jump_speed = 20  # Higher jump speed
        self.gravity = 1
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def scale_image(self, image, target_size):
        # Get the original dimensions
        original_rect = image.get_rect()
        width_ratio = target_size[0] / original_rect.width
        height_ratio = target_size[1] / original_rect.height
        min_ratio = min(width_ratio, height_ratio)
        new_size = (int(original_rect.width * min_ratio), int(original_rect.height * min_ratio))
        return pygame.transform.scale(image, new_size)

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x

        # Handle jumping
        if keys[pygame.K_UP] and self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.vel_y = -self.jump_speed

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Keep the player on the ground
        if self.rect.bottom >= SCREEN_HEIGHT - 20:
            self.rect.bottom = SCREEN_HEIGHT - 20
            self.vel_y = 0

    def shoot(self):
        # Shooting method
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the projectile image
        self.original_image = pygame.image.load("projectile.png").convert_alpha()
        # Scale the projectile image while maintaining aspect ratio
        self.image = self.scale_image(self.original_image, (40, 20))  # Adjust size as needed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def scale_image(self, image, target_size):
        # Get the original dimensions
        original_rect = image.get_rect()
        width_ratio = target_size[0] / original_rect.width
        height_ratio = target_size[1] / original_rect.height
        min_ratio = min(width_ratio, height_ratio)
        new_size = (int(original_rect.width * min_ratio), int(original_rect.height * min_ratio))
        return pygame.transform.scale(image, new_size)

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
        # Load the enemy image
        self.original_image = pygame.image.load("enemy.png").convert_alpha()
        # Scale the enemy image while maintaining aspect ratio
        self.image = self.scale_image(self.original_image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100)
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 20
        self.speed_x = random.randint(3, 6)
        self.health = 50

    def scale_image(self, image, target_size):
        # Get the original dimensions
        original_rect = image.get_rect()
        width_ratio = target_size[0] / original_rect.width
        height_ratio = target_size[1] / original_rect.height
        min_ratio = min(width_ratio, height_ratio)
        new_size = (int(original_rect.width * min_ratio), int(original_rect.height * min_ratio))
        return pygame.transform.scale(image, new_size)

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
def draw_text(player_name, score, lives):
    font = pygame.font.Font(None, 36)
    text = f"Player: {player_name} | Score: {score} | Lives: {lives}"
    text_obj = font.render(text, True, BLACK)
    screen.blit(text_obj, (10, 10))

# Game over display
def show_game_over_message():
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("You lost! Try again.", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Wait for 3 seconds

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Get the player's name
player_name = get_player_name()

# Create player
player = Player()
all_sprites.add(player)

# Game loop
running = True
score = 0

while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the game loop
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

    # Check collisions between enemies and projectiles
    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    if hits:
        score += len(hits)

    # Check if player collides with enemies
    enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
    if enemy_hits:
        player.health -= 10 * len(enemy_hits)
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives <= 0:
                show_game_over_message()  # Show game over message
                running = False  # Game over

    # Draw everything
    screen.blit(background_image, (0, 0))  # Draw the background first
    all_sprites.draw(screen)
    draw_health_bar(player)
    draw_text(player_name, score, player.lives)

    # Flip the display
    pygame.display.flip()

pygame.quit()

