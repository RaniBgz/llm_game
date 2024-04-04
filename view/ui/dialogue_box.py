import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst

class DialogueBox(PopupBox):
    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 4
        super().__init__(screen, width, height)
        self.font = pygame.font.SysFont("Arial", 16)
        self.exit_font = pygame.font.SysFont("Arial", 32)
        self.button_font = pygame.font.SysFont("Arial", 24)

    def create_dialogue(self, npc, dialogue_text, dialogue_index, total_dialogues):
        self.rect.topleft = (10, 3 * view_cst.HEIGHT // 4 - 10)
        self.surface.fill(view_cst.POPUP_BG_COLOR)
        dialogue_rendered = self.font.render(dialogue_text, True, view_cst.TEXT_COLOR)
        self.surface.blit(dialogue_rendered, (10, 10))
        print(f"Blitting dialogue")
        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        self.create_prev_next_buttons(dialogue_index, total_dialogues)
        # self.close_button_rect = self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        self.show = True

    def create_prev_next_buttons(self, dialogue_index, total_dialogues):
        prev_button_text = self.button_font.render("Prev", True, view_cst.TEXT_COLOR)
        next_button_text = self.button_font.render("Next", True, view_cst.TEXT_COLOR)

        prev_button_rect = prev_button_text.get_rect(bottomleft=(10, self.height - 10))
        next_button_rect = next_button_text.get_rect(bottomright=(self.width - 10, self.height - 10))

        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, prev_button_rect)
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, next_button_rect)

        self.surface.blit(prev_button_text, prev_button_rect)
        self.surface.blit(next_button_text, next_button_rect)

        self.prev_button_rect = pygame.Rect(prev_button_rect)
        self.next_button_rect = pygame.Rect(next_button_rect)

        if dialogue_index == 0:
            self.prev_button_rect = None
        if dialogue_index == total_dialogues - 1:
            self.next_button_rect = None

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
