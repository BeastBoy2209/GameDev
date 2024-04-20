import pygame


class Character:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# стены и преграды
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))  # Черный цвет стены
        self.rect = self.image.get_rect(topleft=(x, y))

class QuestGiver(Character):
    def __init__(self, image_path, x, y, quest_id):
        super().__init__(image_path, x, y)
        self.quest_id = quest_id  # ID квеста, который дает персонаж

    def interact(self, player):
        # Логика взаимодействия с игроком (выдача квеста)
        pass  # Здесь будет код выдачи квеста игроку


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Просто квадрат для представления игрока
        self.image.fill((0, 0, 255))  # Синий цвет игрока
        self.rect = self.image.get_rect(topleft=(x, y))
        self.level = level  # Ссылка на уровень, чтобы проверять столкновения со стенами

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Проверка столкновений со стенами
        wall_collisions = pygame.sprite.spritecollide(self, self.level.walls, False)
        for wall in wall_collisions:
            if keys[pygame.K_LEFT]:
                self.rect.x += 5  # Отменяем движение влево
            if keys[pygame.K_RIGHT]:
                self.rect.x -= 5  # Отменяем движение вправо
            if keys[pygame.K_UP]:
                self.rect.y += 5  # Отменяем движение вверх
            if keys[pygame.K_DOWN]:
                self.rect.y -= 5  # Отменяем движение вниз


    def draw(self, screen):
        # Отрисовка персонажа с учетом направления движения
        if self.direction == "left":
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)