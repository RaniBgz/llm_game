""" Constants to handle the view of the game. """

WIDTH, HEIGHT = 1280, 720
H_TILES = 24
V_TILES = 8
TILE_WIDTH = WIDTH // H_TILES
TILE_HEIGHT = HEIGHT // V_TILES

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = BLACK
RED = (128, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 128)
POPUP_BG_COLOR = (225,173,109)
METAL_GRAY = (128, 128, 128)  # A basic metallic gray
HIGHLIGHT_COLOR = (180, 180, 180)  # A brighter gray for highlights
SCI_FI_BLUE = (0, 150, 255)  # A sci-fi inspired blue for text

FPS = 16
MOVEMENT_SPEED = 10

QUEST_MENU = "quests"
INVENTORY_MENU = "inventory"
MAP_MENU = "map"
