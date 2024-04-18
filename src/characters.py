import pygame


class Character:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class QuestGiver(Character):
    def __init__(self, image_path, x, y, quest_id):
        super().__init__(image_path, x, y)
        self.quest_id = quest_id  # ID квеста, который дает персонаж

    def interact(self, player):
        # Логика взаимодействия с игроком (выдача квеста)
        pass  # Здесь будет код выдачи квеста игроку


class Player(Character):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.speed = 5  # Скорость передвижения
        self.direction = "right"  # Направление движения

    def update(self):
        # Обработка ввода пользователя и обновление позиции
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
        
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed  # Движение вверх
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed  # Движение вниз

    # Остальной код класса


    def draw(self, screen):
        # Отрисовка персонажа с учетом направления движения
        if self.direction == "left":
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)