

from world_canvas import Element, Transformation, Handle

import pygame
from pygame import Vector2

class Polygon(Element):
    def __init__(self, color: pygame.Color, points: list[Vector2]):
        super().__init__()
        self.points = [Transformation(point) for point in points]
        self.handles = [Handle(point, 10, self) for point in self.points]
        self.color = color
    
    def add_point(self, point: Vector2) -> None:
        point_transform = Transformation(point)
        self.points.append(point_transform)
        self.handles.append(Handle(point_transform, 10, self))

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        if len(self.points) < 3:
            return
        pygame.draw.polygon(win, self.color, [transform.transform(point).pos for point in self.points])