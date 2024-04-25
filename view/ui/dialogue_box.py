import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui.utils import wrap_text
from view.ui.button import Button

class DialogueBox(PopupBox):
    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 4
        super().__init__(screen, width, height)
        self.default_button_image = pygame.image.load("./assets/buttons/wood_button_small.png").convert_alpha()


        self.fonts = {
            "name": pygame.font.SysFont("Arial", 24),
            "text": pygame.font.SysFont("Arial", 16),
            "exit": pygame.font.SysFont("Arial", 24),
            "button": pygame.font.SysFont("Arial", 20),
            "accept_deny": pygame.font.SysFont("Arial", 20)
        }
        self.background_color = view_cst.PARCHMENT_COLOR
        self.name_color = view_cst.COFFEE_BROWN_3

    def set_background_color(self, color):
        self.background_color = color

    def set_name_color(self, color):
        self.name_color = color

    def create_dialogue(self, npc_name, dialogue_text):
        #Width and Height offset compared to the parent surface
        self.width_offset = 10
        self.height_offset = 2*view_cst.HEIGHT // 3-10
        self.rect.topleft = (self.width_offset, self.height_offset)
        self.surface.fill(self.background_color)

        name_rendered = self.fonts["name"].render(npc_name, True, self.name_color)
        name_pos = (10 + self.width // 2 - name_rendered.get_width() // 2, 10)
        self.surface.blit(name_rendered, name_pos)

        # Use the wrap_text function to get the lines of dialogue
        lines = wrap_text(dialogue_text, self.width - 20, self.fonts["text"], view_cst.TEXT_COLOR)
        y_offset = 60
        for line_surface in lines:
            # Calculate the x position to center the line
            line_width = line_surface.get_width()
            x_offset = 20 + (self.width - 20 - line_width) // 2  # Adjust to center the line

            # Blit each line of text, incrementing the y_offset for each line
            self.surface.blit(line_surface, (x_offset, y_offset))
            y_offset += line_surface.get_height() + 5  # Adjust spacing between lines

        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)

        self.show = True

    def create_prev_button(self):
        prev_button_text = self.fonts["button"].render("Prev", True, view_cst.DARK_GRAY_2)
        prev_button_rect = prev_button_text.get_rect(bottomleft=(10, self.height - 10))
        pygame.draw.rect(self.surface, self.background_color, prev_button_rect)
        self.prev_button_rect = pygame.Rect(10+10, self.rect.topleft[1] + self.height - 50, 60, 40)
        print(f"Prev button rect: {self.prev_button_rect}")
        # self.prev_button_rect = self.surface.get_rect(bottomleft=(10, self.rect.topleft[1] + self.height - 10))
        self.surface.blit(prev_button_text, prev_button_rect)

    def create_next_button(self):
        next_button_text = self.fonts["button"].render("Next", True, view_cst.DARK_GRAY_2)
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
        print("self width is: ", self.width)
        print("self height is: ", self.height)
        button_width = 150
        button_height = 50
        self.accept_button = Button(self.default_button_image, button_width, button_height, (self.width // 3 - button_width/2, self.height - button_height - 10), "Accept", self.rect.topleft)
        self.decline_button = Button(self.default_button_image, button_width, button_height, (2*self.width // 3 - button_width/2, self.height - button_height - 10), "Decline", self.rect.topleft)
        self.accept_button.draw(self.surface)
        self.decline_button.draw(self.surface)

    def create_end_quest_button(self):
        end_quest_button_text = self.fonts["accept_deny"].render("End quest", True, view_cst.DARK_GRAY_2)
        end_quest_button_rect = end_quest_button_text.get_rect(bottomleft=(self.width // 2 -end_quest_button_text.get_width()//2, self.height - 20))
        pygame.draw.rect(self.surface, self.background_color, end_quest_button_rect)
        self.end_quest_button_rect = pygame.Rect(self.width // 2-end_quest_button_text.get_width()//2, self.rect.topleft[1] + self.height - 50, 100, 40)
        self.surface.blit(end_quest_button_text, end_quest_button_rect)


    def create_generate_quest_button(self):
        generate_quest_button_text = self.fonts["accept_deny"].render("Generate quest", True, view_cst.DARK_GRAY_2)
        generate_quest_button_rect = generate_quest_button_text.get_rect(bottomleft=((self.width // 2 - generate_quest_button_text.get_width() // 2)+10, self.height - 20))
        pygame.draw.rect(self.surface, self.background_color, generate_quest_button_rect)
        self.generate_quest_button_rect = pygame.Rect(self.width // 2 - generate_quest_button_text.get_width() // 2, self.rect.topleft[1] + self.height - 50, 100, 40)
        self.surface.blit(generate_quest_button_text, generate_quest_button_rect)

    def hide_generate_quest_button(self):
        if hasattr(self, 'generate_quest_button_rect'):
            # Redraw the background over the button area to hide it
            background_rect = pygame.Rect(self.generate_quest_button_rect.left - 10,
                                          self.generate_quest_button_rect.top - 10,
                                          self.generate_quest_button_rect.width + 20,
                                          self.generate_quest_button_rect.height + 20)
            pygame.draw.rect(self.surface, self.background_color, background_rect)
            self.surface.blit(self.surface, background_rect, background_rect)
            # Optional: Redraw part of the border if needed or other interface elements that might be overlapped by the button redraw


    def handle_events(self, event):
        pass