import pygame
import sys
import collections

# Constants
GRID_SIZE = 10  # Size of each grid cell
GREEN_THRESHOLD = 80  # Lower threshold to increase sensitivity
GREEN_DOMINANCE_RATIO = 1.2  # Green must be at least 1.2x greater than red and blue
GRID_LINE_COLOR = (255, 255, 255)  # White grid lines
FIRE_COLOR = (255, 0, 0)  # Red fire color
BURNED_COLOR = (0, 0, 0)  # Black after burning
BLUE_COLOR = (0, 0, 255)  # Represent non-green pixels
GREEN_COLOR = (0, 255, 0)  # Represent green pixels

# Initialize pygame
pygame.init()

# Load the image
image_path = "upload-image14.jpg"  # Change to your image path
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

# Grid initialization
grid = [[image.get_at((col * GRID_SIZE, row * GRID_SIZE)) for col in range(cols)] for row in range(rows)]
fire_queue = collections.deque()
visited = set()

# Function to check if a pixel is green
def is_green(pixel):
    r, g, b, *_ = pixel  # Unpack RGBA
    
    # Check if the green component is dominant
    green_dominant = g > GREEN_THRESHOLD and g > r * GREEN_DOMINANCE_RATIO and g > b * GREEN_DOMINANCE_RATIO
    
    # Allow detection of various green shades
    green_shade = (g > r) and (g > b) and (r < 150 and b < 150)  # Avoid bright reds and blues
    
    return green_dominant or green_shade

# Function to check if a pixel has enough green neighbors
def has_green_neighbors(row, col):
    """Check if at least 5 out of 8 surrounding pixels are also green."""
    green_count = 0
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols and is_green(grid[nr][nc]):
            green_count += 1
    return green_count >= 5  # At least 5 out of 8 neighbors should be green

# Initialize fire at the ignition point if it's green and has enough green neighbors
if is_green(grid[IGNITION_POINT[0]][IGNITION_POINT[1]]) and has_green_neighbors(*IGNITION_POINT):
    fire_queue.append(IGNITION_POINT)
    visited.add(IGNITION_POINT)
    grid[IGNITION_POINT[0]][IGNITION_POINT[1]] = FIRE_COLOR

# Fire spread function
def spread_fire():
    global fire_queue
    next_fire_queue = collections.deque()
    
    while fire_queue:
        row, col = fire_queue.popleft()
        grid[row][col] = BURNED_COLOR  # Convert burned pixels to black

        # Spread fire in 8 directions (includes diagonals for full coverage)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and is_green(grid[nr][nc]) and has_green_neighbors(nr, nc) and (nr, nc) not in visited:
                next_fire_queue.append((nr, nc))
                grid[nr][nc] = FIRE_COLOR  # Mark as burning
                visited.add((nr, nc))

    fire_queue = next_fire_queue  # Update burning cells

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen

    # Spread fire continuously until all green pixels are burned
    if fire_queue:
        spread_fire()

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == FIRE_COLOR:
                color = FIRE_COLOR  # Fire is visible while spreading
            elif grid[row][col] == BURNED_COLOR:
                color = BURNED_COLOR
            elif is_green(grid[row][col]) and has_green_neighbors(row, col):
                color = GREEN_COLOR  # Still green but not burning yet
            else:
                color = BLUE_COLOR  # Non-green pixels as blue

            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    pygame.display.flip()
    pygame.time.delay(150)  # Faster fire spread for better visibility

pygame.quit()
sys.exit()
