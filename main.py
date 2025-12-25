

from random import randint, choice

import pygame
from pygame import Vector2

from world_canvas import WorldCanvas
from world_canvas import RectanglarSurfElement, TokenElement

from shapes import Polygon, PolygonTool

def main():
    # tester
    context = WorldCanvas()
    width, height = 1280, 720
    context.initialize(width, height)

    context.assign_tool(pygame.K_p, PolygonTool)

    elements = [
        RectanglarSurfElement(pygame.image.load(r'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\vaps2.png')),
    ]

    for _ in range(10):
        elements.append(token := TokenElement(pygame.image.load(rf'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\imageTest{choice([str(i+1) for i in range(3)])}.png')))
        token.transformation.pos = Vector2(randint(0, width), randint(0, height))

    elements.append(Polygon((255, 255, 255), [
        Vector2(0, 0),
        Vector2(0, 100),
        Vector2(200, 100),
    ]))

    [context.add_element(element) for element in elements]
    context.main_loop()


if __name__ == '__main__':
    main()