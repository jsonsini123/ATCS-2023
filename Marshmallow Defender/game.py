import pygame
import sys

class SimpleGame:
    WIDTH, HEIGHT = 600, 400
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((SimpleGame.WIDTH, SimpleGame.HEIGHT))
        pygame.display.set_caption("Simple Pygame Game with Classes")
        self.clock = pygame.time.Clock()

        # Create player instance
        self.player = Player()

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update
            self.all_sprites.update()

            # Draw
            self.screen.fill(SimpleGame.BLACK)
            self.all_sprites.draw(self.screen)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(SimpleGame.FPS)

        # Quit the game
        pygame.quit()
        sys.exit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(SimpleGame.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, SimpleGame.HEIGHT // 2 - 25)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SimpleGame.HEIGHT:
            self.rect.y += self.speed
# My Code
class Pedestrian(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface(600, _) #use random int)
        self.image.fill(SimpleGame.White) #make image of pedestrian
        self.speed = 5 #change to make pedestrians faster

    def update(self):
        self.rect.x -= self.speed

    # add status when you reach player game ends

class Marshmallow(pygame.sprite.Sprite):
    def __init__(self, x):
        self.image = pygame.Surface(50, x)
        #add image in
        self.speed = 20
    def update(self):
        self.rect.x += self.speed

    #add status when you reach the border or hit pedestrian delete sprite

if __name__ == "__main__":
    game = SimpleGame()
    game.run()
