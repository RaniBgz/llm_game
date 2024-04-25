import pygame
from view import view_constants as view_cst

class Button(pygame.sprite.Sprite):
    def __init__(self, image, width, height, relative_position, text, parent_offset=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.parent_offset = parent_offset
        self.relative_position = relative_position
        self.original_image = image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        print(f"Rect just after creation from image: {self.rect}")
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
        self.text_rect = self.text_render.get_rect()

        print(f"Text rect just after creation: {self.text_rect}")

        print(f"Parent offset: {parent_offset}")
        self.rect.topleft = (relative_position[0], relative_position[1])
        print(f"Rect after setting position: {self.rect}")

        self.text_rect.center = self.rect.center
        self.text_rect.y -= 5

    def draw(self, surface):
        self.true_rect = pygame.Rect(self.rect.topleft[0] + self.parent_offset[0],
                                     self.rect.topleft[1] + self.parent_offset[1], self.rect.width, self.rect.height)
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)

    def is_clicked(self, mouse_pos):
        print(f"rect position: {self.rect.topleft}")
        print(f"entire rect: {self.rect}")
        return self.true_rect.collidepoint(mouse_pos)
