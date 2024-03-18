import pygame


class GameEngine:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.current_scene = MainMenuScene(screen_width, screen_height)

    def switch_scene(self, scene):
        self.current_scene = scene

    def main_game_loop(self):
        while True:
            self.current_scene.handle_events()
            self.current_scene.update()
            self.current_scene.render(self.screen)
            pygame.display.flip()