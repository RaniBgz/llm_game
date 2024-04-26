import pygame
from view import view_constants as view_cst

class Button(pygame.sprite.Sprite):
    def __init__(self, image, width, height, relative_position, text, parent_offset=(0, 0), pressed_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.parent_offset = parent_offset
        self.relative_position = relative_position
        self.original_image = image
        self.image = pygame.transform.scale(image, (width, height))
        self.pressed_image = pressed_image
        # if pressed_image:
        #     self.pressed_image = pygame.transform.scale(pressed_image, (width, height))
        #     print(f"Pressed image is {self.pressed_image}")
        # else:
        #     self.pressed_image = self.image

        self.rect = self.image.get_rect()
        self.text = text
        self.font = pygame.font.SysFont("Arial", 30)
        self.text_render = self.font.render(self.text, True, view_cst.TEXT_COLOR)
        self.text_rect = self.text_render.get_rect()

        self.rect.topleft = (relative_position[0], relative_position[1])

        self.text_rect.center = self.rect.center
        self.text_rect.y -= 5

    def draw(self, surface):
        self.true_rect = pygame.Rect(self.rect.topleft[0] + self.parent_offset[0],
                                     self.rect.topleft[1] + self.parent_offset[1], self.rect.width, self.rect.height)
        print(f"In draw button")
        surface.blit(self.image, self.rect)
        surface.blit(self.text_render, self.text_rect)

    # def press(self):
    #     self.image = pygame.transform.scale(self.pressed_image, self.rect.size)
    #     self.draw(self.parent)
    #
    # def release(self):
    #     self.image = pygame.transform.scale(self.original_image, self.rect.size)
    #     self.draw(self.parent)


    def is_clicked(self, mouse_pos):
        return self.true_rect.collidepoint(mouse_pos)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.true_rect.collidepoint(event.pos):
                self.is_pressed = True
                self.image = pygame.transform.scale(self.pressed_image, (self.rect.width, self.rect.height))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False
            self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))