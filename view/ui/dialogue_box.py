import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui.utils import wrap_text

class DialogueBox(PopupBox):
    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 4
        super().__init__(screen, width, height)
        self.name_font = pygame.font.SysFont("Arial", 24)
        self.font = pygame.font.SysFont("Arial", 16)
        self.exit_font = pygame.font.SysFont("Arial", 24)
        self.button_font = pygame.font.SysFont("Arial", 24)

    def create_dialogue(self, npc_name, dialogue_text):
        self.rect.topleft = (10, 2 * view_cst.HEIGHT // 3 - 10)
        self.surface.fill(view_cst.POPUP_BG_COLOR)

        name_rendered = self.name_font.render(npc_name, True, view_cst.COFFEE_BROWN_3)
        name_pos = (10 + self.width // 2 - name_rendered.get_width() // 2, 10)
        self.surface.blit(name_rendered, name_pos)

        # Use the wrap_text function to get the lines of dialogue
        lines = wrap_text(dialogue_text, self.width - 20, view_cst.TEXT_COLOR)
        y_offset = 60
        for line_surface in lines:
            # Calculate the x position to center the line
            line_width = line_surface.get_width()
            x_offset = 20 + (self.width - 20 - line_width) // 2  # Adjust to center the line

            # Blit each line of text, incrementing the y_offset for each line
            self.surface.blit(line_surface, (x_offset, y_offset))
            y_offset += line_surface.get_height() + 5  # Adjust spacing between lines

        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        self.create_prev_button()
        self.create_next_button()
        self.show = True

    def create_prev_button(self):
        prev_button_text = self.button_font.render("Prev", True, view_cst.DARK_GRAY_2)
        prev_button_rect = prev_button_text.get_rect(bottomleft=(10, self.height - 10))
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, prev_button_rect)
        self.prev_button_rect = pygame.Rect(10+10, self.rect.topleft[1] + self.height - 50, 60, 40)
        print(f"Prev button rect: {self.prev_button_rect}")
        # self.prev_button_rect = self.surface.get_rect(bottomleft=(10, self.rect.topleft[1] + self.height - 10))
        self.surface.blit(prev_button_text, prev_button_rect)

    def create_next_button(self):
        next_button_text = self.button_font.render("Next", True, view_cst.DARK_GRAY_2)
        next_button_rect = next_button_text.get_rect(bottomright=(self.width - 10, self.height - 10))
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, next_button_rect)
        self.next_button_rect = pygame.Rect(self.width - 60, self.rect.topleft[1] + self.height - 50, 60, 40)
        print(f"Next button rect: {self.next_button_rect}")
        # self.next_button_rect = self.surface.get_rect(bottomright=(self.width - 10, self.rect.topleft[1] + self.height - 10))
        self.surface.blit(next_button_text, next_button_rect)

    def create_close_button(self, font, color):
        close_button_text = font.render("X", True, color)
        close_button_rect = close_button_text.get_rect(topright=(self.width - 10, 10))
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, close_button_rect)
        self.surface.blit(close_button_text, close_button_rect)
        self.close_button_rect = pygame.Rect(self.rect.topright[0] - 40, self.rect.topright[1], 40, 40)


    def handle_events(self, event):
        print(f"Handling events for {self.__class__.__name__}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Popup box clicked at {event.pos}")
            if self.close_button_rect and self.close_button_rect.collidepoint(event.pos):
                print(f"Close button clicked at {event.pos}")
                self.show = False
