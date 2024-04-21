import pygame
import sys
from src.characters import Player
from src.levels import Level, MainHall, LeftStairs, RightStairs, LeftCorridor, RightCorridor, IndependenceHall, Door
from src.menu import Menu

pygame.init()

WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Chance")

# Create Level and Rooms
level = Level()
main_hall = MainHall()
left_stairs = LeftStairs()
right_stairs = RightStairs()
left_corridor = LeftCorridor()
right_corridor = RightCorridor()
independence_hall = IndependenceHall()

# Add Rooms to Level (with indices)
level.add_room(main_hall, 0)       
level.add_room(left_stairs, 1)    
level.add_room(right_stairs, 2)   
level.add_room(left_corridor, 3)  
level.add_room(right_corridor, 4) 
level.add_room(independence_hall, 5)  

# --- Doors for Main Hall ---
door1 = Door(x=100, y=200, width=50, height=100, target_room_index=1)  # To Left Stairs (adjust left side of the hall)
main_hall.doors.append(door1)
level.add_door(door1)

door2 = Door(x=700, y=200, width=50, height=100, target_room_index=2)  # To Right Stairs (adjust right side of the hall)
main_hall.doors.append(door2)
level.add_door(door2)

door3 = Door(x=400, y=500, width=50, height=100, target_room_index=5)  # To Independence Hall (adjust bottom center)
main_hall.doors.append(door3)
level.add_door(door3)

# --- Doors for Left Stairs --- 
door4 = Door(x=10, y=10, width=50, height=100, target_room_index=0)  # To Main Hall (top of the stairs) 
left_stairs.doors.append(door4)
level.add_door(door4)

door5 = Door(x=800, y=500, width=50, height=100, target_room_index=3)  # To Left Corridor (bottom of the stairs) 
left_stairs.doors.append(door5)
level.add_door(door5)

# --- Doors for Right Stairs --- 
door6 = Door(x=10, y=10, width=50, height=100, target_room_index=0)  # To Main Hall (top of the stairs)
right_stairs.doors.append(door6)
level.add_door(door6)

door7 = Door(x=10, y=500, width=50, height=100, target_room_index=4)  # To Right Corridor (bottom of the stairs)
right_stairs.doors.append(door7)
level.add_door(door7)

# --- Doors for Left Corridor --- 
door8 = Door(x=10, y=250, width=50, height=100, target_room_index=1)  # To Left Stairs (adjust left end of corridor)
left_corridor.doors.append(door8)
level.add_door(door8)

# --- Doors for Right Corridor --- 
door9 = Door(x=800, y=250, width=50, height=100, target_room_index=2)  # To Right Stairs (adjust right end of corridor)
right_corridor.doors.append(door9)
level.add_door(door9)

# --- Doors for Independence Hall --- 
door10 = Door(x=400, y=10, width=50, height=100, target_room_index=0)  # To Main Hall (top center)
independence_hall.doors.append(door10) 
level.add_door(door10)

# Create Player
player = Player(10, 10, level) 

# Menu Setup
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu
menu.current_menu = menu

GAME_STATES = {
    "MENU": 0,
    "GAME": 1
}
current_state = GAME_STATES["MENU"]  # Start in the menu state

# Game Loop
clock = pygame.time.Clock()
while True:
    events = pygame.event.get()

    if current_state == GAME_STATES["MENU"]:
        menu.current_menu.update(events)
        menu.current_menu.draw(screen)

    elif current_state == GAME_STATES["GAME"]:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update()  # Update player (handle movement, etc.)
        level.check_door_collisions(player) 

        screen.fill((0, 0, 0))
        level.current_room.draw(screen) 
        player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    # Check for Menu Interaction (in the menu state)
    for event in events:
        if current_state == GAME_STATES["MENU"] and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(menu.current_menu.buttons):
                if button.is_clicked(event) and i == 0:  # Play button clicked (adjust index if needed)
                    current_state = GAME_STATES["GAME"]  # Switch to the game state