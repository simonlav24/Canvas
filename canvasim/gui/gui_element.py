

from dataclasses import dataclass
from enum import Enum
from typing import Any

import pygame
from pygame import Vector2

from .gui_globals import *

@dataclass
class GuiAssets:
    font: pygame.Font = None


class GuiEventType:
    BUTTON_CLICK = 0
    TOGGLE_BUTTON_CLICK = 1
    RADIO_BUTTON_CLICK = 2

@dataclass
class GuiEvent:
    type: GuiEventType
    data: dict[Any, Any]
    caller: 'GuiElement'

class GuiElement:
    def __init__(self, **kwargs):
        self.key = kwargs.get('key', None)
        self.pos: Vector2 = Vector2()
        self.size: Vector2 = Vector2()

    def initialize(self, assets: GuiAssets) -> None:
        ...

    def set_pos(self, pos: Vector2, absolute: bool=True) -> None:
        if absolute:
            self.pos = pos
        else:
            self.pos += pos

    def get_size(self) -> Vector2:
        return self.size

    def handle_event(self, event: pygame.Event) -> GuiEvent:
        ...
    
    def step(self) -> None:
        ...

    def draw(self, win: pygame.Surface) -> None:
        ...
    
    def update(self, value: Any) -> None:
        '''update element's value'''
    
    def get_value(self) -> Any:
        '''get element's value'''
        return None


class Filler(GuiElement):
    ...


def calculate_layout(layout: list[list[GuiElement]], initial_pos: Vector2, assets: GuiAssets) -> tuple[list[GuiElement], Vector2]:
    '''Calculate layout of gui elements and return list of elements with positions set and total size'''
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
            if isinstance(element, Filler):
                continue
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

    # second pass for fillers
    for row in layout:
        row_filler_count = 0
        row_space = 0
        for element in row:
            if isinstance(element, Filler):
                row_filler_count += 1
            else:
                row_space += element.get_size()[0] + margin

        row_empty_space = size[0] - row_space - margin
        if row_filler_count == 0:
            continue
        
        filler_width = row_empty_space / row_filler_count

        for i, element in enumerate(row):
            if isinstance(element, Filler) and i < len(row) - 1:
                for next_element in row[i + 1:]:
                    next_element.set_pos(Vector2(filler_width, 0), absolute=False)

    return elements, size
    