import pygame
import sys 
from morning import animated_dialog_morning 
from Kelgenbayev1 import kelgenbayev1_animated_dialog

def main():
    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    npc_list1 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["**Vakes up", "*Opens eyes*", "*Yawn*", "Oh... Why is it so bright outside..?", 
                   "Stop...", "*Realization*", "No, no, no... not again! I can't let this happen!",
                   "WHERE IS MY PHONE?? WHAT TIME IS IT!!?", "*Time on the phone is 11:34.*", "OH MY GOD!!",
                   "Now, I can only make it to the second lecture", "It is my 17th absence; I cannot skip anymore!!",
                   "My last chance not to get F!!", "**Leaving "],
        'background': 'data/dialogs/dormbackgroung.jpg',
        'image1': 'data/dialogs/MainCharacter.png', 
        'image2': 'data/dialogs/MCShock.PNG',
        'image3': 'data/dialogs/MCdiscuse.PNG'
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
                   "Teacher* - There is only one way..",
                   "Teacher* - You have to collect three stamps from all of our teachers",
                   "Teacher* - But they won't give it for nothing, they will test your skills",
                   "Teacher* - You will see, if you really want to get a good mark"],
        'background': 'data/dialogs/Independencebackground.jpg',
        'image1': 'data/dialogs/Teacherkelgenbayev.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
    font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)
    dialog_state1 = {'active': False, 'ready_to_advance': False, 'current_npc': npc_list1[0]}
    dialog_state2 = {'active': False, 'current_npc': npc_list2[0]}
    running = True
    in_dialogue1 = False
    in_dialogue2 = False

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if not in_dialogue1:
                    in_dialogue1 = True
                    dialog_state1['active'] = True
                    dialog_state1['current_phrase_index'] = 0  # Start at the first phrase
                    dialog_state1['text_position'] = 0  # Start text position at zero

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if not in_dialogue2:
                    in_dialogue2 = True
                    dialog_state2['active'] = True
                    dialog_state2['current_phrase_index'] = 0  # Start at the first phrase
                    dialog_state2['text_position'] = 0  # Start text position at zero

        screen.fill((0, 0, 0))  # Clear screen with black

        if in_dialogue1:
            continue_dialogue1 = animated_dialog_morning(screen, npc_list1, font, events, dialog_state1)
            if not continue_dialogue1:
                in_dialogue1 = False  # Handle the end of the dialogue within the main loop

        if in_dialogue2:
            continue_dialogue2 = kelgenbayev1_animated_dialog(screen, npc_list2, font, events, dialog_state2)
            if not continue_dialogue2:
                in_dialogue2 = False  # Handle the end of the dialogue within the main loop

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()