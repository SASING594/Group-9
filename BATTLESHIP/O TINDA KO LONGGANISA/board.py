import pygame
from constants import TILE, ROWS, COLS, BLACK

def draw_board_with_grid(win, board_rect, tile_img):
    pygame.draw.rect(win, BLACK, board_rect, 3)
    for r in range(ROWS):
        for c in range(COLS):
            win.blit(tile_img, (board_rect.x + r * TILE, board_rect.y + c * TILE))
    for r in range(1, ROWS):
        pygame.draw.line(win, BLACK, (board_rect.x, board_rect.y + r * TILE), 
                        (board_rect.x + 500, board_rect.y + r * TILE), 1)
    for c in range(1, COLS):
        pygame.draw.line(win, BLACK, (board_rect.x + c * TILE, board_rect.y), 
                        (board_rect.x + c * TILE, board_rect.y + 500), 1)

def get_grid_pos(mouse_pos, board_rect):
    x, y = mouse_pos
    if board_rect.collidepoint(x, y):
        row = (x - board_rect.x) // TILE
        col = (y - board_rect.y) // TILE
        if 0 <= row < ROWS and 0 <= col < COLS:
            return row, col
    return None

def check_overlap(ship, placed_ships):
    for p_ship in placed_ships:
        if set(ship.positions) & set(p_ship.positions):
            return True
    return False
