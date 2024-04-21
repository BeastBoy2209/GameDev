import pygame

class Character:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Character):
    def __init__(self, x, y, level):
        super().__init__('data/images/mc.png', x, y)
        self.level = level

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: 
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5

    def check_character_interactions(self, events):  # Add events as a parameter
        for character in self.level.current_room.characters:
            character.check_for_interaction(self, events)  # Pass events to the method

class QuestCharacter(Character):
    def __init__(self, image_path, x, y, dialogue):
        super().__init__(image_path, x, y)
        self.interaction_zone = pygame.Rect(self.rect.x - 50, self.rect.y - 50, 
                                            self.rect.width + 100, self.rect.height + 100)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.interaction_zone, 2)

    def interact(self):
        print(1)

    def check_for_interaction(self, player, events):
        if self.interaction_zone.colliderect(player.rect):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    print("1")
                    self.interact()
                    break