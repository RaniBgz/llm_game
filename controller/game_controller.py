import pygame
from view.main_menu_view import MainMenuView


# Define game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3

class GameController:
    def __init__(self):
        self.state = STATE_MENU
        self.view = MainMenuView()

    def run(self):
        pygame.init()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state == STATE_MENU:
                self.menu_loop()
            elif self.state == STATE_PLAYING:
                self.play_loop()
            elif self.state == STATE_PAUSED:
                self.pause_loop()
            elif self.state == STATE_GAME_OVER:
                self.game_over_loop()

    def menu_loop(self):
        # Code for menu loop goes here
        pass

    def play_loop(self):
        # Code for play loop goes here
        pass

    def pause_loop(self):
        # Code for pause loop goes here
        pass

    def game_over_loop(self):
        # Code for game over loop goes here
        pass

if __name__ == "__main__":
    controller = GameController()
    controller.run()