


import pygame
from pygame import Vector2

from world_canvas.transformation import Transformation
from world_canvas.element import Element, Database
from world_canvas.handle import Handle


class Viewport:
    def __init__(self, world_transform: Transformation, database: Database):
        self.world_transform = world_transform
        self.database = database
        self.selected_elements: list[Element] = []

        self.hovered_handle: Handle = None
        self.hovered_element: Element = None

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            # Convert mouse position to world coordinates before zoom
            world_pos = self.world_transform.pos + mouse_pos / self.world_transform.scale
            
            # Apply zoom
            if event.y > 0:
                self.world_transform.scale *= 1.1
            else:
                self.world_transform.scale *= 0.9
            
            # Adjust position so the world point stays under the mouse
            self.world_transform.pos = world_pos - mouse_pos / self.world_transform.scale

    def step(self) -> None:
        ...
        # mouse_in_world = self.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos())))
        # self.hovered_handle = self.get_handle_at(mouse_in_world)
        # self.hovered_element = self.get_element_at(mouse_in_world)

    def get_element_at(self, world_pos: Vector2) -> Element:
        for element in reversed(self.database.elements):
            if element.hit_test(world_pos):
                return element
        return None

    def get_handle_at(self, world_pos: Vector2) -> Handle:
        for element in reversed(self.database.elements):
            for handle in element.handles:
                if handle.hit_test(world_pos):
                    return handle
        return None

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...
        # if self.hovered_handle:
        #     self.hovered_handle.draw(win, transform)
