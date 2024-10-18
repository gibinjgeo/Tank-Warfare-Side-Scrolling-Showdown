class Player(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()
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