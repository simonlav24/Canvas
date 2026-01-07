

import pygame
from pygame import Vector2

from .gui_element import GuiElement, GuiEvent
from .gui_globals import *
from .color_utils import lighten

SLIDER_SIZE = Vector2(200, 25)

class Slider(GuiElement):
    def __init__(self, min_value: float=0.0, max_value: float=1.0, initial_value: float=0.5, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        self.surf: pygame.Surface = pygame.Surface(SLIDER_SIZE, pygame.SRCALPHA)
        self.is_hovered = False
        self.is_holding = False

    def get_size(self) -> Vector2:
        return Vector2(self.surf.get_size())

    def initialize(self, assets):
        super().initialize(assets)
        self.redraw()

    def get_value(self) -> float:
        return self.value
    
    def update(self, value: float) -> None:
        self.value = max(self.min_value, min(self.max_value, value))

    def handle_event(self, event) -> GuiEvent:
        self.was_hovering = self.is_hovered
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = False
            rect = pygame.Rect(self.pos, self.get_size())
            if rect.collidepoint(Vector2(event.pos)):
                self.is_hovered = True
                self.redraw()

            if self.is_holding:
                pos_x = Vector2(event.pos)[0] - self.pos[0]
                pos_0 = Vector2(SLIDER_SIZE[1] * 0.5, SLIDER_SIZE[1] * 0.5)
                pos_1 = Vector2(SLIDER_SIZE[0] - SLIDER_SIZE[1] * 0.5, SLIDER_SIZE[1] * 0.5)
                factor = (pos_x - pos_0[0]) / (pos_1[0] - pos_0[0])
                self.value = max(min(self.min_value + factor * (self.max_value - self.min_value), self.max_value), self.min_value)
                self.redraw()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_holding = True
            self.redraw()
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_holding = False
            self.redraw()

        if self.was_hovering != self.is_hovered:
            self.redraw()
        return None

    def redraw(self) -> None:
        self.surf.fill((0, 0, 0, 0))
        pos_0 = Vector2(SLIDER_SIZE[1] * 0.5, SLIDER_SIZE[1] * 0.5)
        pos_1 = Vector2(SLIDER_SIZE[0] - SLIDER_SIZE[1] * 0.5, SLIDER_SIZE[1] * 0.5)
        factor = (self.value - self.min_value) / (self.max_value - self.min_value)
        handle_pos = pos_0 + (pos_1 - pos_0) * factor

        color = (COLOR_SLIDER_EMPTY, COLOR_SLIDER_FULL)
        if self.is_hovered:
            color = (lighten(color[0], 20), lighten(color[1], 20))

        size = Vector2(SLIDER_SIZE[0] - SLIDER_SIZE[1] * 0.5, SLIDER_SIZE[1] * 0.25)
        pos = Vector2(SLIDER_SIZE[1] * 0.25, SLIDER_SIZE[1] * 0.5 - size[1] * 0.5)
        pygame.draw.rect(self.surf, color[0], (pos, size), 0, border_radius=int(SLIDER_SIZE[0]))
        pygame.draw.rect(self.surf, color[1], (pos, (size[0] * factor, size[1])), 0, border_radius=int(SLIDER_SIZE[0]))
        pygame.draw.circle(self.surf, color[1], handle_pos, SLIDER_SIZE[1] * 0.4)

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.surf, self.pos)

