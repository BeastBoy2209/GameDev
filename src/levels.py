import pygame
import sys
from src.characters import Wall

class Level:
    def __init__(self):
        self.walls = pygame.sprite.Group()  # Группа спрайтов для стен

        # Создание стен и добавление их в группу
        wall1 = Wall(100, 100, 50, 200)
        wall2 = Wall(300, 300, 200, 50)
        self.walls.add(wall1, wall2)

    def draw(self, screen):
        self.walls.draw(screen)  # Отрисовка всех стен на экране
