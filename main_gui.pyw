

from random import randint
import json

import pygame
from pygame import Vector2

from canvasim.gui import GuiContext, GuiStandAlone, Label, Button, ToggleButton, Textbox, RadioButton, Slider

layout = None

def handle_gui_event(event, values):
    print(f'GUI Event: {event.type}, Data: {event.data}, values: {values}')

def main(layout):
    pygame.init()

    gui_context = GuiContext()
    gui_context.set_layout(layout)
    
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

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    values = gui_context.get_values()
                    # save values to file
                    with open('gui_values.json', 'w') as f:
                        json.dump(values, f)
                
                if event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # load values from file
                    with open('gui_values.json', 'r') as f:
                        values = json.load(f)
                    gui_context.set_values(values)
        
        for event in gui_context.get_gui_events():
            values = gui_context.get_values()
            handle_gui_event(event, values)

        gui_context.step()
        
        win.fill((0, 0, 0))
        gui_context.draw(win)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()



def main_standalone(layout):
    gui = GuiStandAlone(font=("david", 18), title='Gui tester')
    gui.initialize(layout, handle_gui_event)
    gui.main_loop()


if __name__ == '__main__':

    layout = [
        [Label('This is a gui app')],
        [Button('button1'), Button('button2'), Button('button3'), Button('button4')],
        [Label('toggles:'), ToggleButton('select2', toggle=True), ToggleButton('select3')],
        [Label('radios:'), RadioButton('option1', 'group1', toggle=True), RadioButton('option2', 'group1'), RadioButton('option3', 'group1')],
        [Textbox('this is text', key='text1'), Textbox('empty', key='text2')],
        [Slider(0, 100, 25, key='slider1'), Slider(key='slider2')],
    ]

    main(layout)
