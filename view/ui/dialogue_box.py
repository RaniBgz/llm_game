import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst


class DialogueBox(PopupBox):

    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 4
        super().__init__(screen, width, height)

    def create_dialogue(self, npc, dialogue_text):
        self.rect.topleft = (10, 3 * view_cst.HEIGHT // 4 - 10)
        font = pygame.font.SysFont("Arial", 16)
        self.surface.fill(view_cst.POPUP_BG_COLOR)

        dialogue_rendered = font.render(dialogue_text, True, view_cst.TEXT_COLOR)
        self.surface.blit(dialogue_rendered, (10, 10))

        self.create_close_button(font, view_cst.TEXT_COLOR)
