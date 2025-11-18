import pygame
import time
import random
from constants import *
from ship import Ship
from board import draw_board_with_grid, get_grid_pos, check_overlap
from game_logic import place_ai_ships, ai_shoot, all_ships_sunk

# Game variables
player_ships = [Ship(s["name"], s["size"], s["color"], i) for i, s in enumerate(SHIPS)]
ai_ships = place_ai_ships()  # Place AI ships immediately
player_shots = []
ai_shots = []
current_player = "player"
phase = "placement"  # Start directly in placement
logo_timer = 0
current_logo = None
winner = None
ai_delay = 0
play_button = pygame.Rect(825, 325, 100, 50)  # Centered at x=875, y=350
battle_start_time = 0  # For 1-second delay after pressing play

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    WIN.blit(bg, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if phase == "placement":
                if event.key == pygame.K_r:
                    for ship in player_ships:
                        if not ship.placed and ship.rect.collidepoint(mouse_pos):
                            ship.rotate()
            
            elif phase == "battle":
                if winner and event.key == pygame.K_r:
                    player_ships = [Ship(s["name"], s["size"], s["color"], i) for i, s in enumerate(SHIPS)]
                    ai_ships = place_ai_ships()
                    player_shots = []
                    ai_shots = []
                    current_player = "player"
                    phase = "placement"
                    winner = None
                    battle_start_time = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and phase == "placement":  # Right-click to undo
                for ship in player_ships:
                    if ship.placed and ship.rect.collidepoint(mouse_pos):
                        ship.unplace()
            elif event.button == 1 and phase == "placement" and all(s.placed for s in player_ships):
                if play_button.collidepoint(mouse_pos):
                    phase = "battle"
                    current_player = "player"
                    battle_start_time = time.time()

    if phase == "placement":
        draw_board_with_grid(WIN, player_board, tile_img)
        
        placed_ships = [s for s in player_ships if s.placed]
        for ship in player_ships:
            ship.draw(WIN, player_board)
        
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            for ship in player_ships:
                if not ship.placed and ship.rect.collidepoint(mouse_pos) and not ship.dragging:
                    ship.dragging = True
                    ship.offset = (ship.rect.x - mouse_pos[0], ship.rect.y - mouse_pos[1])
                if ship.dragging:
                    ship.rect.x = mouse_pos[0] + ship.offset[0]
                    ship.rect.y = mouse_pos[1] + ship.offset[1]
        else:
            for ship in player_ships:
                if ship.dragging:
                    ship.dragging = False
                    if ship.snap_to_grid(player_board) and not check_overlap(ship, placed_ships):
                        ship.placed = True
                    else:
                        ship.rect.topleft = (ship.initial_x, ship.initial_y)
        
        text = small_font.render("Your Board - Drag ships to place. Press R to rotate. Right-click placed ships to undo.", True, CYAN)
        WIN.blit(text, (50, 50))
        
        remaining = [s.name for s in player_ships if not s.placed]
        if remaining:
            remain_text = small_font.render(f"Remaining: {', '.join(remaining)}", True, CYAN)
            WIN.blit(remain_text, (50, 75))
        
        # Draw Play button
        button_color = CYAN if all(s.placed for s in player_ships) else GRAY
        pygame.draw.rect(WIN, button_color, play_button)
        pygame.draw.rect(WIN, BLACK, play_button, 2)
        button_text = small_font.render("PLAY", True, BLACK)
        WIN.blit(button_text, (play_button.x + 20, play_button.y + 15))
        
    elif phase == "battle":
        # Draw player board
        draw_board_with_grid(WIN, player_board, tile_img)
        for ship in player_ships:
            ship.draw(WIN, player_board)
        
        for pos, result in ai_shots:
            img = hit_img if result == "hit" else miss_img
            WIN.blit(img, (player_board.x + pos[0] * TILE, player_board.y + pos[1] * TILE))
        
        # Draw opponent board
        draw_board_with_grid(WIN, opponent_board, tile_img)
        
        for pos, result in player_shots:
            img = hit_img if result == "hit" else miss_img
            WIN.blit(img, (opponent_board.x + pos[0] * TILE, opponent_board.y + pos[1] * TILE))
        
        # Handle shooting naa ni delay gamay para dili mo auto-click sa board
        if not winner and time.time() - battle_start_time >= 1:
            if current_player == "player":
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    time.sleep(0.2)  # Prevent double clicks
                    grid_pos = get_grid_pos(mouse_pos, opponent_board)
                    if grid_pos and grid_pos not in [s[0] for s in player_shots]:
                        hit = any(grid_pos in ship.positions for ship in ai_ships)
                        player_shots.append((grid_pos, "hit" if hit else "miss"))
                        current_logo = "hit" if hit else "miss"
                        logo_timer = time.time() + 1.5
                        if all_ships_sunk(ai_ships, player_shots):
                            winner = "Player"
                        else:
                            current_player = "ai"
                            ai_delay = time.time() + 1
            
            elif current_player == "ai" and time.time() > ai_delay:
                ai_shot = ai_shoot(player_ships, ai_shots)
                if ai_shot:
                    hit = any(ai_shot in ship.positions for ship in player_ships)
                    ai_shots.append((ai_shot, "hit" if hit else "miss"))
                    current_logo = "hit" if hit else "miss"
                    logo_timer = time.time() + 1.5
                    if all_ships_sunk(player_ships, ai_shots):
                        winner = "AI"
                    else:
                        current_player = "player"
        
        if winner:
            win_text = font.render(f"{winner} Wins! Press R to restart.", True, GREEN)
            WIN.blit(win_text, (WIDTH//2 - 150, HEIGHT//2))

        
        #This is indented since under ni sa "ai" nga board
        marines_text = small_font.render("MARINES", True, CYAN)
        WIN.blit(marines_text, (650, 610))
    straw_hat_text = small_font.render("STRAW HAT", True, CYAN)
    WIN.blit(straw_hat_text, (50, 610))

            
    pygame.display.update()

pygame.quit()
