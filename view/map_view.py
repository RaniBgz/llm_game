import sys
import pygame
from view import view_constants as view_cst

map_path = "assets/maps/world_map.png"

class MapView:
    def __init__(self, screen):
        self.screen = screen
        # self.map_image = pygame.image.load(map_path).convert_alpha()
        # self.map_image = pygame.transform.scale(self.map_image, (view_cst.WIDTH, view_cst.HEIGHT))
        #TODO: Replace dimensions of the surface
        self.width = view_cst.WIDTH
        self.height = view_cst.HEIGHT
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()


        self.exit_font = pygame.font.SysFont("Arial", 30)
        self.back_button_text = self.exit_font.render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))
        self.grid_rects = []
        self.x_size = 0
        self.y_size = 0
        self.cell_size = 0
        self.map_biomes = {}  # Use a dictionary for coordinate-based lookup
        #TODO: Set size of a grid cell (doesn't have to be equal to tile size)
        #TODO: reduce number of operations if possible


    def set_map_size(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.cell_size = min(self.height, self.width) // self.x_size
    def set_biome_asset(self, x, y, asset_path):
        self.map_biomes[(x, y)] = asset_path

    #TODO: Get the dimensions of the map
    def draw_grid(self):
        self.surface.fill(view_cst.WHITE)
        grid_color = (50, 50, 50)  # Dark grey grid color

        for i in range(self.x_size + 1): # Draw horizontal lines
            start_pos = (0, i * self.cell_size)
            # end_pos = (self.x_size * view_cst.TILE_HEIGHT, i * view_cst.TILE_HEIGHT)
            end_pos = (self.x_size * self.cell_size, i * self.cell_size)
            pygame.draw.line(self.surface, grid_color, start_pos, end_pos, width=1)

        for j in range(self.y_size + 1): # Draw vertical lines
            start_pos = (j * self.cell_size, 0)
            # end_pos = (j * view_cst.TILE_WIDTH, self.y_size * view_cst.TILE_WIDTH)
            end_pos = (j * self.cell_size, self.height)
            pygame.draw.line(self.surface, grid_color, start_pos, end_pos, width=1)

        # Calculate and store cell rectangles
        for y in range(self.x_size):
            for x in range(self.y_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                # rect = pygame.Rect(x * view_cst.TILE_WIDTH, y * view_cst.TILE_HEIGHT,
                #                    view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT)
                self.grid_rects.append(rect)
                image = self.map_biomes[(x, y)]
                image = pygame.image.load(image).convert_alpha()
                # image = pygame.transform.scale(image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
                image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
                self.surface.blit(image, rect.topleft)

    def render(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.draw_grid()
        self.screen.blit(self.surface, self.rect)
        pygame.display.update()
        # pygame.display.flip()
