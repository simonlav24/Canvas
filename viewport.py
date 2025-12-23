


import pygame
from pygame import Vector2

from world_globals import *
from edit_tool import *
from transformation import Transformation
from element import Element, Database
from handle import Handle


class Viewport:
    def __init__(self, world_transform: Transformation, database: Database):
        self.world_transform = world_transform
        self.database = database
        self.selected_elements: list[Element] = []

        self.hovered_handle: Handle = None

    def step(self) -> None:
        mouse_in_world = self.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos())))
        self.hovered_handle = self.get_handle_at(mouse_in_world)

    def get_handle_at(self, world_pos: Vector2) -> Handle:
        for element in reversed(self.database.elements):
            for handle in element.handles:
                if handle.hit_test(self.world_transform, world_pos):
                    return handle
        return None

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        if self.hovered_handle:
            self.hovered_handle.draw(win, transform)
