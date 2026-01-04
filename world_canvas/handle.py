
from typing import Any, Protocol

import pygame
from pygame import Vector2
from world_canvas.transformation import Transformation


class Selectable(Protocol):
    def hit_test(self, world_pos: Vector2) -> bool:
        ...
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...

    def set_pos(self, pos: Vector2) -> None:
        ...


class Handle:
    def __init__(self, transformation: Transformation, radius: float, owner: Any):
        self.transformation = transformation
        self.radius = radius
        self.owner: Any = owner
    
    def hit_test(self, world_pos: Vector2) -> bool:
        my_world_pos = self.transformation
        if (world_pos - my_world_pos.pos).length() < self.radius:
            return True
        return False
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        my_world_pos = transform.transform(self.transformation)
        pygame.draw.circle(win, (255, 255, 255), my_world_pos.pos, self.radius * transform.scale, 1)
