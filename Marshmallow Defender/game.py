import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
player_speed = 5

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marshmallow Defender")
clock = pygame.time.Clock()

# Load player image
player_image = pygame.Surface((50, 50))
player_image.fill(WHITE)
player_rect = player_image.get_rect()
player_rect.topleft = (50, HEIGHT // 2 - 25)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # Draw background and player
    screen.fill(BLACK)
    screen.blit(player_image, player_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()