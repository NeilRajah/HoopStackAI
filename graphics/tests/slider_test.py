import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption of the window
pygame.display.set_caption("Slider Demo")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the position and size of the slider
slider_x = 200
slider_y = 300
slider_width = 400
slider_height = 10

# Define the position and size of the slider button
button_width = 20
button_height = 20
button_x = slider_x
button_y = slider_y - button_height / 2

# Define the minimum and maximum values for the slider
min_value = 0
max_value = 100

# Define the current value of the slider
current_value = min_value
dragging = False

# The main loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                button_x = event.pos[0] - button_width / 2
                if button_x < slider_x:
                    button_x = slider_x
                elif button_x > slider_x + slider_width - button_width:
                    button_x = slider_x + slider_width - button_width
                current_value = round(((button_x - slider_x) / (slider_width - button_width)) * (max_value - min_value) + min_value)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the slider
    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
    pygame.draw.rect(screen, GRAY, slider_rect)

    # Draw the slider button
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, WHITE, button_rect)

    # Draw the current value of the slider
    font = pygame.font.Font(None, 30)
    text = font.render(str(current_value), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (slider_x + slider_width / 2, slider_y - 30)
    screen.blit(text, text_rect)

    # Update the screen
    pygame.display.update()