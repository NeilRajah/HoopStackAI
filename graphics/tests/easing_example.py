import pygame
from math import sin, pi

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 800
screen_height = 600

# Create the main screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption of the window
pygame.display.set_caption("My Game")

# Define the dimensions of each frame of animation
frame_width = 64
frame_height = 64

# Define the current frame of the animation
current_frame = 0

# Define the animation delay
animation_delay = 10

# Define the initial position of the sprite
start_x = 100
start_y = 100

# Define the final position of the sprite
end_x = 500
end_y = 400

# Define the duration of the animation in frames
animation_duration = 60

# Define an easing function
def ease_in_out_quad(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t + b
    t -= 1
    return -c / 2 * (t * (t - 2) - 1) + b

# The main loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Calculate the position of the sprite based on the current frame of the animation
    if current_frame <= animation_duration:
        x = ease_in_out_quad(current_frame, start_x, end_x - start_x, animation_duration)
        y = ease_in_out_quad(current_frame, start_y, end_y - start_y, animation_duration)
    else:
        x = end_x
        y = end_y

    # Calculate the position of the current frame in the sprite sheet
    frame_x = 0
    frame_y = 0

    # Define a Rect object for the current frame
    frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)

    # Draw the current frame onto the screen
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255, 0, 0), frame_rect.move(x, y))

    # Update the current frame of the animation
    current_frame += 1

    # Update the screen
    pygame.display.update()

    # Delay the animation
    pygame.time.delay(animation_delay)
