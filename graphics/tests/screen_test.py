import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 800
screen_height = 600

# Create the main screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption of the window
pygame.display.set_caption("My Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the font
font = pygame.font.Font(None, 30)

# Define the top screen
top_screen_width = 800
top_screen_height = 300
top_screen = pygame.Surface((top_screen_width, top_screen_height))
top_screen.fill(GRAY)
top_text = font.render("Top Screen", True, WHITE)
top_text_rect = top_text.get_rect()
top_text_rect.center = (top_screen_width / 2, top_screen_height / 2)
top_screen.blit(top_text, top_text_rect)

# Define the bottom screen
bottom_screen_width = 800
bottom_screen_height = 300
bottom_screen = pygame.Surface((bottom_screen_width, bottom_screen_height))
bottom_screen.fill(BLACK)
bottom_text = font.render("Bottom Screen", True, WHITE)
bottom_text_rect = bottom_text.get_rect()
bottom_text_rect.center = (bottom_screen_width / 2, bottom_screen_height / 2)
bottom_screen.blit(bottom_text, bottom_text_rect)

# The main loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Clear the screen
    screen.fill(BLACK)

    # Blit the top screen onto the main screen
    screen.blit(top_screen, (0, 0))

    # Blit the bottom screen onto the main screen
    screen.blit(bottom_screen, (0, top_screen_height))

    # Update the screen
    pygame.display.update()
