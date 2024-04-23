import pygame
import sys

def usu2_animated_dialog(screen, npcs, font, events, dialog_state):
    dialog_active = dialog_state.get('active', False)
    if not dialog_active:
        return False
    
    text_position = dialog_state['text_position']
    current_npc = dialog_state['current_npc']
    current_phrase_index = dialog_state['current_phrase_index']

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
        if dialog_line.startswith("Practice teacher*"):
            npc_image = pygame.image.load(current_npc['image1'])
        elif dialog_line.startswith("Main character*"):
            npc_image = pygame.image.load(current_npc['image2'])

        npc_image_rect = npc_image.get_rect(center=(screen.get_width() // 4, 500))
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
    npc_list4 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Main character* - Here is the coffee!",
                   "Practice teacher* - Thanks! Now let's start our defence",],
        'background': 'data/dialogs/usubackground.jpg',
        'image1': 'data/dialogs/Usu.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
    font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)
    dialog_state4 = {'active': False, 'current_npc': npc_list4[0]}
    running = True
    in_dialogue4 = False

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if not in_dialogue4:
                    in_dialogue4 = True
                    dialog_state4['active'] = True
                    dialog_state4['current_phrase_index'] = 0
                    dialog_state4['text_position'] = 0

        screen.fill((0, 0, 0))
        if in_dialogue4:
            continue_dialog4 = usu2_animated_dialog(screen, npc_list4, font, events, dialog_state4)
            if not continue_dialog4:
                in_dialogue4 = False
                dialog_state4['active'] = False 

        pygame.display.flip() 

    pygame.quit()
    
if __name__ == "__main__":
    main()