import pygame

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class MainGameView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont("Arial", 25)
        self.quests_text = self.button_font.render("Quests", True, RED)
        self.quests_rect = self.quests_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
        self.inventory_text = self.button_font.render("Inventory", True, RED)
        self.inventory_rect = self.inventory_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 150))
        self.map_text = self.button_font.render("Map", True, RED)
        self.map_rect = self.map_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
        self.world_text = self.button_font.render("World", True, RED)
        self.world_rect = self.world_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 250))

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.quests_text, self.quests_rect)
        self.screen.blit(self.inventory_text, self.inventory_rect)
        self.screen.blit(self.map_text, self.map_rect)
        self.screen.blit(self.world_text, self.world_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle button clicks
            pass

    def update(self, state):
        pass
        # update game display elements based on state

    def render(self):
        pass
        # render game display elements on screen