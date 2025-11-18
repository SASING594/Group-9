import pygame
import random
from constants import TILE, ROWS, COLS, BLACK

class Ship:
    def __init__(self, name, size, color, index):
        self.name = name
        self.size = size
        self.color = color
        # Initial position: right of board (x=550), aligned vertically starting from y=100, spaced by 60 pixels
        self.initial_x = 550
        self.initial_y = 100 + index * 60
        self.rect = pygame.Rect(self.initial_x, self.initial_y, size * TILE, TILE)
        self.placed = False
        self.positions = []
        self.dragging = False
        self.offset = (0, 0)
        self.horizontal = True

    def draw(self, win, board_rect):
        if not self.placed:
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.rect(win, BLACK, self.rect, 2)
        else:
            for row, col in self.positions:
                pygame.draw.rect(win, self.color, 
                               (board_rect.x + row * TILE, board_rect.y + col * TILE, TILE, TILE))
                pygame.draw.rect(win, BLACK, 
                               (board_rect.x + row * TILE, board_rect.y + col * TILE, TILE, TILE), 2)

    def rotate(self):
        self.horizontal = not self.horizontal
        if self.horizontal:
            self.rect.width = self.size * TILE
            self.rect.height = TILE
        else:
            self.rect.width = TILE
            self.rect.height = self.size * TILE

    def snap_to_grid(self, board_rect):
        center = self.rect.center
        x, y = center
        if board_rect.collidepoint(x, y):
            row = (x - board_rect.x) // TILE
            col = (y - board_rect.y) // TILE
            if self.horizontal:
                if row + self.size <= ROWS and 0 <= col < COLS:
                    self.rect.topleft = (board_rect.x + row * TILE, board_rect.y + col * TILE)
                    self.positions = [(row + i, col) for i in range(self.size)]
                    return True
            else:
                if 0 <= row < ROWS and col + self.size <= COLS:
                    self.rect.topleft = (board_rect.x + row * TILE, board_rect.y + col * TILE)
                    self.positions = [(row, col + i) for i in range(self.size)]
                    return True
        return False

    def unplace(self):
        self.placed = False
        self.positions = []
        self.rect = pygame.Rect(self.initial_x, self.initial_y, self.size * TILE, TILE)
        self.horizontal = True
