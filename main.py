import pygame
import sys
from src.characters import Player
from src.levels import Level
from src.menu import Menu

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Chance")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Создание экземпляра уровня
level = Level()
level.add_wall(100, 100, 50, 200)  # Пример стены (x, y, ширина, высота)
level.add_wall(300, 300, 200, 50)  # Пример стены (x, y, ширина, высота)

# Создание экземпляра игрока
player = Player("Kelg.png", 10, )

# Создание экземпляра меню
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu
menu.current_menu = menu

# Состояния игры
GAME_STATES = {
    "MENU": 0,
    "GAME": 1
}
current_state = GAME_STATES["MENU"]

# Игровой цикл
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

        # Обновление позиции игрока и проверка столкновений со стенами
        player.update(events, level.walls)

        screen.fill(BLACK)
        level.draw(screen)
        player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    for event in events:
        if current_state == GAME_STATES["MENU"] and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(menu.current_menu.buttons):
                if button.is_clicked(event) and i == 0:  # Нажата кнопка Play
                    current_state = GAME_STATES["GAME"]  # Переключение в режим игры
