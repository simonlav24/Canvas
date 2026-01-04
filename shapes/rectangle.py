




from world_canvas import Element, Transformation, Handle

import pygame
from pygame import Vector2

class Rectangle(Element):
    def __init__(self, color: pygame.Color, point1: Vector2, point2: Vector2):
        super().__init__()

        pos = Vector2(min([point1, point2], key=lambda x: x[0]), min([point1, point2], key=lambda x: x[1]))
        self.size = Vector2(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))
        self.transformation = Transformation(pos)
        self.color = color
    
    def get_rect(self, transform: Transformation) -> pygame.Rect:
        pos = transform.transform(self.transformation).pos
        return pygame.Rect(pos, self.size * transform.scale)

    def hit_test(self, world_pos: Vector2) -> bool:
        rect = self.get_rect(Transformation(Vector2()))
        return rect.collidepoint(world_pos)

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        rect = self.get_rect(transform)
        pygame.draw.rect(win, self.color, rect)