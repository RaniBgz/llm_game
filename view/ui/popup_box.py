import pygame
from view import view_constants as view_cst

class PopupBox:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.create_close_button(pygame.font.SysFont("Arial", 16), view_cst.TEXT_COLOR)
        self.show = False

    def create_close_button(self, font, color):
        close_button_text = font.render("X", True, color)
        close_button_rect = close_button_text.get_rect(topright=(self.width - 10, 10))

        print("In create close button, close_button_rect is:", close_button_rect)
        print(f"width is {self.width}, height is {self.height}")
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, close_button_rect, 1)
        self.surface.blit(close_button_text, close_button_rect)
        return close_button_rect

    # def handle_events(self, event):
    #     print("inner handle event")
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if self.rect.collidepoint(event.pos):
    #             close_button_rect = self.create_close_button(pygame.font.SysFont("Arial", 16), view_cst.TEXT_COLOR)
    #             if close_button_rect.collidepoint(event.pos):
    #                 print("clicked close button")
    #                 self.show = False
    #                 return "close"

    def handle_events(self, event):
        print(f"Handling events for {self.__class__.__name__}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print(f"Popup box clicked at {event.pos}")
                close_button_rect = pygame.Rect(self.rect.topright[0] - 20, self.rect.topright[1], 20, 20)
                # close_button_rect = self.create_close_button(pygame.font.SysFont("Arial", 16), view_cst.TEXT_COLOR)
                if close_button_rect.collidepoint(event.pos):
                    self.show = False
                    return True
        return False


    def display(self):
        if self.show:
            self.screen.blit(self.surface, self.rect)

    def set_position(self, position):
        self.rect.topleft = position