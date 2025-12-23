

import pygame
from world import WorldContext

def main():
    # tester
    from element import RectanglarSurfElement, TokenElement
    context = WorldContext()
    context.initialize()

    elements = [
        RectanglarSurfElement(pygame.image.load(r'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\vaps2.png')),
        TokenElement(pygame.image.load(r'C:\Users\e021776\OneDrive - Elbit Systems 365\Pictures\imageTest1.png'))
    ]
    [context.add_element(element) for element in elements]

    context.main_loop()


if __name__ == '__main__':
    main()