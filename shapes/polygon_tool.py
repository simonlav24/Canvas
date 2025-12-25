

import pygame
from pygame import Vector2

from world_canvas import EditTool, Transformation
from shapes import Polygon


class PolygonTool(EditTool):
    def __init__(self, context):
        super().__init__(context)
        self.polygon = Polygon((255, 255, 255), [])
        self.viewport.database.elements.append(self.polygon)

    def handle_mouse_down(self, event) -> 'EditTool':
        mouse_pos = pygame.mouse.get_pos()
        point_in_world = self.viewport.world_transform.transform_back(Transformation(Vector2(mouse_pos)))
        self.polygon.add_point(point_in_world.pos)
        return self
    
    def handle_key_down(self, event):
        if event.key == pygame.K_RETURN:
            return None

        return self

    def draw(self, win: pygame.Surface) -> None:
        if len(self.polygon.points) < 2:
            return
        points = [self.viewport.world_transform.transform(point).pos for point in [self.polygon.points[-1], self.polygon.points[0]]]
        points.append(Vector2(pygame.mouse.get_pos()))
        pygame.draw.polygon(win, (255, 255, 255), points, 1)
