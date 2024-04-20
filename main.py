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
font = pygame.font.Font(None, 36)  # Выберите шрифт и размер

# Стартовый текст
intro_text = ["text1", "texr2", "text3"]  # Список текстов для показа поочередно
text_delay = 2  # Задержка между появлением текстов в секундах
current_text_index = 0  # Индекс текущего текста для отображения
# Создание экземпляра меню
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu

# Состояния игры
GAME_STATES = {
    "MENU": 0,
    "GAME": 1
}
current_state = GAME_STATES["MENU"]  # Начало с состояния меню

# Игровой цикл
clock = pygame.time.Clock()
show_intro = True  # Флаг для отображения стартового текста
while True:
    events = pygame.event.get()

    
    # Обработка событий в зависимости от текущего состояния игры
    if current_state == GAME_STATES["MENU"]:
        menu.current_menu.update(events)  # Обновление текущего меню
        menu.current_menu.draw(screen)  # Отрисовка текущего меню на экране

    elif current_state == GAME_STATES["GAME"]:
        # Обработка игровых событий
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Обновление игровой логики и отрисовка игровых объектов
        screen.fill(BLACK)  # Заливка экрана черным цветом (можно изменить цвет)
        # Ваша игровая логика и код отрисовки здесь...
        # Обновление состояния игры
        # player.update()
        # level.update()

        # Отрисовка игры
        screen.fill(BLACK)
        # level.draw(screen)
        # player.draw(screen)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

    # Проверка, была ли нажата кнопка "Play" в меню
    for event in events:
        if current_state == GAME_STATES["MENU"] and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(menu.current_menu.buttons):
                if button.is_clicked(event) and i == 0:  # Кнопка Play нажата
                    current_state = GAME_STATES["GAME"]  # Изменение состояния игры на GAME
                    show_intro = True  # Включаем отображение стартового текста
