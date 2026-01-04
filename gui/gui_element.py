

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pygame
from pygame import Vector2

from gui.gui_globals import *

@dataclass
class GuiAssets:
    font: pygame.Font = None


class GuiEventType:
    BUTTON_CLICK = 0


@dataclass
class GuiEvent:
    type: GuiEventType
    data: dict[Any, Any]


class GuiElement:
    def __init__(self, **kwargs):
        self.key = kwargs.get('key', None)
        self.pos: Vector2 = Vector2()
        self.size: Vector2 = Vector2()

    def initialize(self, assets: GuiAssets) -> None:
        ...

    def set_pos(self, pos: Vector2) -> None:
        self.pos = pos

    def get_size(self) -> Vector2:
        ...

    def handle_event(self, event: pygame.Event) -> GuiEvent:
        ...
    
    def step(self) -> None:
        ...

    def draw(self, win: pygame.Surface) -> None:
        ...


def calculate_layout(layout: list[list[GuiElement]], initial_pos: Vector2, assets: GuiAssets) -> tuple[list[GuiElement], Vector2]:
    elements: list[GuiElement] = []
    x = initial_pos[0] + margin
    y = initial_pos[1] + margin
    w = margin
    h = margin
    for row in layout:
        row_height = 0
        x = initial_pos[0] + margin
        row_width = 0
        for element in row:
            element.set_pos(Vector2(x, y))
            element.initialize(assets)
            row_height = max(row_height, element.get_size()[1])
            elements.append(element)
            x += element.get_size()[0] + margin
            row_width += element.get_size()[0] + margin
        y += row_height + margin
        h += row_height + margin
        w = max(w, row_width)
        
    size = Vector2(w + margin, h)
    return elements, size
    