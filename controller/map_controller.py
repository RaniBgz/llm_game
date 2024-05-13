import sys
import pygame
from model.map.biome import Biome
import view.view_constants as view_cst


class MapController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view
        self.view.set_map_size(self.game_data.world_map.x_size, self.game_data.world_map.y_size)
        self.set_map_biomes_asset()
        self.view.initialize_text()
        self.running = True

    def set_map_biomes_asset(self):
        #Iterate through world map grid
        #For each cell, check the type of biome of the local map
        #Set the asset path for the corresponding cell in the view
        for x in range(self.game_data.world_map.x_size):
            for y in range(self.game_data.world_map.y_size):
                local_map = self.game_data.world_map.get_local_map_at(x, y)
                #TODO: Handle that logic in a cleaner way
                if local_map.biome == Biome.PLAIN:
                    self.view.set_biome_asset(x, y, view_cst.GRASS_ASSET_PATH)
                    # print(f"Biome asset is grass_tile at ({x}, {y})")
                elif local_map.biome == Biome.DESERT:
                    self.view.set_biome_asset(x, y, view_cst.SAND_ASSET_PATH)
                elif local_map.biome == Biome.MOUNTAIN:
                    self.view.set_biome_asset(x, y, view_cst.ROCK_ASSET_PATH)
                    # print(f"Biome asset is sand_tile at ({x}, {y})")


    def initialize_map_biomes(self):
        map_biomes = {}
        for x in range(self.game_data.world_map.x_size):
            for y in range(self.game_data.world_map.y_size):
                local_map = self.game_data.world_map.get_local_map_at(x, y)
                map_biomes[(x, y)] = local_map.biome
        self.view.initialize_map_biomes(map_biomes)

    def run(self):
        while self.running:
            self.view.render()
            return_coordinates = self.handle_events()
            if return_coordinates:
                return return_coordinates

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                teleport_coordinates = self.handle_mouse_down_events(event)
                if teleport_coordinates:
                    self.running = False
                    return teleport_coordinates
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up_events(event)
            elif event.type == pygame.MOUSEMOTION:  # Add handling for mouse motion
                self.handle_mouse_motion_events(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False  # Update how we handle exiting


    #TODO: on click, teleport character to that map
    #TODO: add village and dungeon biomes
    #TODO: Change the tile that appears on the map to signify village or dungeon
    #TODO: change the actual layout of the map to put a building in the middle
    #TODO: Add a way to name zones
    #TODO: Fix current LLM prompts to generate quests and dialogue
    #TODO: Modify context to handle location
    #TODO: add location type of objective and test
    #TODO: start thinking about character graphs
    def handle_mouse_down_events(self, event):
        mouse_pos = event.pos
        if self.view.back_button_rect.collidepoint(mouse_pos):
            self.running = False  # Exit the map view
        for coords, rect in self.view.grid_rects_dict.items():
            if rect.collidepoint(mouse_pos):
                x, y = coords
                biome = self.game_data.world_map.get_local_map_at(x, y).biome
                teleport_coordinates = (x, y)
                return teleport_coordinates

    #TODO: Calls could be optimized to not go look in the world map to get the biome, but in the initialized map_biomes
    def handle_mouse_up_events(self, event):
        pass
    def handle_mouse_motion_events(self, event):
        mouse_pos = event.pos

        for coords, rect in self.view.grid_rects_dict.items():
            if rect.collidepoint(mouse_pos):
                x, y = coords
                biome = self.game_data.world_map.get_local_map_at(x, y).biome
                self.view.update_info_display(coords, biome.name)
                # print(f"Hovering over cell at coordinates: ({x}, {y}), Biome: {biome}")