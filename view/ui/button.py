import pygame
from view import view_constants as view_cst

class Button(pygame.sprite.Sprite):
    def __init__(self, image, width, height, center_position, text):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.image = pygame.transform.scale(image, (width, height))  # Adjust the size here
        self.rect = self.image.get_rect()
        print(f"Button rect: {self.rect}")
        self.rect.center = center_position
        print(f"Button center: {self.rect.center}")
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.y -= 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)