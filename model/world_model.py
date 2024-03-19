import pygame

class WorldModel:
    def __init__(self):
        self.map_grid = {}  # Use a dictionary for coordinate-based lookup
        self.current_map_coords = (0, 0)

    # def load_map(self, coords):
    #     if coords not in self.map_grid:
    #        self.map_grid[coords] = load_map_from_file(coords)  # Implement your map loading

    def get_current_map(self):
        return self.map_grid[self.current_map_coords]