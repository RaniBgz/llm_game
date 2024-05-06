import pygame
from view import view_constants as view_cst
from view.ui.button import Button

class SettingsView:
    def __init__(self, screen):
        self.screen = screen
        self.width = view_cst.WIDTH
        self.height = view_cst.HEIGHT
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.font = pygame.font.SysFont("Arial", 28)
        # Title
        self.title_text = self.font.render("Settings", True, view_cst.TEXT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH // 2, view_cst.HEIGHT // 4))
        # Back button
        self.back_button_text = self.font.render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))
        self.default_button_image = pygame.image.load(view_cst.STONE_BUTTON).convert_alpha()
        self.default_pressed_button_image = pygame.image.load(view_cst.STONE_BUTTON_PRESSED).convert_alpha()

        self.text_offset = 4
        self.button_width = 240
        self.button_height = 80
        self.create_reset_items_button()
        self.create_respawn_mobs_button()
        self.create_reset_quests_button()

    def create_respawn_mobs_button(self):
        if getattr(self, 'respawn_mobs_button', None):
            self.render_respawn_mobs_button()
        else:
            self.respawn_mobs_button = Button(self.default_button_image, self.font, self.button_width, self.button_height, self.text_offset,
                                        (self.width // 2 - self.button_width/2, self.height // 3),
                                        "Respawn Mobs", self.rect.topleft, pressed_image=self.default_pressed_button_image)
            self.render_respawn_mobs_button()
        pass

    def create_reset_quests_button(self):
        if getattr(self, 'reset_quests_button', None):
            self.render_reset_quests_button()
        else:
            self.reset_quests_button = Button(self.default_button_image, self.font, self.button_width, self.button_height, self.text_offset,
                                              (self.width // 2 - self.button_width / 2, self.height // 3 + 100),
                                              "Reset Quests", self.rect.topleft,
                                              pressed_image=self.default_pressed_button_image)
            self.render_reset_quests_button()
        pass

    def create_reset_items_button(self):
        if getattr(self, 'reset_items_button', None):
            self.render_reset_items_button()
        else:
            self.reset_items_button = Button(self.default_button_image, self.font, self.button_width, self.button_height,self.text_offset,
                                              (self.width // 2 - self.button_width / 2, self.height // 3 + 200),
                                              "Reset Items", self.rect.topleft,
                                              pressed_image=self.default_pressed_button_image)
            self.render_reset_items_button()
        pass


    def render_respawn_mobs_button(self):
        self.respawn_mobs_button.draw(self.surface)

    def render_reset_quests_button(self):
        self.reset_quests_button.draw(self.surface)

    def render_reset_items_button(self):
        self.reset_items_button.draw(self.surface)

    def render(self):
        self.surface.fill(view_cst.BLUE_GRAY)
        # Render title
        self.surface.blit(self.title_text, self.title_rect)
        # Render back button
        self.surface.blit(self.back_button_text, self.back_button_rect)
        self.render_respawn_mobs_button()
        self.render_reset_quests_button()
        self.render_reset_items_button()
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
