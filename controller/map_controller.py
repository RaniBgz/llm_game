import sys
import pygame
from model.map.biome import Biome


class MapController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view
        self.view.set_map_size(self.game_data.world_map.x_size, self.game_data.world_map.y_size)
        self.set_map_biomes_asset()

    def set_map_biomes_asset(self):
        #Iterate through world map grid
        #For each cell, check the type of biome of the local map
        #Set the asset path for the corresponding cell in the view
        for x in range(self.game_data.world_map.x_size):
            for y in range(self.game_data.world_map.y_size):
                local_map = self.game_data.world_map.get_local_map_at(x, y)
                if local_map.biome == Biome.PLAIN:
                    self.view.set_biome_asset(x, y, "./assets/maps/tiles/grass.png")
                    print(f"Biome asset is grass_tile at ({x}, {y})")
                else:
                    self.view.set_biome_asset(x, y, "./assets/maps/tiles/sand.png")
                    print(f"Biome asset is sand_tile at ({x}, {y})")


    def initialize_map_biomes(self):
        map_biomes = {}
        for x in range(self.game_data.world_map.x_size):
            for y in range(self.game_data.world_map.y_size):
                local_map = self.game_data.world_map.get_local_map_at(x, y)
                map_biomes[(x, y)] = local_map.biome
        self.view.initialize_map_biomes(map_biomes)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.view.render()

