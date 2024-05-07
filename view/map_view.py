import sys
import pygame
from view import view_constants as view_cst

map_path = "assets/maps/world_map.png"

class MapView:
    def __init__(self, screen):
        self.screen = screen
        #TODO: Replace dimensions of the surface
        self.width = view_cst.WIDTH
        self.height = view_cst.HEIGHT
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()


        self.exit_font = pygame.font.SysFont("Arial", 30)
        self.info_font = pygame.font.SysFont("Arial", 24)  # Font for the info text
        self.back_button_text = self.exit_font.render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

        self.grid_rects_dict = {}
        self.x_size = 0
        self.y_size = 0
        self.cell_size = 0
        self.grid_width = 0
        self.grid_height = 0
        self.map_biomes = {}  # Use a dictionary for coordinate-based lookup


    def set_map_size(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.cell_size = min(self.height, self.width) // self.x_size
        self.grid_width = self.cell_size * self.x_size
        self.grid_height = self.cell_size * self.y_size

    def set_biome_asset(self, x, y, asset_path):
        self.map_biomes[(x, y)] = asset_path

    def initialize_text(self):
        print(f"Initializing text")
        # Coordinate Text Setup
        self.coord_label_text = self.info_font.render("Coordinates: ", True, view_cst.TEXT_COLOR)
        self.coord_label_rect = self.coord_label_text.get_rect(midleft=(self.grid_width + 20, 50))

        self.coord_display_text = self.info_font.render("(-, -)", True, view_cst.TEXT_COLOR)
        self.coord_display_rect = self.coord_display_text.get_rect(midleft=(self.grid_width + 20, 80))

        # Biome Text Setup
        self.biome_label_text = self.info_font.render("Biome: ", True, view_cst.TEXT_COLOR)
        self.biome_label_rect = self.biome_label_text.get_rect(midleft=(self.grid_width + 20, 120))

        self.biome_display_text = self.info_font.render("None", True, view_cst.TEXT_COLOR)
        self.biome_display_rect = self.biome_display_text.get_rect(midleft=(self.grid_width + 20, 150))


    def update_info_display(self, coords, biome):
        self.coord_display_text = self.info_font.render(f"({coords[0]}, {coords[1]})", True, view_cst.TEXT_COLOR)
        self.biome_display_text = self.info_font.render(biome, True, view_cst.TEXT_COLOR)

    def draw_grid(self):
        self.surface.fill(view_cst.WHITE)
        grid_color = (50, 50, 50)  # Dark grey grid color

        for i in range(self.x_size + 1): # Draw horizontal lines
            start_pos = (0, i * self.cell_size)
            end_pos = (self.x_size * self.cell_size, i * self.cell_size)
            pygame.draw.line(self.surface, grid_color, start_pos, end_pos, width=1)

        for j in range(self.y_size + 1): # Draw vertical lines
            start_pos = (j * self.cell_size, 0)
            end_pos = (j * self.cell_size, self.height)
            pygame.draw.line(self.surface, grid_color, start_pos, end_pos, width=1)

        for y in range(self.x_size): # Calculate and store cell rectangles
            for x in range(self.y_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                self.grid_rects_dict[(x, y)] = rect
                image = self.map_biomes[(x, y)]
                image = pygame.image.load(image).convert_alpha()
                image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                self.surface.blit(image, rect.topleft)

    def render(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.draw_grid()
        self.surface.blit(self.coord_label_text, self.coord_label_rect)
        self.surface.blit(self.coord_display_text, self.coord_display_rect)
        self.surface.blit(self.biome_label_text, self.biome_label_rect)
        self.surface.blit(self.biome_display_text, self.biome_display_rect)
        self.screen.blit(self.surface, self.rect)
        pygame.display.update()
