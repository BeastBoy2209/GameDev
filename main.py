import pygame
import sys
from src.characters import Player, Character, QuestCharacter
from src.levels import Level, Wall, MainHall, LeftStairs, RightStairs, LeftCorridor, RightCorridor, IndependenceHall, Door
from src.menu import Menu

pygame.init()

WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Chance")

player_speed = 5

# Создание прямоугольников для стен
wall_rect1 = pygame.Rect(351, 9, 208, 58)
wall_rect2 = pygame.Rect(789, 9, 208, 58)
wall_rect3 = pygame.Rect(942, 10, 58, 208)
wall_rect4=pygame.Rect(1509, 256, 58, 208)

# Создание объектов стен с передачей прямоугольников
wall1 = Wall(wall_rect1)
wall2 = Wall(wall_rect2)
wall3= Wall(wall_rect3)
wall4= Wall(wall_rect4)

# Установка прозрачности стен
wall_alpha = 100  # Прозрачность первой стены (значение альфа)
wall1.image.set_alpha(wall_alpha)
wall2.image.set_alpha(wall_alpha)
wall3.image.set_alpha(wall_alpha)
wall4.image.set_alpha(wall_alpha)

# Create Level and Rooms
level = Level()
main_hall = MainHall()
left_stairs = LeftStairs()
right_stairs = RightStairs()
left_corridor = LeftCorridor()
right_corridor = RightCorridor()
independence_hall = IndependenceHall()

# Add Walls to Level
level.add_wall(wall1)
level.add_wall(wall2)

# Add Rooms to Level (with indices)
level.add_room(main_hall, 0)       
level.add_room(left_stairs, 1)    
level.add_room(right_stairs, 2)   
level.add_room(left_corridor, 3)  
level.add_room(right_corridor, 4) 
level.add_room(independence_hall, 5)  

# --- Doors for Main Hall ---
door1 = Door(559, 45, 229, 23, 1, 1)  # To Left Stairs 
main_hall.doors.append(door1)


door2 = Door(578, 919, 211, 22, 2, 2)  # To Right Stairs 
main_hall.doors.append(door2)


door3 = Door(1357, 370, 19, 190, 5, 3)  # To Independence Hall 
main_hall.doors.append(door3)


# --- Doors for Left Stairs --- 
door4 = Door(665, 818, 168, 21, 0, 4)  # To Main Hall  
left_stairs.doors.append(door4)


door5 = Door(1380, 190, 14, 363, 3, 5)  # To Left Corridor 
left_stairs.doors.append(door5)


# --- Doors for Right Stairs --- 
door6 = Door(657, 185, 169, 13, 0, 6)  # To Main Hall 
right_stairs.doors.append(door6)


door7 = Door(1369, 466, 18, 363, 4, 7)  # To Right Corridor 
right_stairs.doors.append(door7)


# --- Doors for Left Corridor --- 
door8 = Door(0, 341, 14, 275, 1, 8)  # To Left Stairs 
left_corridor.doors.append(door8)


# --- Doors for Right Corridor --- 
door9 = Door(0, 342, 14, 276, 2, 9)  # To Right Stairs
right_corridor.doors.append(door9)


# --- Doors for Independence Hall --- 
door10 = Door(160, 366, 20, 250, 0, 10)  # To Main Hall 
independence_hall.doors.append(door10) 


# Create Player
player = Player(10, 10, level) 
player.rect.x = 442 
player.rect.y = 449

# Create Quest Characters
independence_hall_character = QuestCharacter(r"data\images\Kelg.PNG", 929, 455, "Welcome to Independence Hall!")
left_corridor_character = QuestCharacter(r"data\images\Usu.PNG", 1287, 126, "Psst, hey kid... I've got a job for you.")

# Add them to the respective rooms
independence_hall.characters.append(independence_hall_character)
left_corridor.characters.append(left_corridor_character)

# Menu Setup
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu
menu.current_menu = menu

GAME_STATES = {
    "MENU": 0,
    "GAME": 1
}
current_state = GAME_STATES["MENU"] 

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

        player.update()
        level.check_door_collisions(player)
        player.check_character_interactions(events)

        screen.fill((0, 0, 0))  
        level.current_room.draw(screen)  
        for wall in level.walls:
            screen.blit(wall.image, wall.rect)
        player.draw(screen)
        
        pygame.display.flip()

    pygame.display.flip()
    clock.tick(60) 

    # Check for Menu Interaction
    for event in events:
        if current_state == GAME_STATES["MENU"] and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(menu.current_menu.buttons):
                if button.is_clicked(event) and i == 0: 
                    current_state = GAME_STATES["GAME"] 