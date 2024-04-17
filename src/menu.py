import pygame
import sys 

class Button:
    def __init__(self, text, x, y, width, height, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.Font(None, 32)  # Пикните шрифт нормальный

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Menu:
    def __init__(self):
        self.background_image = pygame.image.load(r"C:\Users\timur\Desktop\GitHUB\GameDev\data\menu.PNG")  # Путь к игре(меняйте на свой)
        self.buttons = [
            Button("START", 350, 250, 100, 50, (150, 150, 150), (255, 255, 255)),
            Button("OPTIONS", 350, 320, 100, 50, (150, 150, 150), (255, 255, 255)),
            Button("QUIT", 350, 390, 100, 50, (150, 150, 150), (255, 255, 255))
        ]
        self.settings_menu = SettingsMenu() 
        self.current_menu = self  

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(screen)

    def update(self, events):
        for event in events:
            for button in self.buttons:
                if button.is_clicked(event):
                    if button.text == "START":
                        # Запустить игру
                        pass  # Здесь будет код запуска игры
                    elif button.text == "OPTIONS":
                        self.current_menu = self.settings_menu
                    elif button.text == "QUIT":
                        pygame.quit()
                        sys.exit()

class SettingsMenu(Menu): 
    def __init__(self):
        self.background_image = pygame.image.load(r"C:\Users\timur\Desktop\GitHUB\GameDev\data\Setings Menu.PNG")
        self.buttons = [
            Button("BACK", 350, 500, 100, 50, (150, 150, 150), (255, 255, 255))
        ]
        self.sliders = [
            Slider(200, 200, 300, 20, 0, 1, 0.5, "Music Volume"),
            Slider(200, 250, 300, 20, 0, 1, 0.5, "Effects Volume")
        ]

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        for slider in self.sliders:
            slider.draw(screen)

    def update(self, events):
        for event in events:
            for button in self.buttons:
                if button.is_clicked(event):
                    if button.text == "BACK":
                        self.current_menu = self.main_menu  # Возвращаемся в главное меню
            for slider in self.sliders:
                slider.update(event)

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.slider_rect = pygame.Rect(x, y, int(width * (self.value / self.max_value)), height)

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)
        text_surface = self.font.render(self.text + f": {int(self.value * 100)}%", True, (255, 255, 255))
        text_rect = text_surface.get_rect(midleft=(self.rect.x - 100, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.slider_rect.x = event.pos[0] - self.rect.x
                self.value = (self.slider_rect.width / self.rect.width) * self.max_value