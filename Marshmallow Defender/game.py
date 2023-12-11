import pygame
import sys
import random
from fsm import FSM

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

        # Time tracking for marshmallow spawning
        self.last_marshmallow_spawn_time = pygame.time.get_ticks()
        self.marshmallow_spawn_delay = 500  # 1000 milliseconds (1 second)

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fire
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE] and current_time - self.last_marshmallow_spawn_time > self.marshmallow_spawn_delay:
                self.marshmallow = Marshmallow(self.player.get_y())
                self.all_sprites.add(self.marshmallow)
                self.last_marshmallow_spawn_time = current_time
            
            for sprite in self.all_sprites.sprites():
                if hasattr(sprite, 'remove_flag') and sprite.remove_flag:
                    sprite.kill()
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
    def get_y(self):
        return self.rect.y
# My Code
class Pedestrian(pygame.sprite.Sprite):
    PASSIVE, MAD, SCARED = 0, 1, 2
    IS_SHOT = "is"

    def __init__(self):
        self.fsm = FSM(0)
        super().__init__()
        self.image = pygame.Surface((600, random.randint(20, 380))) #use random int)
        self.image.fill(SimpleGame.WHITE) #make image of pedestrian
        self.speed = 5 #change to make pedestrians faster
        self.is_shot = False
        #initialise fsm with initial state
        self.fsm.add_transition(self.IS_SHOT, self.PASSIVE, self.turn_mad, self.MAD)
        self.fsm.add_transition(self.IS_SHOT, self.MAD, self.turn_scared, self.SCARED)

    def turn_mad(self):
        self.speed = 10
        # Change image
        self.is_shot = False

    def turn_scared(self):
        # Change image
        self.speed = -10

    def change_status():
        self.is_shot = True


    def update(self):
        self.rect.x -= self.speed

    # add status when you reach player game ends

class Marshmallow(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(SimpleGame.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, y + 10)
        self.speed = 20
        self.remove_flag = False
    def update(self):
        if (self.rect.x + self.speed <= 600):
            self.rect.x += self.speed
        else:
            self.remove_flag = True
    def get_status(self):
        return self.remove_flag


    #add status when you reach the border or hit pedestrian delete sprite

if __name__ == "__main__":
    game = SimpleGame()
    game.run()
