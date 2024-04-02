import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
class NPCInfoBox(PopupBox):

    def __init__(self, screen):
        width, height = 200, 100
        super().__init__(screen, width, height)
        self.npc = None
        self.npc_rect = None

    def create_npc_info(self, npc, npc_rect):
        self.npc = npc
        self.rect.midleft = (npc_rect.midright[0] + 10, npc_rect.midright[1])
        font = pygame.font.SysFont("Arial", 16)
        self.surface.fill(view_cst.POPUP_BG_COLOR)

        npc_name = f"Name: {self.npc.name}"
        npc_name_text = font.render(npc_name, True, view_cst.TEXT_COLOR)
        self.surface.blit(npc_name_text, (10, 10))

        npc_hp = f"HP: {self.npc.hp}"
        npc_hp_text = font.render(npc_hp, True, view_cst.TEXT_COLOR)
        self.surface.blit(npc_hp_text, (10, 30))

        npc_hostile = "Hostile" if self.npc.hostile else "Friendly"
        txt_color = view_cst.RED if self.npc.hostile else view_cst.GREEN
        npc_hostile_text = font.render(npc_hostile, True, txt_color)
        self.surface.blit(npc_hostile_text, (10, 50))

        self.create_close_button(font, view_cst.TEXT_COLOR)