import pygame
import math
import time
import random

# Initialize Pygame
pygame.init()

# Constants
HEIGHT = 800
WIDTH = 1000
BLACK = (0, 0, 0)
IMAGE_SCALE = 4
TOP_MARGIN = 50  # Stop player's upward movement 50 pixels from the top

# Pygame setup
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background image
bg_surf = pygame.image.load('assets/images/backgrounds/clouds2.png').convert()
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
        self.f_mask = pygame.mask.from_surface(self.f_image)

        self.p_image = pygame.image.load("assets/images/player/parachute.png").convert_alpha()
        self.p_image = pygame.transform.scale(self.p_image, (self.p_image.get_width() * IMAGE_SCALE, self.p_image.get_height() * IMAGE_SCALE))
        self.p_mask = pygame.mask.from_surface(self.p_image)

        self.image = self.f_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scroll_speed = 4  # Speed at which the player and background scroll
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

class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/obstacles/plane.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
    
    def update(self):
        # self.rect.centery -= self.speed
        self.rect.centerx -= 2
    
        if self.rect.bottom < 0:
            self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/obstacles/hot_air_balloon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
    
    def update(self):
        self.rect.centery -= self.speed
        # self.rect.centerx -= 2
    
        if self.rect.bottom < 0:
            self.kill()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Wind(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/wind.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
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

plane_group = pygame.sprite.Group()
last_plane_spawn_time = pygame.time.get_ticks()

balloon_group = pygame.sprite.Group()
last_balloon_spawn_time = pygame.time.get_ticks()

wind_group = pygame.sprite.Group()

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

    # Time-based plane spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_plane_spawn_time > 6000:
        plane = Plane(WIDTH, random.randint(50, 600))
        plane_group.add(plane)
        last_plane_spawn_time = current_time  

    # Time-based balloon spawning
    if current_time - last_balloon_spawn_time > 4000:
        balloon = Balloon(random.randint(50, WIDTH-50), HEIGHT+50)
        balloon_group.add(balloon) 
        last_balloon_spawn_time = current_time 

    plane_group.update()
    plane_group.draw(surface)

    balloon_group.update()
    balloon_group.draw(surface)

    if pygame.sprite.spritecollide(player, plane_group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(player, balloon_group, False, pygame.sprite.collide_mask):
        running = False 
    
    # wind_group.draw(surface)
    
    # Adjust scroll speed based on player's state
    if not player.state == Player.DESCENDING and (keys[pygame.K_SPACE] or player.state == Player.TOP):
        scroll -= player.scroll_speed
    else:
        scroll -= player.scroll_speed

    pygame.display.flip()
    clock.tick(160)

pygame.quit()
