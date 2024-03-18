import pygame
import sys
from model.character import Character
from model.item import Item
from model.object import Object
# from view.main_menu import MainMenu

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



    # Set up the buttons for the new screen
    button_font = pygame.font.SysFont("Arial", 25)
    quests_text = button_font.render("Quests", True, RED)
    quests_rect = quests_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
    inventory_text = button_font.render("Inventory", True, RED)
    inventory_rect = inventory_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 150))
    map_text = button_font.render("Map", True, RED)
    map_rect = map_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
    world_text = button_font.render("World", True, RED)
    world_rect = world_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 250))

    # Game loop
    def main_menu():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if the play button was clicked
            if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_menu()

            # Draw everything
            screen.fill(WHITE)
            screen.blit(title_text, title_rect)
            screen.blit(play_text, play_rect)
            screen.blit(quit_text, quit_rect)

            # Update the display
            pygame.display.flip()

    def game_menu():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if the play button was clicked
            if quests_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                # Handle quests
                pass
            elif inventory_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                # Handle inventory
                pass
            elif map_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                # Handle map
                pass
            elif world_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                # Handle world
                pass

            # Draw everything
            screen.fill(WHITE)
            screen.blit(quests_text, quests_rect)
            screen.blit(inventory_text, inventory_rect)
            screen.blit(map_text, map_rect)
            screen.blit(world_text, world_rect)

            # Update the display
            pygame.display.flip()

    # Start the main menu
    main_menu()


    # # Set up the menu buttons
    # menu_font = pygame.font.SysFont("Arial", 30)
    # menu_buttons = ["Quests", "Inventory", "Map", "World"]
    # menu_rects = []
    # for i, button in enumerate(menu_buttons):
    #     menu_text = menu_font.render(button, True, RED)
    #     menu_rect = menu_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + (i + 1) * 50))
    #     menu_rects.append(menu_rect)

    # # Game loop
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #
    #     # Check if the play or quit button was clicked
    #     if play_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
    #         # Display the menu buttons
    #         screen.fill(WHITE)
    #         for button, rect in zip(menu_buttons, menu_rects):
    #             menu_text = menu_font.render(button, True, RED)
    #             screen.blit(menu_text, rect)
    #     elif quit_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
    #         # Exit the game
    #         pygame.quit()
    #         sys.exit()
    #     else:
    #         # Draw the main menu
    #         screen.fill(WHITE)
    #         screen.blit(title_text, title_rect)
    #         screen.blit(play_text, play_rect)
    #         screen.blit(quit_text, quit_rect)
    #
    #     # Update the display
    #     pygame.display.flip()



if __name__ == "__main__":
    main()
