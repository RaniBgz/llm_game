# import pygame
# import time
#
# # Initialize Pygame
# pygame.init()
#
# # Set window size
# width = 800
# height = 600
# screen = pygame.display.set_mode((width, height))
#
# # Set window title
# pygame.display.set_caption("Basic Pygame Project")
#
# # Colors
# black = (0, 0, 0)
# white = (255, 255, 255)
#
# # Clock for FPS
# clock = pygame.time.Clock()
# fps = 60
#
# # --- Main game loop ---
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 running = False
#
#     # Update game logic (empty here)
#
#     # Render
#     screen.fill(black)
#
#     # Display FPS
#     font = pygame.font.Font(None, 36)
#     fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, white)
#     screen.blit(fps_text, (10, 10))
#
#     # Update display
#     pygame.display.flip()
#
#     # Limit FPS
#     clock.tick(fps)
#
# # Quit Pygame
# pygame.quit()




import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyGame FPS Counter")

# Colors
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Calculate FPS
    fps = int(clock.get_fps())

    # Clear the screen
    screen.fill(WHITE)

    # Display FPS counter
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()