import pygame

""" Constants to handle the view of the game. """

''' Screen and tile constants'''
FPS = 60
WIDTH, HEIGHT = 1536, 960
H_TILES = 16
V_TILES = 10
TILE_WIDTH = WIDTH // H_TILES
TILE_HEIGHT = HEIGHT // V_TILES
MENU_BUTTON_HEIGHT = TILE_HEIGHT
PLAYABLE_AREA_HEIGHT = HEIGHT - MENU_BUTTON_HEIGHT
PLAYABLE_AREA_WIDTH = WIDTH

''' Colors '''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = BLACK
RED = (128, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 128)
PARCHMENT_COLOR = (225, 173, 109)
DARK_GRAY_2 = (50, 50, 50)  # A darker gray
DARK_GRAY = (100, 100, 100)  # A basic dark gray
LIGHT_GRAY = (150, 150, 150)  # A basic light gray
YELLOW = (200, 200, 0)  # A basic yellow
METAL_GRAY = (128, 128, 128)  # A basic metallic gray
HIGHLIGHT_COLOR = (180, 180, 180)  # A brighter gray for highlights
SCI_FI_BLUE = (120,204,226)
SCI_FI_BLUE_2 = (0, 150, 255)  # A sci-fi inspired blue for text
SCI_FI_BLUE_3 = (33, 179, 210)
SCI_FI_BLUE_4 = (0,80,102)  # A darker sci-fi inspired blue for text
SCI_FI_BLUE_5 = (24, 138, 180)
COFFEE_BROWN = (200, 190, 140)  # A coffee brown color for text
COFFEE_BROWN_2 = (150, 140, 100)  # A darker coffee brown color for text
COFFEE_BROWN_3 = (111, 78, 55)  # A darker coffee brown color for text
EARTH_BROWN = (100, 80, 50)
BLUE_GRAY = (90, 100, 120)

''' Fonts '''
#TODO: Figure out how to initialize fonts

# ARIAL_32 = pygame.font.SysFont("Arial", 32)
# ARIAL_24 = pygame.font.SysFont("Arial", 24)
# ARIAL_20 = pygame.font.SysFont("Arial", 20)
# ARIAL_16 = pygame.font.SysFont("Arial", 16)

''' Menu constants '''
QUEST_MENU = "quests"
INVENTORY_MENU = "inventory"
MAP_MENU = "map"
SETTINGS_MENU = "settings"

''' Dialogue constants '''

''' Button constants '''
WOOD_BUTTON = "./assets/buttons/wood_button.png"
WOOD_BUTTON_PRESSED = "./assets/buttons/wood_button_pressed.png"
STONE_BUTTON = "./assets/buttons/stone_button.png"
STONE_BUTTON_PRESSED = "./assets/buttons/stone_button_pressed.png"

''' Tiles constants '''
GRASS_ASSET_PATH = "./assets/maps/tiles/grass.png"
SAND_ASSET_PATH = "./assets/maps/tiles/sand.png"
ROCK_ASSET_PATH = "./assets/maps/tiles/rock.png"

''' Buildings constants '''
FRIENDLY_HOUSE_ASSET_PATH = "./assets/maps/buildings/house.png"