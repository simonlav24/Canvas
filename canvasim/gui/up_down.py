


import pygame
from pygame import Vector2

from .gui_element import GuiElement, GuiEvent, calculate_layout, GuiEventType
from .primitives import Button
from .text_box import Textbox
from .gui_globals import *
from .color_utils import lighten


class UpDown(GuiElement):
    def __init__(self, initial_value: float, step: float, decimals: int=3, **kwargs):
        super().__init__(**kwargs)
        self.value = initial_value
        self.step_value = step
        self.decimals = decimals
        self.text = self._to_string()
        self.text_box_element: Textbox = None

    def _to_string(self) -> str:
        return f"{self.value:.{self.decimals}f}"
    
    def get_value(self):
        return self.value

    def initialize(self, assets):
        self.text_box_element = Textbox(self.text, 100)
        layout = [[self.text_box_element, Button('^', key=1.0), Button('V', key=-1.0)]]
        elements, size = calculate_layout(layout, self.pos, assets)
        self.size = size
        self.elements = elements
    
    def handle_event(self, event):
        output_event = None
        for element in self.elements:
            output_event = element.handle_event(event)
            if output_event is not None and output_event.type == GuiEventType.BUTTON_CLICK:
                self.value = self.value + self.step_value * output_event.data['key']
                self.text_box_element.update(self._to_string())
        return None

    def draw(self, win):
        for element in self.elements:
            element.draw(win)