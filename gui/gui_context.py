
from typing import Any

import pygame
from pygame import Vector2

from gui.gui_element import GuiElement, GuiEvent, GuiAssets, calculate_layout
from gui.gui_globals import *


class GuiContext:
    def __init__(self, pos: Vector2=None):
        self.elements: list[GuiElement] = []
        self.gui_events: list[GuiEvent] = []
        self.assets = GuiAssets(pygame.font.SysFont(*font_name))
        self.size: Vector2 = Vector2(0, 0)
        self.pos = pos
        if self.pos is None:
            self.pos: Vector2 = Vector2(0, 0)
    
    def set_layout(self, layout: list[list[GuiElement]]):
        elements, size = calculate_layout(layout, self.pos, self.assets)
        self.size = size
        self.elements = elements

    def get_gui_events(self) -> list[GuiEvent]:
        events = self.gui_events.copy()
        self.gui_events.clear()
        return events

    def handle_event(self, event) -> None:
        output_event: GuiEvent = None
        for element in self.elements:
            output_event = element.handle_event(event)
            if output_event is not None:
                self.gui_events.append(output_event)
    
    def step(self):
        for element in self.elements:
            element.step()
    
    def draw(self, win: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(win)
