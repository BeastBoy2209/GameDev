import pygame, sys, random
from pygame.locals import *
class Character:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy(Character):
    def __init__(self, image_paths, x, y):  # Pass a list of image paths
        self.images = [pygame.image.load(path) for path in image_paths]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_timer = 0

    def update(self):
        self.animation_timer += 1
        if self.animation_timer >= 10:  
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
            print("Game Over!")  

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

    def check_character_interactions(self, events):  
        for character in self.level.current_room.characters:
            if isinstance(character, QuestCharacter):  # Check if it's a QuestCharacter
                character.check_for_interaction(self, events)
            if isinstance(character, Safe):  # Check if it's a SAfe
                character.check_for_interaction(self, events)
        
    def check_enemy_collisions(self):
        for character in self.level.current_room.characters:
            if isinstance(character, Enemy):  # Check if it's an Enemy
                character.check_collision(self)

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

class Safe(Character):
    def __init__(self, x, y):
        self.images = {
            "closed": pygame.image.load(r"data\images\safe_clossed.png"),
            "open": pygame.image.load(r"data\images\safe_clossed.png"),
            "empty": pygame.image.load(r"data\images\safe_clossed.png")
        }
        self.state = "closed" 
        self.image = self.images[self.state]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_zone = pygame.Rect(self.rect.x - 50, self.rect.y - 50, 
                                            self.rect.width + 100, self.rect.height + 100)

    def check_for_interaction(self, player, events):
        if self.interaction_zone.colliderect(player.rect):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    print("1")
                    if self.state == "closed":
                        player_won = run_safe_minigame()
                        if player_won:  # Replace with the appropriate condition to check for a win
                            self.state = "open"
                            self.image = self.images[self.state]
                    elif self.state == "open":
                        self.state = "empty"
                        self.image = self.images[self.state]
                    break

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (0, 255, 0), self.interaction_zone, 2)

