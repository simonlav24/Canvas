

import pygame
from pygame import Vector2

from gui import GuiContext, Label, Button



def handle_gui_event(self, event):
    print(event)


def main():
    pygame.init()

    gui_context = GuiContext()
    gui_context.set_layout([
        [Label('This is a gui app')],
        [Button('button1'), Button('button2'), Button('button3'), Button('button4')],
    ])
    
    win = pygame.display.set_mode(gui_context.size)
    pygame.display.set_caption("Gui")
    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            # handle events
            gui_context.handle_event(event)

            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        
        for event in gui_context.get_gui_events():
            print(f'GUI Event: {event.type}, Data: {event.data}')

        gui_context.step()
        
        win.fill((0, 0, 0))
        gui_context.draw(win)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()



if __name__ == '__main__':
    main()
