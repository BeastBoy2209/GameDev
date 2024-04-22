import pygame
import sys
from src.safe_game import game_constants
from src.characters import Player, Character, QuestCharacter, Enemy, Safe
import textwrap
from src.characters import Player, Character, QuestCharacter, Enemy
from src.levels import Level, Wall, MainHall, LeftStairs, RightStairs, LeftCorridor, RightCorridor, IndependenceHall, Door
from src.menu import Menu
from src.Usu import usu_animated_dialog
from src.Usu2 import usu2_animated_dialog
from src.Kelgenbayev1 import kelgenbayev1_animated_dialog
from src.Kelgenbayev2 import final_animated_dialog, show_win_screen
from src.morning import animated_dialog_morning


pygame.init()

WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Chance")


player_speed = 5

#npc dialogs
npc_list3 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Main character* - Hello, teacher!",
                   "Practice teacher* - Hello, are you my student??", 
                   "Main character* - Yes i am, i have missed a lot",
                   "Practice teacher* - I can see", 
                   "Practice teacher* - So what brought you here?", 
                   "Main character* - I really need to get the bonus points",
                   "Main character* - My teacher said that I can defend my completed labs to get them", 
                   "Main character* - But the teacher is busy right now", 
                   "Main character* - He said I can defend them with you", 
                   "Practice teacher* - Ohh, let's take a look",
                   "Practice teacher* - Okay, while I am openning the file, can you please bring me a coffee",
                   "Main character* - Ohh, Okay"],
        'background': 'data/dialogs/usubackground.jpg',
        'image1': 'data/dialogs/Usu.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
npc_list4 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Main character* - Here is the coffee!",
                   "Practice teacher* - Thanks! Now let's start our defence",],
        'background': 'data/dialogs/usubackground.jpg',
        'image1': 'data/dialogs/Usu.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
npc_list1 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["HEllo"],
        'background': 'data/dialogs/dormbackgroung.jpg',
        'image1': 'data/dialogs/MainCharacter.png', 
        'image2': 'data/dialogs/MCShock.PNG',
        'image3': 'data/dialogs/MCdiscuse.PNG',
        'image4': 'data/dialogs/black.jpg',
        'image5': 'data/dialogs/kbtu.png'
    }]
npc_list2 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Teacher* - Oooh, hello my dear friend, so glad you have come", 
                   "Main character* - Hello, sorry for being late..", 
                   "Main character* - Can i sign the attendance please...",
                   "Teacher* - Of course you can!", 
                   "Main character* - *Exhale of relief", 
                   "Main character* - *Sighns", 
                   "Main character* - Thank you, my mark is saved",
                   "Teacher* - ohh, I wouldn't be so sure about that",
                   "Main character* - Why?....",
                   "Teacher* - You have missed a lot of classes, including our defence weeks",
                   "Teacher* - Your points are not enough to close your semester",
                   "Main character* - Is there any chance.. I can somehow raise my mark?",
                   "Teacher* - Hmm, that's the great question",
                   "Teacher* - You should have thought about it earlier",
                   "Teacher* - Anyway..",
                   "Teacher* - Ok, there is only one way..",
                   "Teacher* - I see you have done some of the Labs",
                   "Teacher* - You have to defend them all, but now I have a lecture to conduct",
                   "Teacher* - Try to reach your practice teacher and defend the Lab works with him",
                   "Teacher* - When you are done with your defence, you come to me and get your bonus points",
                   "Main character* - Thank you so much! I'll be right back",],
        'background': 'data/dialogs/Independencebackground.jpg',
        'image1': 'data/dialogs/Teacherkelgenbayev.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
npc_list = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Main character* - Hello again, I have succesfully defended my labs", 
                   "Teacher* - Nice job!!"],
        'background': 'data/dialogs/Independencebackground.jpg',
        'image1': 'data/dialogs/Teacherkelgenbayev.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
dialog_state = {
    'active': False,
    'current_npc': None,
    'text_position': 0, 
    'current_phrase_index': 0,  
    'ready_to_advance': False  
}
dialogue = 0
font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)


# Создание прямоугольников для стен
wall_rect1 = pygame.Rect(351, 9, 208, 58)
wall_rect2 = pygame.Rect(789, 9, 208, 58)
wall_rect3 = pygame.Rect(942, 10, 58, 208)
wall_rect4 = pygame.Rect(1509, 256, 58, 208)

# Создание объектов стен с передачей прямоугольников
wall1 = Wall(wall_rect1)
wall2 = Wall(wall_rect2)
wall3= Wall(wall_rect3)
wall4= Wall(wall_rect4)

# Установка прозрачности стен
wall_alpha = 100  # Прозрачность первой стены (значение альфа)
wall1.image.set_alpha(wall_alpha)
wall2.image.set_alpha(wall_alpha)
wall3.image.set_alpha(wall_alpha)
wall4.image.set_alpha(wall_alpha)

# Create Level and Rooms
level = Level()
main_hall = MainHall(screen)
left_stairs = LeftStairs(screen)
right_stairs = RightStairs(screen)
left_corridor = LeftCorridor(screen)
right_corridor = RightCorridor(screen)
independence_hall = IndependenceHall(screen )

# Add Walls to Level
level.add_wall(wall1)
level.add_wall(wall2)

# Add Rooms to Level (with indices)
level.add_room(main_hall, 0)       
level.add_room(left_stairs, 1)    
level.add_room(right_stairs, 2)   
level.add_room(left_corridor, 3)  
level.add_room(right_corridor, 4) 
level.add_room(independence_hall, 5)  

# --- Doors for Main Hall ---
door1 = Door(559, 45, 229, 23, 1, 1)  # To Left Stairs 
main_hall.doors.append(door1)


door2 = Door(578, 919, 211, 22, 2, 2)  # To Right Stairs 
main_hall.doors.append(door2)


door3 = Door(1357, 370, 19, 190, 5, 3)  # To Independence Hall 
main_hall.doors.append(door3)


# --- Doors for Left Stairs --- 
door4 = Door(665, 818, 168, 21, 0, 4)  # To Main Hall  
left_stairs.doors.append(door4)


door5 = Door(1380, 190, 14, 363, 3, 5)  # To Left Corridor 
left_stairs.doors.append(door5)


# --- Doors for Right Stairs --- 
door6 = Door(657, 185, 169, 13, 0, 6)  # To Main Hall 
right_stairs.doors.append(door6)


door7 = Door(1369, 466, 18, 363, 4, 7)  # To Right Corridor 
right_stairs.doors.append(door7)


# --- Doors for Left Corridor --- 
door8 = Door(0, 341, 14, 275, 1, 8)  # To Left Stairs 
left_corridor.doors.append(door8)


# --- Doors for Right Corridor --- 
door9 = Door(0, 342, 14, 276, 2, 9)  # To Right Stairs
right_corridor.doors.append(door9)


# --- Doors for Independence Hall --- 
door10 = Door(160, 366, 20, 250, 0, 10)  # To Main Hall 
independence_hall.doors.append(door10) 


# Create Player
player = Player(10, 10, level) 
player.rect.x = 442 
player.rect.y = 449

# Create Enemy Characters (provide a list of image paths)
cleaner1 = Enemy(["data/images/cleaner1.PNG", "data/images/cleaner2.PNG", "data/images/cleaner3.PNG"], 455, 439)
cleaner2 = Enemy(["data/images/cleaner1.PNG", "data/images/cleaner2.PNG", "data/images/cleaner3.PNG"], 1481, 220)
right_corridor.characters.append(cleaner1)
right_corridor.characters.append(cleaner2)

# Create Quest Characters
independence_hall_character = QuestCharacter(r"data\images\Kelg.PNG", 929, 455, "Welcome to Independence Hall!")
left_corridor_character = QuestCharacter(r"data\images\Usu.PNG", 1287, 126, "Psst, hey kid... I've got a job for you.")

# Create Safe object
safe = Safe(1700, 400, game_constants)
right_corridor.characters.append(safe)

# Add them to the respective rooms
independence_hall.characters.append(independence_hall_character)
left_corridor.characters.append(left_corridor_character)

# Load music files
menu_music = pygame.mixer.music.load("data/sounds/start_menu.mp3")
menu_music_playing = False
game_music_playing = False

# Menu Setup
menu = Menu()
menu.main_menu = menu
menu.settings_menu.main_menu = menu
menu.current_menu = menu

GAME_STATES = {
    "MENU": 0,
    "GAME": 1,
    "DIALOG_MORNING": 2,  
    "DIALOG_USU1": 3,   
    "DIALOG_USU2": 4,    
    "DIALOG_KELGENBAYEV1": 5, 
    "DIALOG_FINAL": 6,
    "QUIZ": 7,
    "SAFE_MINIGAME": 8
}
current_state = GAME_STATES["MENU"]

# quiz completion
def run_quiz(screen, font):
    # Colors and settings
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    width, height = 1900, 1000
    # Define questions and answers
    questions = [
        {"question": "What will be the output of the code: numbers = [1, 2, 3, 4, 5]; numbers.append(6); print(numbers)?",
         "choices": ["A) [1, 2, 3, 4, 5]", "B) [1, 2, 3, 4, 5, 6]", "C) [6, 1, 2, 3, 4, 5]", "D) None"],
         "correct": "B"},
        {"question": "Which data structure automatically removes duplicates in Python?",
         "choices": ["A) List", "B) Tuple", "C) Set", "D) Dictionary"],
         "correct": "C"},
        {"question": "What is the correct way to access the value 'apple' from the dictionary: fruits = {'name': 'apple', 'color': 'red'}?",
         "choices": ["A) fruits[1]", "B) fruits['name']", "C) fruits(name)", "D) fruits.color"],
         "correct": "B"},
        {"question": "What does the pop() method do when used with a list?",
         "choices": ["A) Deletes the last item of the list", "B) Adds an item to the end of the list", "C) Returns the first item of the list", "D) Randomly selects an item to delete"],
         "correct": "A"},
        {"question": "How would you add the element 'orange' to the set fruits = {'apple', 'banana', 'cherry'}?",
         "choices": ["A) fruits.add('orange')", "B) fruits.append('orange')", "C) fruits.insert(0, 'orange')", "D) fruits['orange']"],
         "correct": "A"}
    ]

    current_question = 0
    selected_answer = None
    score = 0
    global congrats
    congrats = True

    while congrats:
        screen.fill(WHITE)
        congrats = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                congrats = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in (pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d):
                    selected_answer = ord(event.unicode.upper()) - ord('A')
                    if questions[current_question]["choices"][selected_answer] == questions[current_question]["choices"][ord(questions[current_question]["correct"]) - ord('A')]:
                        score += 1
                    current_question += 1
                    if current_question == len(questions):
                        if score < 4:
                            game_over(screen, font, score, RED, width, height)
                        else:
                            congratulations(screen, font, score, RED, width, height)

        if current_question < len(questions):
            render_question(screen, font, questions[current_question]["question"], questions[current_question]["choices"], selected_answer, BLACK, WHITE)
        
        pygame.display.flip()

def render_question(screen, font, question, choices, selected, text_color, background_color):
    lines = textwrap.wrap(question, width=100)  # Adjust the width as needed
    y = 50
    for line in lines:
        question_surface = font.render(line, True, text_color)
        screen.blit(question_surface, (50, y))
        y += font.get_height()

    y += 20  # Add some spacing before choices
    for index, choice in enumerate(choices):
        choice_surface = font.render(choice, True, text_color)
        screen.blit(choice_surface, (50, y))
        y += 50

def game_over(screen, font, score, text_color, width, height):
    WHITE = (0, 0, 0)
    screen.fill(WHITE)
    message = f"Game over! Your score: {score}! You have failed"
    message_surface = font.render(message, True, text_color)
    screen.blit(message_surface, (width // 2 - message_surface.get_width() // 2, height // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  
    pygame.quit()
    sys.exit()

def congratulations(screen, font, score, text_color, width, height):
    WHITE = (0, 0, 0)
    screen.fill(WHITE)
    message = f"Congratulations! Your score: {score}! You passed the quiz!"
    message_surface = font.render(message, True, text_color)
    screen.blit(message_surface, (width // 2 - message_surface.get_width() // 2, height // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  #
    global current_state, congrats
    current_state = GAME_STATES["GAME"]
    congrats = False

# Dialog state variables 
dialog_state_morning = {'active': False, 'ready_to_advance': False, 'current_npc': npc_list1[0]}
dialog_state_usu1 = {'active': False, 'current_npc': npc_list3[0]}
dialog_state_usu2 = {'active': False, 'current_npc': npc_list4[0]} 
dialog_state_kelgenbayev1 = {'active': False, 'current_npc': npc_list2[0]}
dialog_state_final = {'active': False, 'current_npc': npc_list[0]}  


# Game Loop
clock = pygame.time.Clock()
while True:
    events = pygame.event.get()

    if current_state == GAME_STATES["MENU"]:
        if not menu_music_playing:
            menu_music_playing = True
            pygame.mixer.music.play(-1)
        menu.current_menu.update(events)
        menu.current_menu.draw(screen)
        music_volume_slider = menu.settings_menu.sliders[0]  
        pygame.mixer.music.set_volume(music_volume_slider.value)

    elif current_state == GAME_STATES["GAME"]:
        if not game_music_playing and menu_music_playing == True:
            pygame.mixer.music.unload
            game_music = pygame.mixer.music.load("data/sounds/bg_music.mp3")
            pygame.mixer.music.play(-1)
            game_music_playing = True
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for character in level.current_room.characters:
            if isinstance(character, Enemy):
                character.update()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2 and dialogue == 1:
                    current_state = GAME_STATES["DIALOG_USU1"]
                    dialog_state_usu1['active'] = True
                    dialog_state_usu1['current_phrase_index'] = 0
                    dialog_state_usu1['text_position'] = 0
                    dialogue = 2
                elif event.key == pygame.K_3:
                    current_state = GAME_STATES["DIALOG_USU2"]
                    dialog_state_usu2['active'] = True 
                    dialog_state_usu2['current_phrase_index'] = 0
                    dialog_state_usu2['text_position'] = 0
                    dialogue = 3
                elif event.key == pygame.K_4 and dialogue == 0:
                    current_state = GAME_STATES["DIALOG_KELGENBAYEV1"]
                    dialog_state_kelgenbayev1['active'] = True 
                    dialog_state_kelgenbayev1['current_phrase_index'] = 0
                    dialog_state_kelgenbayev1['text_position'] = 0
                    dialogue = 1 
                elif event.key == pygame.K_5 and dialogue == 3:
                    current_state = GAME_STATES["DIALOG_FINAL"]
                    dialog_state_final['active'] = True 
                    dialog_state_final['current_phrase_index'] = 0
                    dialog_state_final['text_position'] = 0
                    dialogue = 4



        player.update()
        level.check_door_collisions(player)
        player.check_character_interactions(events, game_constants)  # Check for Safe interaction
        player.check_enemy_collisions()

        screen.fill((0, 0, 0))  
        level.current_room.draw()
        for wall in level.walls:
            screen.blit(wall.image, wall.rect)
        player.draw(screen)
        pygame.display.flip()

    elif current_state == GAME_STATES["DIALOG_MORNING"]:
        in_dialogue = animated_dialog_morning(screen, npc_list1, font, events, dialog_state_morning)
        if not in_dialogue:
            current_state = GAME_STATES["GAME"] 
            dialog_state_morning['active'] = False
    elif current_state == GAME_STATES["DIALOG_USU1"]: 
        in_dialogue3 = usu_animated_dialog(screen, npc_list3, font, events, dialog_state_usu1)
        if not in_dialogue3:
            current_state = GAME_STATES["GAME"]
            dialog_state_usu1['active'] = False 
    elif current_state == GAME_STATES["DIALOG_USU2"]:
        in_dialogue4 = usu2_animated_dialog(screen, npc_list4, font, events, dialog_state_usu2)
        if not in_dialogue4:
            current_state = GAME_STATES["QUIZ"] 
            dialog_state_usu2['active'] = False
    elif current_state == GAME_STATES["DIALOG_KELGENBAYEV1"]:
        in_dialogue = kelgenbayev1_animated_dialog(screen, npc_list2, font, events, dialog_state_kelgenbayev1)
        if not in_dialogue:
            current_state = GAME_STATES["GAME"]
            dialog_state_kelgenbayev1['active'] = False 
    elif current_state == GAME_STATES["DIALOG_FINAL"]:
        continue_dialog = final_animated_dialog(screen, npc_list, font, events, dialog_state_final)
        if not continue_dialog:
            current_state = GAME_STATES["GAME"]
            dialog_state_final['active'] = False
            show_win_screen(screen, font)
    elif current_state == GAME_STATES["QUIZ"]:
        run_quiz(screen, font)
        if congrats == False:
            current_state = GAME_STATES["GAME"]
    elif current_state == GAME_STATES["SAFE_MINIGAME"]: 
        current_state = GAME_STATES["GAME"] # Return to main game

    pygame.display.flip()
    clock.tick(60) 
    # Check for Menu Interaction
    for event in events:
        if current_state == GAME_STATES["MENU"] and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(menu.current_menu.buttons):
                if button.is_clicked(event) and i == 0: 
                    current_state = GAME_STATES["DIALOG_MORNING"]
                    dialog_state_morning['active'] = True 
