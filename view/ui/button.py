import pygame
from view import view_constants as view_cst



class Button(pygame.sprite.Sprite):
    def __init__(self, image, center_position, text):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.image = pygame.transform.scale(image, (400, 200))  # Adjust the size here
        self.rect = self.image.get_rect()
        print(f"Button rect: {self.rect}")
        self.rect.center = center_position
        print(f"Button center: {self.rect.center}")
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_render = self.font.render(self.text, True, view_cst.DARK_GRAY_2)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.rect.center
        self.text_rect.y -= 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)


# class Button(pygame.sprite.Sprite):
#     def __init__(self, image, position, text):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.topleft = position
#         self.text = text
#         self.font = pygame.font.SysFont("Arial", 30)
#         self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
#         self.text_rect = self.text_render.get_rect(center=self.rect.center)
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#         surface.blit(self.text_render, self.text_rect)
