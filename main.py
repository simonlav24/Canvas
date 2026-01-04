

from random import randint, choice

import pygame
from pygame import Vector2

from world_canvas import WorldCanvas
from world_canvas import RectanglarSurfElement, TokenElement
from shapes import Polygon, PolygonTool, Rectangle
from gui import GuiContext, Label, Button, ToggleButton

def main():
    # tester
    context = WorldCanvas()
    width, height = 1280, 720
    context.initialize(width, height)

    context.assign_tool(pygame.K_p, PolygonTool)

    elements = [
        RectanglarSurfElement(pygame.image.load(r'C:\Simon\Projects\CardGamesMaster\assets\card_sprite.png')),
    ]

    for _ in range(10):
        elements.append(token := TokenElement(pygame.image.load(r'C:\Simon\Projects\dnd-vtt\assets\tokens\Token-Character-Knight-Male.png')))
        token.transformation.pos = Vector2(randint(0, width), randint(0, height))

    elements.append(Polygon((255, 255, 255), [
        Vector2(0, 0),
        Vector2(0, 100),
        Vector2(200, 100),
    ]))
    elements.append(Rectangle((255, 255, 255), Vector2(100, 100), Vector2(200, 400)))
    [context.add_element(element) for element in elements]


    # gui
    gui_context = GuiContext()
    gui_context.set_layout([
        [Label('label1:'), Button('button1', key='button1')],
        [Label('label2:'), Button('button2', key='button2')],
        [Label('label3:'), Button('button3', key='button3')],
        [Label('label3:'), ToggleButton('selected', key='button3')],
    ])


    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get():
            event_handled = False
            gui_context.handle_event(event)
            for event in gui_context.get_gui_events():
                event_handled = True
                print(f'GUI Event: {event.type}, Data: {event.data}')
            if event_handled:
                continue

            context.handle_event(event)

            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        
        context.step()
        gui_context.step()
        
        context.draw()
        gui_context.draw(context.win)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()