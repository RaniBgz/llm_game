import pygame
class BackButton:
    def __init__(self, screen, text, rect):
        self.screen = screen
        self.text = text
        self.rect = rect

    def draw(self):
        self.screen.blit(self.text, self.rect)

    def collidepoint(self, point):
        return self.rect.collidepoint(point)