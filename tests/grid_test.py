import pygame

# Define the dimensions of the screen
width = 600
height = 600

# Define the number of rows and columns in the grid
n_rows = 10
n_cols = 10

# Define the width and height of each cell in the grid
cell_width = width // n_cols
cell_height = height // n_rows

# Define the colors we'll use
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

# Define the 2D matrix to represent the grid
grid = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
grid[2][3] = 1  # Example cell to set as blue

# Initialize PyGame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((width, height))

# Draw the grid
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Fill the background with white
    screen.fill(white)

    # Draw the grid
    for row in range(n_rows):
        for col in range(n_cols):
            color = blue if grid[row][col] == 1 else white
            rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, black, rect, 1)

    # Update the display
    pygame.display.update()