import pygame
from view.main_menu_view import MainMenuView

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class GameController:
    def __init__(self):
        self.screen = self.initialize_screen()
        self.current_view = MainMenuView(self)

    def initialize_screen(self):
        # Initialize Pygame
        pygame.init()
        # Set up the display
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        return screen

    def run(self):
        while True:
            self.current_view.handle_events()
            self.current_view.update()
            self.current_view.render(self.screen)




    # class GameController:
    #     def __init__(self):
    #         self.model = GameModel()
    #         self.view = MainMenuView()
    #
    #     def run(self):
    #         while True:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     pygame.quit()
    #                     sys.exit()
    #
    #             user_input = get_user_input()
    #             self.model.update(user_input)
    #             self.view.update(self.model.state)
    #             self.view.render()
    #
    #             if self.model.state == 'playing':
    #                 self.view = MainGameView()
    #             elif self.model.state == 'quest':
    #                 self.view = QuestView()