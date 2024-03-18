import pygame

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class MainMenuView:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Arial", 50)
        self.title_text = self.title_font.render("My Game", True, RED)
        self.title_rect = self.title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))

        self.play_font = pygame.font.SysFont("Arial", 30)
        self.play_text = self.play_font.render("Play", True, RED)
        self.play_rect = self.play_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        self.quit_font = pygame.font.SysFont("Arial", 30)
        self.quit_text = self.quit_font.render("Quit", True, RED)
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

    def display_menu(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.play_text, self.play_rect)
        self.screen.blit(self.quit_text, self.quit_rect)
        pygame.display.flip()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_rect.collidepoint(event.pos):
                pass
                # TODO: Here, the scene should exit with the information of the next scene to call, and the game controller should handle the scene change
                # Call the game_menu function
                # game_menu()

    def update(self, state):
        pass
        # update menu display elements based on state

    def render(self):
        pass
        # render menu display elements on screen