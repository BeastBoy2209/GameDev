import pygame
import sys

class Button:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Menu:
    def __init__(self):
        self.background_image = pygame.image.load(r"data/menu/main menu.PNG")
        self.buttons = [
            Button(r"data/menu/start_button.png", 1344, 394),
            Button(r"data/menu/options_button.png", 1300, 554),
            Button(r"data/menu/quit_button.png", 1352, 713)
        ]
        self.settings_menu = SettingsMenu(self)
        self.current_menu = self

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(screen)

    def update(self, events):
        for event in events:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    if i == 0:
                        #логика игры
                        pass
                    elif i == 1:
                        self.current_menu = self.settings_menu
                    elif i == 2:
                        pygame.quit()
                        sys.exit()

class SettingsMenu(Menu):
    def __init__(self, main_menu):
        self.background_image = pygame.image.load(r"data/menu/setings menu.PNG")
        self.buttons = [
            Button(r"data/menu/back_button.png", 1352, 713)
        ]
        self.sliders = [
            Slider(1080, 453, 300, 20, 0, 1, 0.5, "Music Volume"),
            Slider(1080, 553, 300, 20, 0, 1, 0.5, "Effects Volume")
        ]
        self.main_menu = main_menu

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        for slider in self.sliders:
            slider.draw(screen)

    def update(self, events):
        for event in events:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event):
                    if i == 0:
                        self.main_menu.current_menu = self.main_menu
            for slider in self.sliders:
                slider.update(event)
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, text):
        self.rect = pygame.Rect(x, y, 698, 23)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.text = text
        self.font = pygame.font.Font(None, 36) 
        self.slider_rect = pygame.Rect(x, y, int(width * (self.value / self.max_value)), height)
        
        self.background_image = pygame.image.load(r"data/menu/slider_background.png")
        self.knob_image = pygame.image.load(r"data/menu/slider_knob.png")
        
        self.knob_rect = self.knob_image.get_rect(center=(self.slider_rect.centerx, self.slider_rect.centery))
        
        self.dragging = False 

    def draw(self, screen):
        screen.blit(self.background_image, self.rect)
        screen.blit(self.knob_image, self.knob_rect)

        text_surface = self.font.render(self.text + f": {int(self.value * 100)}%", True, (255, 255, 255))
        text_rect = text_surface.get_rect(midbottom=(self.rect.centerx, self.rect.top - 10))
        screen.blit(text_surface, text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if self.dragging:
            mouse_x = event.pos[0]
            if mouse_x < self.rect.left:
                mouse_x = self.rect.left
            elif mouse_x > self.rect.right:
                mouse_x = self.rect.right
            relative_x = mouse_x - self.rect.left
            self.slider_rect.width = relative_x
            self.value = (self.slider_rect.width / self.rect.width) * self.max_value
            self.knob_rect.centerx = mouse_x