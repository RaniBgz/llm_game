""" Constants to handle the view of the game. """

WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = BLACK
RED = (255, 0, 0)

SPAWN_POSITIONS = [
    (WIDTH // 4, HEIGHT // 4),  # top left
    (WIDTH // 2, HEIGHT // 4),  # top middle
    (3 * WIDTH // 4, HEIGHT // 4),  # top right
    (WIDTH // 4, HEIGHT // 2),  # middle left
    (WIDTH // 2, HEIGHT // 2),  # middle
    (3 * WIDTH // 4, HEIGHT // 2),  # middle right
    (WIDTH // 4, 3 * HEIGHT // 4),  # bottom left
    (WIDTH // 2, 3 * HEIGHT // 4),  # bottom middle
    (3 * WIDTH // 4, 3 * HEIGHT // 4)  # bottom right
]

SPAWN_POSITIONS_DICT = {
    "top_left": (WIDTH // 4, HEIGHT // 4),
    "top_middle": (WIDTH // 2, HEIGHT // 4),
    "top_right": (3 * WIDTH // 4, HEIGHT // 4),
    "middle_left": (WIDTH // 4, HEIGHT // 2),
    "middle": (WIDTH // 2, HEIGHT // 2),
    "middle_right": (3 * WIDTH // 4, HEIGHT // 2),
    "bottom_left": (WIDTH // 4, 3 * HEIGHT // 4),
    "bottom_middle": (WIDTH // 2, 3 * HEIGHT // 4),
    "bottom_right": (3 * WIDTH // 4, 3 * HEIGHT // 4)
}