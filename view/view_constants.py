""" Constants to handle the view of the game. """

WIDTH, HEIGHT = 1280, 720
H_TILES = 24
V_TILES = 8
TILE_WIDTH = WIDTH // H_TILES
TILE_HEIGHT = HEIGHT // V_TILES

MENU_BUTTON_HEIGHT = TILE_HEIGHT
PLAYABLE_AREA_HEIGHT = HEIGHT - MENU_BUTTON_HEIGHT
PLAYABLE_AREA_WIDTH = WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = BLACK
RED = (128, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 128)
POPUP_BG_COLOR = (225,173,109)

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
COFFEE_BROWN = (200, 190, 140)  # A coffee brown color for text
COFFEE_BROWN_2 = (150, 140, 100)  # A darker coffee brown color for text
COFFEE_BROWN_3 = (111, 78, 55)  # A darker coffee brown color for text

FPS = 60
MOVEMENT_SPEED = 10

QUEST_MENU = "quests"
INVENTORY_MENU = "inventory"
MAP_MENU = "map"
SETTINGS_MENU = "settings"
