import sys
import pygame

class WorldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.view.character_rect.move_ip(0, self.view.character_image.get_height())
                    elif event.key == pygame.K_UP:
                        self.view.character_rect.move_ip(0, -self.view.character_image.get_height())
                    elif event.key == pygame.K_LEFT:
                        self.view.character_rect.move_ip(-self.view.character_image.get_width(), 0)
                    elif event.key == pygame.K_RIGHT:
                        self.view.character_rect.move_ip(self.view.character_image.get_width(), 0)
                    # Handle left and right keys similarly
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        return

            self.view.display_world()