# Written by: Jake Sonsini with the Help of AI
## Whenever I put a double hash like this ## code is written by me

import pygame
import sys
import random
from fsm import FSM
import os  # Import the os module to work with file paths

class SimpleGame:
    # Initialize window size
    WIDTH, HEIGHT = 1000, 600
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    score = 0

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode((SimpleGame.WIDTH, SimpleGame.HEIGHT))
        pygame.display.set_caption("Marshmallow Defender")
        self.clock = pygame.time.Clock()

        # Access current directory for image gathering
        current_directory = os.getcwd()

        # Create player instance
        self.player = Player()

        # Create sprite group
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Time tracking for marshmallow spawning
        self.last_marshmallow_spawn_time = pygame.time.get_ticks()
        self.marshmallow_spawn_delay = 160  # 160 milliseconds

        ## Time tracking for pedestrian spawning
        self.last_pedestrian_spawn_time = pygame.time.get_ticks()
        self.pedestrian_spawn_delay = 1800.0  # 1800 milliseconds (1.8 second)

        ## Load background image
        background_path = os.path.join(current_directory, "ATCS-2023", "Marshmallow Defender", "images", "background.png")
        self.background_image = pygame.image.load(background_path).convert()

    def run(self):
        ## Display instructions
        play = False
        while not play:
            # Wait for return key
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    play = True

            ## Display instructions
            self.screen.fill(SimpleGame.BLACK)
            font = pygame.font.Font(None, 20)
            text_surface = font.render("To play this game use arrow keys to move and space bar to fire marshmallows at pedestrians, but be careful they will get angry! Press Enter to start.", True, SimpleGame.WHITE)
            self.screen.blit(text_surface, (50, 180))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(SimpleGame.FPS)

        pygame.time.delay(10)  # Add a slight delay to allow event handling
        # Main game loop
        running = True
        game_over = False
        font = pygame.font.Font(None, 36)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # If sprites are flagged for removal, remove them
            for sprite in self.all_sprites.sprites():
                if hasattr(sprite, 'remove_flag') and sprite.remove_flag:
                    sprite.kill()

            # Check to see if a marshmallow hits a pedestrian
            collisions = pygame.sprite.groupcollide(self.all_sprites, self.all_sprites, False, False)
            for sprite, collided_sprites in collisions.items():
                for collided_sprite in collided_sprites:
                    if isinstance(sprite, Marshmallow) and isinstance(collided_sprite, Pedestrian):
                        ## Marshmallow hit Pedestrian call got_shot()
                        collided_sprite.got_shot()
                        sprite.remove_flag = True
            
            
            ## Fire
            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - self.last_marshmallow_spawn_time > self.marshmallow_spawn_delay:
                self.marshmallow = Marshmallow(self.player.get_y())
                self.all_sprites.add(self.marshmallow)
                self.last_marshmallow_spawn_time = current_time

            ## If delay is up spawn another pedestrian
            if current_time - self.last_pedestrian_spawn_time > self.pedestrian_spawn_delay:
                self.pedestrian = Pedestrian(self)
                self.all_sprites.add(self.pedestrian)
                self.last_pedestrian_spawn_time = current_time

            # Update
            self.all_sprites.update()

            ## Scale the image to the desired size
            self.background = pygame.transform.scale(self.background_image, (SimpleGame.WIDTH, SimpleGame.HEIGHT))

            ## Draw
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)

            ## Draw score on the right side of the screen
            text_surface = font.render(f"Score: {self.score}", True, SimpleGame.WHITE)
            self.screen.blit(text_surface, (880, 10))

            # If a pedestrian survives call game over
            if any(hasattr(sprite, 'rect') and sprite.rect.x <= 5 for sprite in self.all_sprites.sprites()):
                game_over = True
            
            ## Game over call
            if game_over == True:
                ## Quit the game and display scores
                self.screen.fill(SimpleGame.BLACK)
                text_surface = font.render(f"Final Score: {self.score}", True, SimpleGame.WHITE)
                self.screen.blit(text_surface, (820, 10))
                text_surface = font.render(f"GAME OVER", True, SimpleGame.WHITE)
                self.screen.blit(text_surface, (430, 280))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(SimpleGame.FPS)

            ## Increase in difficulty over time
            self.pedestrian_spawn_delay -= 0.1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Initialise speed and image
        self.image = pygame.Surface((50, 50))
        self.image.fill(SimpleGame.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, SimpleGame.HEIGHT // 2 - 25)
        self.speed = 8

    def update(self):
        # Change location based off of input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SimpleGame.HEIGHT:
            self.rect.y += self.speed
    
    # Returns Y value for Marshmallow spawning
    def get_y(self):
        return self.rect.y

## I believe that I have improved my object oriented programming with
## This class and the marshmallow class where I spent most of my time programming
class Pedestrian(pygame.sprite.Sprite):
    # Initialize states
    PASSIVE, MAD, SCARED = 0, 1, 2
    IS_SHOT = "is"

    def __init__(self, game_instance):
        # Create initial Passive state
        self.fsm = FSM(self.PASSIVE)
        super().__init__()
        self.game = game_instance
        # Access current directory then initialize images and scale them
        current_directory = os.getcwd()
        passive_path = os.path.join(current_directory, "ATCS-2023", "Marshmallow Defender", "images", "passive.png")
        angry_path = os.path.join(current_directory, "ATCS-2023", "Marshmallow Defender", "images", "angry.png")
        scared_path = os.path.join(current_directory, "ATCS-2023", "Marshmallow Defender", "images", "scared.png")
        self.images = {
            self.PASSIVE: pygame.transform.scale(pygame.image.load(passive_path).convert(), (70, 120)),
            self.MAD: pygame.transform.scale(pygame.image.load(angry_path).convert(), (70, 120)),
            self.SCARED: pygame.transform.scale(pygame.image.load(scared_path).convert(), (70, 120))
        }
        ## Set initial image and random spawn location
        self.image = self.images[self.PASSIVE]
        self.rect = self.image.get_rect()
        self.rect.topleft = 1000, random.randint(20, 480)

        ## Create passive speed and initialize remove_flag
        self.speed = 3
        self.remove_flag = False

        ## initialize fsm with initial state
        ## I spent a lot of time on the FSM so I was hoping this could improve my content standards because
        ## I beieve my quiz doesn't show what I know
        self.fsm.add_transition(self.IS_SHOT, self.PASSIVE, self.turn_mad, self.MAD)
        self.fsm.add_transition(self.IS_SHOT, self.MAD, self.turn_scared, self.SCARED)
        self.fsm.add_transition(self.IS_SHOT, self.SCARED, None, self.SCARED)

    ## Change image and adjust speed for MAD state
    def turn_mad(self):
        self.image = self.images[self.MAD]
        self.speed = 8

    ## Change image and adjust speed for SCARED state
    def turn_scared(self):
        self.image = self.images[self.SCARED]
        self.speed = -8

    ## If shot run FSM process
    def got_shot(self):
        self.fsm.process(self.IS_SHOT)

    ## Change location and check if out of bounds
    def update(self):
        if self.rect.x > 0:
            if self.rect.x > 1000:
                self.game.score += 1
                self.remove_flag = True
            else:
                self.rect.x -= self.speed
        else:
            self.remove_flag = True

class Marshmallow(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        ## Initialize marshmallow location and image
        self.image = pygame.Surface((5, 5))
        self.image.fill(SimpleGame.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, y + 10)
        self.speed = 20
        self.remove_flag = False

    ## Change location
    def update(self):
        if (self.rect.x + self.speed <= 1000):
            self.rect.x += self.speed
        else:
            self.remove_flag = True

    ## Return Status
    def get_status(self):
        return self.remove_flag

if __name__ == "__main__":
    game = SimpleGame()
    game.run()
