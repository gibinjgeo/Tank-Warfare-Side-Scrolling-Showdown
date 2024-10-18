# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 20:55:15 2024

@author: Ali
"""
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
