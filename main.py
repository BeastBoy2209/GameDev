import pygame
import sys

from src.characters import Player
from src.levels import Level
from src.menu import Menu

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Chance")


# Цвета
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


# Создание объектов
# player = Player("data/images/player.png", 100, 100)
# level = Level("data/levels/level1.json")  # Пример загрузки уровня
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu

# Состояния игры
GAME_STATES = {
    "MENU": 0,
    "GAME": 1
}
current_state = GAME_STATES["MENU"]  # Начинаем с меню

# Игровой цикл
clock = pygame.time.Clock()
while True:
    events = pygame.event.get()

    if current_state == GAME_STATES["MENU"]:
        # Обработка событий меню
        menu.current_menu.update(events)  # Обновляем текущее меню 

        # Отрисовка меню
        menu.current_menu.draw(screen)  # Отрисовываем текущее меню

    elif current_state == GAME_STATES["GAME"]:
        # Обработка событий игры
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обновление состояния игры
        player.update()
        level.update()

        # Отрисовка игры
        screen.fill(BLACK)
        level.draw(screen)
        player.draw(screen)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)
pygame.quit()