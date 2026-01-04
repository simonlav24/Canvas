
from typing import Any

import pygame
from pygame import Vector2

from . import world_globals
from .edit_tool import EditTool, SelectTool
from .transformation import Transformation
from .viewport import Viewport
from .draw_utils import draw_axis, draw_grid
from .element import Element, Database

class WorldCanvas:
    def __init__(self):
        self.win: pygame.Surface = None
        self.clock = pygame.time.Clock()

        self.database = Database()
        self.world_transform = Transformation(Vector2())

        self.viewport = Viewport(self.world_transform, self.database)

        self.default_tool = SelectTool
        self.tool: EditTool = self.default_tool(self.viewport)

        self.assigned_tools: dict[int, Any] = {}

    def initialize(self, width, height):
        world_globals.initialize(width, height)
        pygame.init()
        self.win = pygame.display.set_mode((world_globals.win_width, world_globals.win_height))
        pygame.display.set_caption("Map")

    def add_element(self, element: Element) -> None:
        self.database.elements.append(element)

    def handle_event(self, event) -> None:
        self.viewport.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.tool = self.tool.handle_mouse_down(event)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.tool = self.tool.handle_mouse_up(event)

        if event.type == pygame.MOUSEMOTION:
            self.tool = self.tool.handle_mouse_motion(event)

        if event.type == pygame.KEYDOWN:
            if event.key in self.assigned_tools.keys():
                self.tool = self.assigned_tools[event.key]()
                print(self.tool)
            else:
                self.tool = self.tool.handle_key_down(event)

        if event.type == pygame.KEYUP:
            self.tool = self.tool.handle_key_up(event)

        if self.tool is None:
            self.tool = self.default_tool(self.viewport)

    def step(self) -> None:
        self.tool.step()
        self.viewport.step()

    def draw(self) -> None:
        self.win.fill((30, 30, 30))

        draw_grid(self.win, self.world_transform)
        draw_axis(self.win, self.world_transform)

        for element in self.database.elements:
            element.draw(self.win, self.world_transform)

        self.tool.draw(self.win, self.world_transform)
        self.viewport.draw(self.win, self.world_transform)

    def assign_tool(self, key: int, tool_cls: Any) -> None:
        self.assigned_tools[key] = lambda: tool_cls(self.viewport)

    def main_loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                self.handle_event(event)
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True

            self.step()
            self.draw()

            pygame.display.flip()
            self.clock.tick(world_globals.FPS)
        pygame.quit()


def main():
    context = WorldCanvas()
    context.initialize()
    context.main_loop()


if __name__ == '__main__':
    main()
