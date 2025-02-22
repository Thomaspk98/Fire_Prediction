import pygame
import sys
import collections
import random

# Constants
GRID_SIZE = 5  
GREEN_THRESHOLD = 80  
GREEN_DOMINANCE_RATIO = 1.2  
GRID_LINE_COLOR = (240, 240, 240, 80)  # Very light gray with slight transparency
FIRE_COLOR = (255, 0, 0, 150)  # Red fire with transparency (alpha 150)
BURNED_COLOR = (0, 0, 0, 180)  # Black with transparency (alpha 180)

# Initialize pygame
pygame.init()

# Load the image
image_path = "upload-image11.jpg"  # Change to your image path
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (image.get_width() // GRID_SIZE * GRID_SIZE, 
                                       image.get_height() // GRID_SIZE * GRID_SIZE))

# Get image dimensions
width, height = image.get_size()
cols, rows = width // GRID_SIZE, height // GRID_SIZE

# Compute the ignition point at the center of the image
IGNITION_POINT = (rows // 2, cols // 2)

# Create the pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fire Spread Simulation")

# Grid initialization (using original image pixels)
grid = [[image.get_at((col * GRID_SIZE, row * GRID_SIZE)) for col in range(cols)] for row in range(rows)]
fire_queue = collections.deque()
visited = set()

# Function to check if a pixel is green
def is_green(pixel):
    r, g, b = pixel[:3]  # Extract RGB values
    
    # Define the detected green range
    MIN_GREEN = (0, 1, 0)
    MAX_GREEN = (150, 150, 150)

   # Define additional conditions to exclude light grey shades
    brightness = (r + g + b) / 3  # Average brightness
    is_greyish = abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20

    
    # Check if the pixel is within the green range
    in_range = all(MIN_GREEN[i] <= pixel[i] <= MAX_GREEN[i] for i in range(3))
    
    return in_range and not is_greyish


# Initialize fire at the ignition point if it's green
if is_green(grid[IGNITION_POINT[0]][IGNITION_POINT[1]]):
    fire_queue.append(IGNITION_POINT)
    visited.add(IGNITION_POINT)
    grid[IGNITION_POINT[0]][IGNITION_POINT[1]] = FIRE_COLOR



import random

# Define wind direction (Change as needed: "N", "S", "E", "W")
WIND_DIRECTION = "E"  # Example: Fire moves stronger downward

# Fire spread pattern (always includes immediate neighbors)
base_spread_pattern = [
    (-1, 0), (1, 0), (0, -1), (0, 1)  # Immediate neighbors
]

# Define wind-based priority movement for the second layer
wind_spread_patterns = {
    "N": [(-1, 0), (-2, 0), (-1, -1), (-1, 1)],  # Stronger upward
    "S": [(1, 0), (2, 0), (1, -1), (1, 1)],  # Stronger downward
    "E": [(0, 1), (0, 2), (-1, 1), (1, 1)],  # Stronger rightward
    "W": [(0, -1), (0, -2), (-1, -1), (1, -1)]  # Stronger leftward
}

# Fire spread function with wind influence
def spread_fire():
    global fire_queue
    next_fire_queue = collections.deque()
    
    while fire_queue:
        row, col = fire_queue.popleft()
        grid[row][col] = BURNED_COLOR  # Mark as burned

        # Get the wind-prioritized spread pattern
        wind_priority_spread = wind_spread_patterns[WIND_DIRECTION]

        # Final spread pattern: Immediate neighbors + wind-prioritized + random outer layer
        spread_directions = (
            base_spread_pattern + 
            wind_priority_spread + 
            random.sample(base_spread_pattern + wind_priority_spread, len(base_spread_pattern) // 2)  # Some randomness
        )

        for dr, dc in spread_directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and is_green(grid[nr][nc]) and (nr, nc) not in visited:
                # Fire has a higher chance to spread in the wind direction
                if random.random() < (0.5 if (dr, dc) in wind_priority_spread else 0.5):  
                    next_fire_queue.append((nr, nc))
                    grid[nr][nc] = FIRE_COLOR  # Mark as burning
                    visited.add((nr, nc))

    fire_queue = next_fire_queue  # Update burning cells





# Create a transparent surface for the grid
grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
grid_surface.set_alpha(50)  # Adjust transparency (lower = more transparent)

# Draw subtle grid lines
for row in range(rows):
    for col in range(cols):
        pygame.draw.rect(grid_surface, GRID_LINE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image, (0, 0))  # Always draw background first
    screen.blit(grid_surface, (0, 0))  # Overlay subtle grid lines

    # Spread fire continuously until all green pixels are burned
    if fire_queue:
        spread_fire()

    fire_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Transparent surface for fire

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == FIRE_COLOR:
                pygame.draw.rect(fire_surface, FIRE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            elif grid[row][col] == BURNED_COLOR:
                pygame.draw.rect(fire_surface, BURNED_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    screen.blit(fire_surface, (0, 0))  # Overlay fire and burned areas
    pygame.display.flip()
    pygame.time.delay(300)

pygame.quit()
sys.exit()