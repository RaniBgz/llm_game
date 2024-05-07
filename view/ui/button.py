import pygame
from view import view_constants as view_cst

class Button(pygame.sprite.Sprite):
    def __init__(self, image, font, width, height, text_offset, relative_position, text, parent_offset=(0, 0), pressed_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.parent_offset = parent_offset
        self.relative_position = relative_position
        self.original_image = image
        self.image = pygame.transform.scale(image, (width, height))
        self.pressed_image = pressed_image
        self.rect = self.image.get_rect()
        self.text = text
        self.font = font
        self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
        self.text_rect = self.text_render.get_rect()

        self.rect.topleft = (relative_position[0], relative_position[1])

        self.text_rect.center = self.rect.center
        self.text_rect.y -= text_offset

    def draw(self, surface):
        self.true_rect = pygame.Rect(self.rect.topleft[0] + self.parent_offset[0],
                                     self.rect.topleft[1] + self.parent_offset[1], self.rect.width, self.rect.height)
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)

    def is_clicked(self, event):
        return self.true_rect.collidepoint(event.pos)

    def handle_mouse_down(self):
        self.image = pygame.transform.scale(self.pressed_image, (self.rect.width, self.rect.height))
        # if self.is_clicked(event):


    def handle_mouse_up(self):
        self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))
        # if self.is_clicked(event):
        #     print(f"Button {self.text} clicked")

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_up(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_down(event)