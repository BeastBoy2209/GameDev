import pygame
import sys

def animated_dialog_morning(screen, npcs, font, events, dialog_state):
    dialog_active = dialog_state.get('active', False)
    text_position = dialog_state.get('text_position', 0)
    current_npc = dialog_state.get('current_npc', None)
    current_phrase_index = dialog_state.get('current_phrase_index', 0)
    ready_to_advance = dialog_state.get('ready_to_advance', False)

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not dialog_active:
                dialog_active = True
                dialog_state['active'] = True
            ready_to_advance = True

    if dialog_active and current_npc:
        dialog_line = current_npc['dialog'][current_phrase_index]
        if dialog_line in ["Time is 12:14 PM"]:
            background_image = pygame.image.load(current_npc['image5'])
        else:
            background_image = pygame.image.load(current_npc['background'])
        screen.blit(background_image, (0, 0))

        if dialog_line in ["*Yawn*"]:
            npc_image = pygame.image.load(current_npc['image1'])
        elif dialog_line in ["Oh... Why is it so bright outside..?", "Stop..."]:
            npc_image = pygame.image.load(current_npc['image3'])
        elif dialog_line in ["*Realization*", "No, no, no... not again! I can't let this happen!",
                             "WHERE IS MY PHONE?? WHAT TIME IS IT!!?", "*Time on the phone is 11:34 PM*", "OH MY GOD!!",
                             "Now, I can only make it to the second lecture", "It is my 17th absence; I cannot skip anymore!!",
                             "My last chance not to get F!!", "**Leaving "]:
            npc_image = pygame.image.load(current_npc['image2'])
        elif dialog_line in ["..."]:
            npc_image = pygame.image.load(current_npc['image4'])
            background_image = pygame.image.load(current_npc['image4'])
        elif dialog_line in ["Time is 12:14 PM"]:
            background_image = pygame.image.load(current_npc['image5'])
            npc_image = None
        else:
            npc_image = None

        if npc_image:
            npc_image_rect = npc_image.get_rect(center=(screen.get_width() // 3, 500))
            screen.blit(npc_image, npc_image_rect)

        if ready_to_advance and text_position >= len(dialog_line):
            current_phrase_index += 1
            if current_phrase_index < len(current_npc['dialog']):
                dialog_state.update({
                    'current_phrase_index': current_phrase_index,
                    'text_position': 0,
                    'ready_to_advance': False
                })
            else:
                dialog_active = False
                dialog_state.update({
                    'active': False,
                    'current_npc': None,
                    'ready_to_advance': False
                })
                return False 

        if dialog_active:
            if text_position < len(dialog_line):
                text_position += 1
                dialog_state['text_position'] = text_position

            dialog_box = pygame.Rect(100, screen.get_height() - 150, screen.get_width() - 200, 100)
            pygame.draw.rect(screen, (255, 255, 255), dialog_box)
            displayed_text = dialog_line[:text_position]
            text_surface = font.render(displayed_text, True, (0, 0, 0))
            screen.blit(text_surface, (dialog_box.x + 5, dialog_box.y + 5))

    return True 



def main():
    pygame.init()
    screen = pygame.display.set_mode((1900, 1000))
    npc_list1 = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["**Vakes up", "*Opens eyes*", "*Yawn*", "Oh... Why is it so bright outside..?", 
                   "Stop...", "*Realization*", "No, no, no... not again! I can't let this happen!",
                   "WHERE IS MY PHONE?? WHAT TIME IS IT!!?", "*Time on the phone is 11:34.*", "OH MY GOD!!",
                   "Now, I can only make it to the second lecture", "It is my 17th absence; I cannot skip anymore!!",
                   "My last chance not to get F!!", "**Leaving ", "...",  "Time is 12:14 PM"],
        'background': 'data/dialogs/dormbackgroung.jpg',
        'image1': 'data/dialogs/MainCharacter.png', 
        'image2': 'data/dialogs/MCShock.PNG',
        'image3': 'data/dialogs/MCdiscuse.PNG',
        'image4': 'data/dialogs/black.jpg',
        'image5': 'data/dialogs/kbtu.png'
    }]
    font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)
    dialog_state = {'active': False, 'ready_to_advance': False, 'current_npc': npc_list1[0]}
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
            continue_dialogue = animated_dialog_morning(screen, npc_list1, font, events, dialog_state)
            if not continue_dialogue:
                in_dialogue = False 

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


