import pygame
from view import view_constants as view_cst

class Button(pygame.sprite.Sprite):
    def __init__(self, image, width, height, relative_position, text, parent_surface):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
        self.text_rect = self.text_render.get_rect()

        print("Text rect: ", self.text_rect)
        print("Text rect left: ", self.text_rect.left)
        print("Text rect top: ", self.text_rect.top)

        print("Text render rect: ", self.text_render.get_rect())
        print("Text render rect left: ", self.text_render.get_rect().left)
        print("Text render rect top: ", self.text_render.get_rect().top)

        # Calculate the absolute position based on the parent surface's position and dimensions
        parent_rect = parent_surface.get_rect()
        print(f"Parent rect: {parent_rect}")
        print(f"Parent rect left: {parent_rect.left}")
        print(f"Parent rect top: {parent_rect.top}")
        self.rect.topleft = (parent_rect.left + relative_position[0], parent_rect.top + relative_position[1])
        print(f"Button rect: {self.rect}")
        print(f"Button rect left: {self.rect.left}")
        print(f"Button rect top: {self.rect.top}")

        self.text_rect.center = self.rect.center
        self.text_rect.y -= 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# class Button(pygame.sprite.Sprite):
#     def __init__(self, image, width, height, center_position, text):
#         pygame.sprite.Sprite.__init__(self)
#         self.original_image = image
#         self.image = pygame.transform.scale(image, (width, height))  # Adjust the size here
#         self.rect = self.image.get_rect()
#         self.text = text
#         self.font = pygame.font.SysFont("Arial", 30)
#         self.rect.center = center_position
#         self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
#         self.text_rect = self.text_render.get_rect()
#         self.text_rect.center = self.rect.center
#         self.text_rect.y -= 5
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#         surface.blit(self.text_render, self.text_rect)
#
#     def is_clicked(self, mouse_pos):
#         return self.rect.collidepoint(mouse_pos)