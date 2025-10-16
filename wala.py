import pygame
import random   

pygame.init()
WIDTH, HEIGHT = 720, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trojan Game")

clock = pygame.time.Clock()

pwidth, pheight = 20, 20
player = pygame.Rect((WIDTH/2), HEIGHT - pheight, pwidth, pheight)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    WIN.fill("white")
    pygame.draw.rect(WIN, "blue", player, 150)

    move = pygame.key.get_pressed()

    if move[pygame.K_a]:
        player.x -= 1
    if move[pygame.K_d]:
        player.x += 1
    if move[pygame.K_w]:
        player.y -= 1
    if move[pygame.K_s]:
        player.y += 1

    pygame.display.flip()

    
    clock.tick(60)
pygame.quit()
