import pygame
import numpy as np
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

# Constants
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 5
FIRE_SPREAD_PROB = 0.2
WIND_DIRECTIONS = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
WIND_DIRECTION = 'E'
WIND_STRENGTH = 0.6

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fire Spread Simulation")
font = pygame.font.Font(None, 36)

def upload_image():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    root.destroy()
    
    if file_path:
        try:
            img = pygame.image.load(file_path)
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    return None

def draw_button(screen, msg):
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    
    pygame.draw.rect(screen, (0, 128, 0), (button_x, button_y, button_width, button_height))
    text = font.render(msg, True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
    screen.blit(text, text_rect)
    
    return pygame.Rect(button_x, button_y, button_width, button_height)

# Initial upload screen
image = None
uploaded = False
button_rect = None

while not uploaded:
    screen.fill((255, 255, 255))
    button_rect = draw_button(screen, "Upload Image")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                image = upload_image()
                if image:
                    screen.fill((255, 255, 255))
                    text = font.render("Image uploaded successfully!", True, (0, 128, 0))
                    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    uploaded = True
    
    pygame.display.flip()

# Fire simulation initialization
grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE
fire_grid = np.zeros((grid_height, grid_width), dtype=int)

def spread_fire(grid):
    new_grid = grid.copy()
    dx, dy = WIND_DIRECTIONS[WIND_DIRECTION]
    
    for y in range(1, grid.shape[0] - 1):
        for x in range(1, grid.shape[1] - 1):
            if grid[y, x] == 1:
                new_grid[y, x] = 2
                
                for sy in [-1, 0, 1]:
                    for sx in [-1, 0, 1]:
                        if (sx, sy) != (0, 0) and grid[y + sy, x + sx] == 0:
                            prob = FIRE_SPREAD_PROB
                            if (sx, sy) == (dx, dy):
                                prob += WIND_STRENGTH
                            if random.random() < prob:
                                new_grid[y + sy, x + sx] = 1
    return new_grid

def draw_fire(screen, grid, image):
    fire_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 1:
                fire_overlay.fill((255, 0, 0, 150), rect=(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[y, x] == 2:
                fire_overlay.fill((0, 0, 0, 200), rect=(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    screen.blit(image, (0, 0))  
    screen.blit(fire_overlay, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // GRID_SIZE
        grid_y = mouse_y // GRID_SIZE
        
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                new_x = grid_x + dx
                new_y = grid_y + dy
                if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
                    fire_grid[new_y, new_x] = 1

    fire_grid = spread_fire(fire_grid)
    draw_fire(screen, fire_grid, image)
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()