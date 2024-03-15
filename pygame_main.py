import pygame
import sys
from model.character import Character
from model.item import Item
from model.object import Object

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def initialize_screen():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    return screen


def main():
    screen = initialize_screen()
    # Set up the game title
    title_font = pygame.font.SysFont("Arial", 50)
    title_text = title_font.render("My Game", True, RED)
    title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))

    # Set up the play button
    play_font = pygame.font.SysFont("Arial", 30)
    play_text = play_font.render("Play", True, RED)
    play_rect = play_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    # Set up the quit button
    quit_font = pygame.font.SysFont("Arial", 30)
    quit_text = quit_font.render("Quit", True, RED)
    quit_rect = quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check if the play or quit button was clicked
        if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            # Clear the display
            screen.fill(WHITE)
            pygame.display.flip()
        elif quit_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            # Exit the game
            pygame.quit()
            sys.exit()

        # Draw everything
        screen.fill(WHITE)
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        # Update the display
        pygame.display.flip()



if __name__ == "__main__":
    main()
