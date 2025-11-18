import random
from constants import ROWS, COLS, SHIPS
from ship import Ship

def place_ai_ships():
    ai_ships = []
    occupied = set()
    for ship_data in SHIPS:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            attempts += 1
            horizontal = random.choice([True, False])
            if horizontal:
                row = random.randint(0, ROWS - ship_data["size"])
                col = random.randint(0, COLS - 1)
                positions = [(row + i, col) for i in range(ship_data["size"])]
            else:
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, COLS - ship_data["size"])
                positions = [(row, col + i) for i in range(ship_data["size"])]
            
            if all((r, c) not in occupied for r, c in positions):
                occupied.update(positions)
                ai_ship = Ship(ship_data["name"], ship_data["size"], ship_data["color"], 0)
                ai_ship.positions = positions
                ai_ship.placed = True
                ai_ship.horizontal = horizontal
                ai_ships.append(ai_ship)
                placed = True
    return ai_ships

def ai_shoot(player_ships, shots):
    possible_shots = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in [s[0] for s in shots]]
    if not possible_shots:
        return None
    
    # Hunt mode: find adjacent cells to hits
    for shot in reversed(shots):
        if shot[1] == "hit":
            r, c = shot[0]
            hunt_targets = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
            hunt_targets = [t for t in hunt_targets if 0 <= t[0] < ROWS and 0 <= t[1] < COLS and t in possible_shots]
            if hunt_targets:
                return random.choice(hunt_targets)
    
    return random.choice(possible_shots)

def is_ship_sunk(ship, shots):
    hit_positions = [pos for pos, result in shots if result == "hit"]
    return set(ship.positions).issubset(set(hit_positions))

def all_ships_sunk(ships, shots):
    for ship in ships:
        if not is_ship_sunk(ship, shots):
            return False
    return True
