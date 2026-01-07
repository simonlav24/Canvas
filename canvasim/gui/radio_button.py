
from typing import Any

import pygame
from pygame import Vector2

from .gui_globals import *
from .gui_element import GuiEvent, GuiEventType
from .primitives import Label, ToggleableElement, ToggleableButton
from .color_utils import lighten

RADIO_BOX_SIZE = Vector2(25, 25)

class RadioElement(ToggleableElement):
    def initialize(self, assets):
        super().initialize(assets)
        self.check_surface = pygame.Surface(RADIO_BOX_SIZE, pygame.SRCALPHA)

    def redraw(self) -> None:
        self.check_surface.fill((0, 0, 0, 0))
        radius = (
            (self.animation_factor) * RADIO_BOX_SIZE[1] * 0.25 +
            (1 - self.animation_factor) * 0
        )
        color = (COLOR_TOGGLE_BACK_OFF, COLOR_TOGGLE_HANDLE_OFF)
        if self.is_toggled:
            color = (COLOR_TOGGLE_BACK_ON, COLOR_TOGGLE_HANDLE_ON)
        if self.is_hovered:
            color = (lighten(color[0], 20), lighten(color[1], 20))

        pygame.draw.circle(self.check_surface, color[1], RADIO_BOX_SIZE / 2, RADIO_BOX_SIZE[1] * 0.5, 2)
        pygame.draw.circle(self.check_surface, color[1], RADIO_BOX_SIZE / 2, radius)


class RadioButton(ToggleableButton):
    def __init__(self, text, group: Any, toggle = False, **kwargs):
        super().__init__(text, toggle, **kwargs)
        self.group = group

    def initialize(self, assets):
        self.check_element = RadioElement(self.is_toggled)
        self.layout = [[self.check_element, Label(self.text)]]
        super().initialize(assets)

    def handle_event(self, event):
        output_event = super().handle_event(event)
        if output_event is not None:
            output_event = GuiEvent(GuiEventType.RADIO_BUTTON_CLICK, {'key': self.key}, self)
        return output_event
