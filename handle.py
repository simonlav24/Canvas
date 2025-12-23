
import pygame
from transformation import Transformation


class Handle:
    def __init__(self, transformation: Transformation, radius: float):
        self.transformation = transformation
        self.radius = radius
    
    def hit_test(self, world_transform: Transformation, world_position: Transformation) -> bool:
        my_world_pos = world_transform.transform(self.transformation)
        if (world_position.pos - my_world_pos.pos).length() < self.radius:
            return True
        return False
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        my_world_pos = transform.transform(self.transformation)
        pygame.draw.circle(win, (255, 255, 255), my_world_pos.pos, self.radius, 1)
