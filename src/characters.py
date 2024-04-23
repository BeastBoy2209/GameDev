import pygame, sys, random
from pygame.locals import *
from .constants import GameConstants
from .safe_game import main, terminate, checkForQuit, getStartingBoard, getBlankPosition, makeMove, isValidMove, getRandomMove, getLeftTopOfTile, getSpotClicked, drawTile, makeText, drawBoard, slideAnimation, generateNewPuzzle, resetAnimation  

BLACK =         (  50,   50,   50)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
GRAY =          (  122,  122,  122)
BLUE =          (  112,  50, 255)
PURPLE =         (  186, 85, 211)
RED =           (255, 0, 0)
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

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
    def __init__(self, x, y, level, shared_data):
        super().__init__('data/images/mc.png', x, y)
        self.level = level
        self.shared_data = shared_data

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

    def check_character_interactions(self, events, game_constants=None):  # Accept optional game_constants
        for character in self.level.current_room.characters:
            if isinstance(character, Safe):  # Prioritize Safe interaction
                character.check_for_interaction(self, events)
            elif isinstance(character, QuestCharacter):
                character.check_for_interaction(self, events)
            elif isinstance(character, kelCharacter):
                if character.check_for_interaction(self, events, 1):  # Check if interaction occurred
                    self.shared_data.talkk += 1
                    if self.shared_data.dialogue == 0:  
                        self.shared_data.dialogue = 1 

            elif isinstance(character, usuCharacter):
                if character.check_for_interaction(self, events, 2): 
                    self.shared_data.talku += 1
                    if self.shared_data.dialogue == 1:  
                        self.shared_data.dialogue = 2  

    def check_enemy_collisions(self):
        for character in self.level.current_room.characters:
            if isinstance(character, Enemy):
                character.check_collision(self)

class kelCharacter(Character):
    def __init__(self, image_path, x, y, index, shared_data):
        super().__init__(image_path, x, y)  # Pass only the required arguments to the parent class
        self.interaction_zone = pygame.Rect(self.rect.x - 50, self.rect.y - 50, 
                                               self.rect.width + 100, self.rect.height + 100)
        self.index = index
        self.shared_data = shared_data

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def interact(self):
        print("1")

    def check_for_interaction(self, player, events, index):
        if self.interaction_zone.colliderect(player.rect):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and index == 1:
                    self.shared_data.talkk += 1 
                    print("uwu")
                    return True

class usuCharacter(Character):
    def __init__(self, image_path, x, y, index, shared_data):
        super().__init__(image_path, x, y)  # Pass only the required arguments to the parent class
        self.interaction_zone = pygame.Rect(self.rect.x - 50, self.rect.y - 50, 
                                               self.rect.width + 100, self.rect.height + 100)
        self.index = index
        self.shared_data = shared_data

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def interact(self):
        print(1)

    def check_for_interaction(self, player, events, index):
        if self.interaction_zone.colliderect(player.rect):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e and index == 2:
                    self.shared_data.talku += 1 
                    print("2")
                    break


    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
    def __init__(self, x, y, game_constants):
        self.images = {
            "closed": pygame.image.load(r"data\images\safe_clossed.png"),
            "open": pygame.image.load(r"data\images\safe_opened.png"),
            "empty": pygame.image.load(r"data\images\safe_empty.png")
        }
        self.state = "closed"
        self.game_constants = game_constants
        self.image = self.images[self.state]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_zone = pygame.Rect(self.rect.x - 50, self.rect.y - 50, 
                                            self.rect.width + 100, self.rect.height + 100)
        

    def check_for_interaction(self, player, events):
        if self.interaction_zone.colliderect(player.rect):
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    print("Interacting with Safe")
                    if self.state == "closed":
                        player_won = self.run_safe_minigame(player.level.current_room.screen) 
                        if player_won:
                            print("Player won the minigame!")
                            self.state = "open"
                            self.image = self.images[self.state]
                    # Удалено лишнее условие
                    elif self.state == "open":  # Изменено на elif
                        print("now empty")
                        self.state = "empty"
                        self.image = self.images[self.state]
                        break

    def run_safe_minigame(self, screen):
        mainBoard, solutionSeq = generateNewPuzzle(80, screen, self.game_constants)
        SOLVEDBOARD = getStartingBoard()
        allMoves = []
        TEXT = PURPLE
        BGCOLOR = GRAY
        SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXT, BGCOLOR, 
                                            1900 - 120, 1000 - 250)

        while True:
            slideTo = None
            msg = 'Click tile or press arrow keys to slide.'
            if mainBoard == SOLVEDBOARD:
                return True  # Player won!

            drawBoard(mainBoard, msg, screen, self.game_constants)
            checkForQuit()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == MOUSEBUTTONUP:
                    spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                    if (spotx, spoty) == (None, None):
                        if SOLVE_RECT.collidepoint(event.pos):
                            resetAnimation(mainBoard, solutionSeq + allMoves, screen, self.game_constants)  # Передаем screen и self.game_constants
                            allMoves = []
                    else:
                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = GameConstants.LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = GameConstants.RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = GameConstants.UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = GameConstants.DOWN

                elif event.type == KEYUP:
                    if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                        slideTo = UP
                    elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                        slideTo = DOWN

            if slideTo:
                slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8, screen, self.game_constants)  # Передаем screen и self.game_constants
                makeMove(mainBoard, slideTo)
                allMoves.append(slideTo) 
            pygame.display.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (0, 255, 0), self.interaction_zone, 2)

