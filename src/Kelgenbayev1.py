import pygame
import sys

def kelgenbayev1_animated_dialog(screen, npcs, font, events, dialog_state):
    dialog_active = dialog_state.get('active', False)
    if not dialog_active:
        return False
    
    text_position = dialog_state['text_position']
    current_npc = dialog_state['current_npc']
    current_phrase_index = dialog_state['current_phrase_index']
    npc_image = None

    if not dialog_active and not current_npc:
        npc = npcs[0]
        dialog_active = True
        dialog_state.update({
            'active': True,
            'current_npc': npc,
            'text_position': 0,
            'current_phrase_index': 0
        })

    if dialog_active and current_npc:
        background_image = pygame.image.load(current_npc['background'])
        screen.blit(background_image, (0, 0))

        dialog_line = current_npc['dialog'][current_phrase_index]
        if dialog_line.startswith("Teacher*"):
            npc_image = pygame.image.load(current_npc['image1'])
        elif dialog_line.startswith("Main character*"):
            npc_image = pygame.image.load(current_npc['image2'])

        npc_image_rect = npc_image.get_rect(center=(screen.get_width() // 2, 500))
        screen.blit(npc_image, npc_image_rect)

        space_pressed = False
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                space_pressed = True

        if space_pressed and text_position >= len(dialog_line):
            current_phrase_index += 1
            if current_phrase_index < len(current_npc['dialog']):
                dialog_state['current_phrase_index'] = current_phrase_index
                text_position = 0
                dialog_state['text_position'] = text_position
            else:
                dialog_active = False
                dialog_state['active'] = False
                dialog_state['current_npc'] = None

        if dialog_active:
            if text_position < len(dialog_line):
                text_position += 1
                dialog_state['text_position'] = text_position

            dialog_box = pygame.Rect(100, screen.get_height() - 150, screen.get_width() - 200, 100)
            pygame.draw.rect(screen, (255, 255, 255), dialog_box)
            displayed_text = dialog_line[:text_position]
            text_surface = font.render(displayed_text, True, (0, 0, 0))
            screen.blit(text_surface, (dialog_box.x + 5, dialog_box.y + 5))

    if current_phrase_index >= len(current_npc['dialog']):
        return False  
    return True  


def main():
    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
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
                   "Teacher* - When you are done with your defence, you come to me and get your bonus points"
                   "Main character* - Thank you so much! I'll be right back",],
        'background': 'data/dialogs/Independencebackground.jpg',
        'image1': 'data/dialogs/Teacherkelgenbayev.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
    font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)
    dialog_state = {'active': False, 'current_npc': npc_list2[0]}
    running = True
    in_dialogue = False

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if not in_dialogue:
                    in_dialogue = True
                    dialog_state['active'] = True
                    dialog_state['current_phrase_index'] = 0
                    dialog_state['text_position'] = 0

        screen.fill((0, 0, 0)) 

        if in_dialogue:
            continue_dialog = kelgenbayev1_animated_dialog(screen, npc_list2, font, events, dialog_state)
            if not continue_dialog:
                in_dialogue = False
                dialog_state['active'] = False 

        pygame.display.flip() 

    pygame.quit()

if __name__ == "__main__":
    main()