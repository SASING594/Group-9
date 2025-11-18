import pygame

# Window dimensions
WIDTH = 1200
HEIGHT = 700

# Board settings
ROWS = 10
COLS = 10
TILE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
CYAN = (0, 255, 255)

# Ship definitions
SHIPS = [
    {"name": "Carrier", "size": 5, "color": RED},
    {"name": "Battleship", "size": 4, "color": BLUE},
    {"name": "Cruiser", "size": 3, "color": GREEN},
    {"name": "Submarine", "size": 3, "color": YELLOW},
    {"name": "Destroyer", "size": 2, "color": PURPLE},
]

# Initialize Pygame components
pygame.init()
pygame.mixer.init()  # Initialize mixer for music
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BATTLESHIP")
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Load and play background music

pygame.mixer.music.load("tingtingting.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely
bg = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
tile_img = pygame.transform.scale(pygame.image.load("tile.png"), (TILE, TILE))
hit_img = pygame.transform.scale(pygame.image.load("hit.jpeg"), (TILE, TILE))
miss_img = pygame.transform.scale(pygame.image.load("miss.png"), (TILE, TILE))

# Board rectangles
player_board = pygame.Rect(50, 100, 500, 500)
opponent_board = pygame.Rect(650, 100, 500, 500)
