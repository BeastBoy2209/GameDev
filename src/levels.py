import pygame

class Level:
    def __init__(self):
        self.rooms = [] 
        self.current_room_index = 0 

    def switch_room(self, index, player, door_used):  # Renamed argument to door_used
        self.current_room_index = index
        print("Переход в комнату:", self.current_room_index)
        # Use a dictionary to map (room_index, door_index) to spawn positions
        spawn_points = {
            (0, 4): (624, 76),  # Main Hall from Left Stairs
            (0, 6): (652, 756),      # Main Hall from Right Stairs
            (0, 10): (1260, 388),      # Main Hall from Independence Hall
            (1, 1): (690, 659),      # Left Stairs from Left Corridor
            (1, 8): (1280, 290),      # Left Stairs from Main Hall
            (2, 2): (693, 208),      # Right Stairs from Right Corridor
            (2, 9): (1262, 560),      # Right Stairs from Main Hall
            (3, 5): (30, 400),   # Left Corridor 
            (4, 7): (30, 400),   # Right Corridor 
            (5, 3): (197, 419)  # Independence Hall 
        }

        spawn_point = spawn_points.get((index, door_used.door_index))  # Use door_used
        if spawn_point:
            player.rect.x, player.rect.y = spawn_point
            print("Spawn point not defined for room", index, "and door", door_used.door_index)
        else:
            print("Spawn point not defined for room", index, "and door", door_used.door_index)

    def add_room(self, room, index):  
        self.rooms.append((index, room))  

    @property
    def current_room(self):
        for i, room in self.rooms:
            if i == self.current_room_index:
                return room  
        return None 

    def add_door(self, door):
        pass

    def check_door_collisions(self, player):
        for door in self.current_room.doors:
            if player.rect.colliderect(door.rect):
                self.switch_room(door.target_room_index, player, door)

class Door:
    def __init__(self, x, y, width, height, target_room_index, door_index): 
        self.rect = pygame.Rect(x, y, width, height)
        self.target_room_index = target_room_index
        self.door_index = door_index  

class Room:
    def __init__(self):
        self.background_image = None
        self.doors = []  # Список дверей для этой комнат

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))

        # Draw red rectangles for doors
        for door in self.doors:
            pygame.draw.rect(screen, (255, 0, 0), door.rect, 2)  # Red color, 2 pixels thick


class MainHall(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\mainHall.png').convert()  
class LeftStairs(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\left_stairs.png').convert()  
class RightStairs(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\right_stairs.png').convert()  
class LeftCorridor(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\left_corridor.png').convert()  
class RightCorridor(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\right_corridor.png').convert()  
class IndependenceHall(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load(r'data\rooms\independence.png').convert() 
