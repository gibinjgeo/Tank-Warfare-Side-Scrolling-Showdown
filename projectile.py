# Projectile class
class Projectile(pygame.sprite.Sprite):
    def _init_(self, x, y):
        super()._init_()
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

