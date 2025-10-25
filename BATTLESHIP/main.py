import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

button = pygame.Rect(WIDTH/2, HEIGHT/2, 100, 50)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WIN.fill("white")
    pygame.draw.rect(WIN, "blue", button)
    
    pygame.display.flip()
    
pygame.quit()
