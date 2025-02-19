import pygame
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 5  # Defines the resolution of the fire simulation
FIRE_SPREAD_PROB = 0.2  # Base probability of fire spreading
WIND_DIRECTIONS = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
WIND_DIRECTION = 'E'  # Default wind direction
WIND_STRENGTH = 0.6  # Increases spread probability in wind direction

# Load and scale the image
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
image = pygame.image.load("upload-image.jpg")
image = pygame.transform.scale(image, (WIDTH, HEIGHT))

grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE
fire_grid = np.zeros((grid_height, grid_width), dtype=int)  # 0: Unburnt, 1: Burning, 2: Burnt

# Ignite fire at a random point
start_x, start_y = grid_width // 2, grid_height // 2
fire_grid[start_y, start_x] = 1

def spread_fire(grid):
    new_grid = grid.copy()
    dx, dy = WIND_DIRECTIONS[WIND_DIRECTION]
    
    for y in range(1, grid.shape[0] - 1):  # Avoid the border
        for x in range(1, grid.shape[1] - 1):  # Avoid the border
            if grid[y, x] == 1:  # Burning pixel
                new_grid[y, x] = 2  # Mark as burnt
                
                # Spread fire
                for sy in [-1, 0, 1]:
                    for sx in [-1, 0, 1]:
                        if (sx, sy) != (0, 0) and grid[y + sy, x + sx] == 0:  # If it's unburned
                            prob = FIRE_SPREAD_PROB
                            if (sx, sy) == (dx, dy):
                                prob += WIND_STRENGTH  # Increase spread chance in wind direction
                            if random.random() < prob:
                                new_grid[y + sy, x + sx] = 1  # Ignite fire in neighboring cell
    # Now handle the edge boundary cells and turn them burnt
    for x in range(grid.shape[1]):
        if grid[0, x] == 1:  # Top row
            new_grid[0, x] = 2
        if grid[grid.shape[0] - 1, x] == 1:  # Bottom row
            new_grid[grid.shape[0] - 1, x] = 2
    for y in range(grid.shape[0]):
        if grid[y, 0] == 1:  # Left column
            new_grid[y, 0] = 2
        if grid[y, grid.shape[1] - 1] == 1:  # Right column
            new_grid[y, grid.shape[1] - 1] = 2
    
    return new_grid

def draw_fire(screen, grid, image):
    # Create a surface to hold the fire overlay (with transparency)
    fire_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 1:  # Burning (Fire)
                fire_overlay.fill((255, 0, 0, 150), rect=(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Red for fire
            elif grid[y, x] == 2:  # Burnt
                fire_overlay.fill((0, 0, 0, 200), rect=(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Black for burnt

    # Draw the original image as background
    screen.blit(image, (0, 0))  
    
    # Draw black border around the screen
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 10)  # 10-pixel black border on all sides
    
    # Overlay the fire effect on top (with transparency)
    screen.blit(fire_overlay, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    fire_grid = spread_fire(fire_grid)  # Update the fire grid
    draw_fire(screen, fire_grid, image)  # Draw fire over the background image with transparency
    pygame.display.flip()  # Update the screen
    pygame.time.delay(100)  # Control simulation speed

pygame.quit()
