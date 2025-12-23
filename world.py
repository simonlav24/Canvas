

import pygame
from pygame import Vector2

from world_globals import *
from edit_tool import *
from transformation import Transformation
from viewport import Viewport
from draw_utils import draw_axis, draw_grid
from element import Element, Database
from handle import Handle


class WorldContext:
    def __init__(self):
        self.win: pygame.Surface = None
        self.clock = pygame.time.Clock()

        self.database = Database()
        self.world_transform = Transformation(Vector2())

        self.viewport = Viewport(self.world_transform, self.database)
        self.tool = IdleTool(self.viewport)

    def initialize(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Map")

    def add_element(self, element: Element) -> None:
        self.database.elements.append(element)

    def handle_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            ...

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

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.tool = self.tool.handle_mouse_down(event)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.tool = self.tool.handle_mouse_up(event)

        if event.type == pygame.MOUSEMOTION:
            self.tool = self.tool.handle_mouse_motion(event)

        if event.type == pygame.KEYDOWN:
            self.tool = self.tool.handle_key_down(event)

        if event.type == pygame.KEYUP:
            self.tool = self.tool.handle_key_up(event)

    def step(self) -> None:
        self.viewport.step()

    def draw(self) -> None:
        self.win.fill((30, 30, 30))

        draw_grid(self.win, self.world_transform)
        draw_axis(self.win, self.world_transform)

        for element in self.database.elements:
            element.draw(self.win, self.world_transform)

        self.viewport.draw(self.win, self.world_transform)

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
            self.clock.tick(FPS)
        pygame.quit()


def main():
    context = WorldContext()
    context.initialize()
    context.main_loop()


if __name__ == '__main__':
    main()
