import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst

class NPCInfoBox(PopupBox):
    def __init__(self, screen):
        width, height = 200, 100
        super().__init__(screen, width, height)
        self.npc = None
        self.npc_rect = None
        self.font = pygame.font.SysFont("Arial", 16)
        self.text_font = pygame.font.SysFont("Arial", 12)
        self.exit_font = pygame.font.SysFont("Arial", 24)

    def create_npc_info(self, npc, npc_rect):
        self.npc = npc
        # self.rect.midleft = (npc_rect.midright[0] + 10, npc_rect.midright[1])

        screen_width, screen_height = pygame.display.get_surface().get_size()
        if npc_rect.width + npc_rect[0] + self.width < screen_width:
            print("Enough space to the right")
            self.rect.midleft = (npc_rect.midright[0] + 10, npc_rect.midright[1])
        else:
            print("Not enough space to the right")
            self.rect.midright = (npc_rect.midleft[0] - 10, npc_rect.midleft[1])

        self.surface.fill(view_cst.POPUP_BG_COLOR)

        npc_name = f"Name: {self.npc.name}"
        npc_name_text = self.font.render(npc_name, True, view_cst.TEXT_COLOR)
        self.surface.blit(npc_name_text, (10, 10))

        npc_hp = f"HP: {self.npc.hp}"
        npc_hp_text = self.font.render(npc_hp, True, view_cst.TEXT_COLOR)
        self.surface.blit(npc_hp_text, (10, 30))

        npc_hostile = "Hostile" if self.npc.hostile else "Friendly"
        txt_color = view_cst.RED if self.npc.hostile else view_cst.GREEN
        npc_hostile_text = self.font.render(npc_hostile, True, txt_color)
        self.surface.blit(npc_hostile_text, (10, 50))

        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        self.show = True

    def create_close_button(self, font, color):
        close_button_text = font.render("X", True, color)
        close_button_rect = close_button_text.get_rect(topright=(self.width - 10, 10))
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, close_button_rect)
        self.surface.blit(close_button_text, close_button_rect)
        self.close_button_rect = pygame.Rect(self.rect.topright[0] - 40, self.rect.topright[1], 40, 40)


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect and self.close_button_rect.collidepoint(event.pos):
                self.show = False
