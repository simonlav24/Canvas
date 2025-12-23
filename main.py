

from random import randint

import pygame
from pygame import Vector2

from world_globals import WIDTH, HEIGHT
from world import WorldContext

def main():
    # tester
    from element import RectanglarSurfElement, TokenElement
    context = WorldContext()
    context.initialize()

    elements = [
        RectanglarSurfElement(pygame.image.load(r'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\vaps2.png')),
    ]

    for i in range(10):
        elements.append(token := TokenElement(pygame.image.load(r'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\imageTest1.png')))
        token.transformation.pos = Vector2(randint(0, WIDTH), randint(0, HEIGHT))

    [context.add_element(element) for element in elements]

    context.main_loop()


if __name__ == '__main__':
    main()