import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui.utils import wrap_text

class DialogueBox(PopupBox):
    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 4
        super().__init__(screen, width, height)

        #TODO: may be a better way to handle fonts
        self.name_font = pygame.font.SysFont("Arial", 24)
        self.font = pygame.font.SysFont("Arial", 16)
        self.exit_font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 20)
        self.accept_deny_font = pygame.font.SysFont("Arial", 24)
        # self.background_color = view_cst.LIGHT_GRAY
        self.background_color = view_cst.PARCHMENT_COLOR
        self.name_color = view_cst.COFFEE_BROWN_3

    def set_background_color(self, color):
        self.background_color = color

    def set_name_color(self, color):
        self.name_color = color

    def create_dialogue(self, npc_name, dialogue_text):
        self.rect.topleft = (10, 2 * view_cst.HEIGHT // 3 - 10)
        self.surface.fill(self.background_color)

        name_rendered = self.name_font.render(npc_name, True, self.name_color)
        name_pos = (10 + self.width // 2 - name_rendered.get_width() // 2, 10)
        self.surface.blit(name_rendered, name_pos)

        # Use the wrap_text function to get the lines of dialogue
        lines = wrap_text(dialogue_text, self.width - 20, self.font, view_cst.TEXT_COLOR)
        y_offset = 60
        for line_surface in lines:
            # Calculate the x position to center the line
            line_width = line_surface.get_width()
            x_offset = 20 + (self.width - 20 - line_width) // 2  # Adjust to center the line

            # Blit each line of text, incrementing the y_offset for each line
            self.surface.blit(line_surface, (x_offset, y_offset))
            y_offset += line_surface.get_height() + 5  # Adjust spacing between lines

        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        # self.create_prev_button()
        # self.create_next_button()

        self.show = True

    def create_prev_button(self):
        prev_button_text = self.button_font.render("Prev", True, view_cst.DARK_GRAY_2)
        prev_button_rect = prev_button_text.get_rect(bottomleft=(10, self.height - 10))
        pygame.draw.rect(self.surface, self.background_color, prev_button_rect)
        self.prev_button_rect = pygame.Rect(10+10, self.rect.topleft[1] + self.height - 50, 60, 40)
        print(f"Prev button rect: {self.prev_button_rect}")
        # self.prev_button_rect = self.surface.get_rect(bottomleft=(10, self.rect.topleft[1] + self.height - 10))
        self.surface.blit(prev_button_text, prev_button_rect)

    def create_next_button(self):
        next_button_text = self.button_font.render("Next", True, view_cst.DARK_GRAY_2)
        next_button_rect = next_button_text.get_rect(bottomright=(self.width - 10, self.height - 10))
        pygame.draw.rect(self.surface, self.background_color, next_button_rect)
        self.next_button_rect = pygame.Rect(self.width - 60, self.rect.topleft[1] + self.height - 50, 60, 40)
        print(f"Next button rect: {self.next_button_rect}")
        # self.next_button_rect = self.surface.get_rect(bottomright=(self.width - 10, self.rect.topleft[1] + self.height - 10))
        self.surface.blit(next_button_text, next_button_rect)

    def create_close_button(self, font, color):
        close_button_text = font.render("X", True, color)
        close_button_rect = close_button_text.get_rect(topright=(self.width - 10, 10))
        pygame.draw.rect(self.surface, self.background_color, close_button_rect)
        self.surface.blit(close_button_text, close_button_rect)
        self.close_button_rect = pygame.Rect(self.rect.topright[0] - 40, self.rect.topright[1], 40, 40)

    def create_accept_decline_buttons(self):
        accept_button_text = self.accept_deny_font.render("Accept", True, view_cst.DARK_GRAY_2)
        accept_button_rect = accept_button_text.get_rect(bottomleft=(self.width // 3, self.height - 20))
        pygame.draw.rect(self.surface, self.background_color, accept_button_rect)
        self.accept_button_rect = pygame.Rect(self.width // 3, self.rect.topleft[1] + self.height - 50, 100, 40)
        self.surface.blit(accept_button_text, accept_button_rect)

        decline_button_text = self.accept_deny_font.render("Decline", True, view_cst.DARK_GRAY_2)
        decline_button_rect = decline_button_text.get_rect(bottomright=(2 * self.width // 3, self.height - 20))
        pygame.draw.rect(self.surface,self.background_color, decline_button_rect)
        self.decline_button_rect = pygame.Rect(2 * self.width // 3 - 100, self.rect.topleft[1] + self.height - 50, 100,
                                               40)
        self.surface.blit(decline_button_text, decline_button_rect)

    def create_end_quest_button(self):
        end_quest_button_text = self.accept_deny_font.render("End quest", True, view_cst.DARK_GRAY_2)
        end_quest_button_rect = end_quest_button_text.get_rect(bottomleft=(self.width // 2 -end_quest_button_text.get_width()//2, self.height - 20))
        pygame.draw.rect(self.surface, self.background_color, end_quest_button_rect)
        self.end_quest_button_rect = pygame.Rect(self.width // 2-end_quest_button_text.get_width()//2, self.rect.topleft[1] + self.height - 50, 100, 40)
        self.surface.blit(end_quest_button_text, end_quest_button_rect)

    def handle_events(self, event):
        pass