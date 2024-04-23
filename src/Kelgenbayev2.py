import pygame
import sys

def show_win_screen(screen, font):
    win = True
    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to exit the win screen
                    win = False

        screen.fill((0, 100, 0))  # Green background for the win screen
        win_text = "Congratulations! You've passed!"
        text_surface = font.render(win_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

    pygame.quit()

def final_animated_dialog(screen, npcs, font, events, dialog_state):
    dialog_active = dialog_state.get('active', False)
    if not dialog_active:
        return False

    text_position = dialog_state['text_position']
    current_npc = dialog_state['current_npc']
    current_phrase_index = dialog_state['current_phrase_index']

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
            return False  # Ends dialog when phrases are exhausted

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
    npc_list = [{
        'rect': pygame.Rect(150, 100, 50, 50),
        'dialog': ["Main character* - Hello again, I have succesfully defended my labs", 
                   "Teacher* - Nice job!!"],
        'background': 'data/dialogs/Independencebackground.jpg',
        'image1': 'data/dialogs/Teacherkelgenbayev.PNG',
        'image2': 'data/dialogs/MainCharacter.PNG'
    }]
    font = pygame.font.Font("data/dialogs/Grand9K Pixel.ttf", 36)
    dialog_state = {'active': False, 'current_npc': npc_list[0]}
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
            continue_dialog = final_animated_dialog(screen, npc_list, font, events, dialog_state)
            if not continue_dialog:
                in_dialogue = False
                show_win_screen(screen, font)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
