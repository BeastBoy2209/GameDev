import pygame

class Level:
    def __init__(self):
        self.rooms = []  # Список комнат
        self.current_room_index = 0  # Индекс текущей комнаты
        self.doors = []  # Список дверей

    def switch_room(self, index):
        self.current_room_index = index
        print("Переход в комнату:", self.current_room_index)

    def add_room(self, room):
        self.rooms.append(room)

    @property
    def current_room(self):
        return self.rooms[self.current_room_index]

    def add_door(self, door):
        self.doors.append(door)

    def check_door_collisions(self, player):
        for door in self.doors:
            if player.rect.colliderect(door.rect):
                print("1")
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    self.switch_room(door.target_room_index)

class Door:
    def __init__(self, x, y, width, height, target_room_index):
        self.rect = pygame.Rect(x, y, width, height)
        self.target_room_index = target_room_index

class Room:
    def __init__(self):
        self.background_image = None
        self.doors = []

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        for door in self.doors:
            pygame.draw.rect(screen, (255, 0, 0), door.rect, 2)


class MainHall(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load('data/rooms/mainHall.png').convert()

class Room2(Room):
    def __init__(self):
        super().__init__()
        self.background_image = pygame.image.load('data/rooms/left_stairs.png').convert()