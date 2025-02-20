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

# Store original image colors (prevents modification issues)
original_grid = [[image.get_at((col * GRID_SIZE, row * GRID_SIZE)) for col in range(cols)] for row in range(rows)]
grid = [[original_grid[row][col] for col in range(cols)] for row in range(rows)]

# Fire management
fire_queue = collections.deque()
visited = set()
remaining_green = set()  # Track all green pixels

# Function to check if a pixel is green
def is_green(pixel):
    r, g, b, *_ = pixel  # Unpack RGBA
    return g > GREEN_THRESHOLD and g > r * GREEN_DOMINANCE_RATIO and g > b * GREEN_DOMINANCE_RATIO

# Identify all green areas and initialize fire at the ignition point
for row in range(rows):
    for col in range(cols):
        if is_green(original_grid[row][col]):
            remaining_green.add((row, col))

if is_green(original_grid[IGNITION_POINT[0]][IGNITION_POINT[1]]):
    fire_queue.append(IGNITION_POINT)
    visited.add(IGNITION_POINT)
    grid[IGNITION_POINT[0]][IGNITION_POINT[1]] = FIRE_COLOR
    remaining_green.discard(IGNITION_POINT)  # Remove from remaining greens

# Fire spread function
def spread_fire():
    global fire_queue

    next_fire_queue = collections.deque()
    while fire_queue:
        row, col = fire_queue.popleft()
        grid[row][col] = BURNED_COLOR  # Mark as burned

        # Spread fire in 8 directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if (nr, nc) in remaining_green:  # Burn only green areas
                    next_fire_queue.append((nr, nc))
                    grid[nr][nc] = FIRE_COLOR
                    visited.add((nr, nc))
                    remaining_green.discard((nr, nc))  # Remove from remaining green set

    fire_queue = next_fire_queue

    # If no fire remains but green exists, ignite a new isolated green area
    if not fire_queue and remaining_green:
        new_ignition = remaining_green.pop()  # Pick any green pixel
        fire_queue.append(new_ignition)
        visited.add(new_ignition)
        grid[new_ignition[0]][new_ignition[1]] = FIRE_COLOR

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
            elif (row, col) in remaining_green:
                color = GREEN_COLOR  # Still green but not burning yet
            else:
                color = BLUE_COLOR  # Non-green pixels as blue

            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, GRID_LINE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    pygame.display.flip()
    pygame.time.delay(100)  # Control fire speed

pygame.quit()
sys.exit()