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