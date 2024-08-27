import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Constants
HEIGHT = 800
WIDTH = 500
BLACK = (0, 0, 0)
IMAGE_SCALE = 4
TOP_MARGIN = 50  # Stop player's upward movement 50 pixels from the top

# Pygame setup
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background image
bg_surf = pygame.image.load('assets/images/backgrounds/clouds.png').convert()
bg_height = bg_surf.get_height()
tiles = math.ceil(HEIGHT / bg_height) + 1

class Player(pygame.sprite.Sprite):

    # Player's y axis location on screen
    BOTTOM = 1
    ASCENDING = 2 # Player is moving toward top of screen
    TOP = 3
    DESCENDING = 4 # Player is moving toward bottom of screen

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load and scale images
        self.f_image = pygame.image.load("assets/images/player/freefall.png").convert_alpha()
        self.f_image = pygame.transform.scale(self.f_image, (self.f_image.get_width() * IMAGE_SCALE, self.f_image.get_height() * IMAGE_SCALE))

        self.p_image = pygame.image.load("assets/images/player/parachute.png").convert_alpha()
        self.p_image = pygame.transform.scale(self.p_image, (self.p_image.get_width() * IMAGE_SCALE, self.p_image.get_height() * IMAGE_SCALE))

        self.image = self.f_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scroll_speed = 2  # Speed at which the player and background scroll
        self.original_y = y
        self.state = Player.BOTTOM
        self.stop_time = 0

    def update(self, keys):

        # If player is at screen bottom and space bar is pressed, player moves toward top of screen
        if self.state == Player.BOTTOM:
            self.image = self.f_image
            self.rect = self.image.get_rect(center=self.rect.center)
            if keys[pygame.K_SPACE]:
                self.state = Player.ASCENDING
        
        elif self.state == Player.ASCENDING:
            self.image = self.p_image
            self.rect = self.image.get_rect(center=self.rect.center)
            if self.rect.y > TOP_MARGIN:
                self.rect.y -= self.scroll_speed
            else:
                self.state = Player.TOP
                self.stop_time = time.time()

        elif self.state == Player.TOP:
            self.image = self.p_image
            self.rect = self.image.get_rect(center=self.rect.center)
            if time.time() - self.stop_time > 3:
                self.state = Player.DESCENDING

        # After 3 seconds at top of screen, player moves toward bottom of screen
        elif self.state == Player.DESCENDING:
            self.image = self.f_image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y += self.scroll_speed
            if self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.state = Player.BOTTOM

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def scroll_clouds(surface, scroll, bg_surf, tiles, bg_height):
    for i in range(0, tiles):
        surface.blit(bg_surf, (0, i * bg_height + scroll))
    
    if abs(scroll) > bg_height:
        scroll = 0

    return scroll

# Main game loop
scroll = 0
player = Player(250, 500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surface.fill(BLACK)
    
    # Scroll clouds continuously
    scroll = scroll_clouds(surface, scroll, bg_surf, tiles, bg_height)

    # Update and draw player
    keys = pygame.key.get_pressed()
    player.update(keys)
    player.draw(surface)
    
    # Adjust scroll speed based on player's state
    if not player.state == Player.DESCENDING and (keys[pygame.K_SPACE] or player.state == Player.TOP):
        scroll -= player.scroll_speed
    else:
        scroll -= player.scroll_speed

    pygame.display.flip()
    clock.tick(160)

pygame.quit()
