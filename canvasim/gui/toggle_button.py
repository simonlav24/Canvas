
import pygame
from pygame import Vector2

from .gui_element import GuiAssets
from .gui_globals import *
from .primitives import Label, ToggleableElement, ToggleableButton, CHECK_BOX_SIZE
from .color_utils import lighten


class ToggleElement(ToggleableElement):
    def initialize(self, assets):
        super().initialize(assets)
        self.check_surface = pygame.Surface(CHECK_BOX_SIZE, pygame.SRCALPHA)

    def redraw(self) -> None:
        self.check_surface.fill((0, 0, 0, 0))
        pos = (
            (1 - self.animation_factor) * Vector2(CHECK_BOX_SIZE[1] * 0.5, CHECK_BOX_SIZE[1] * 0.5) +
            (self.animation_factor) * Vector2(CHECK_BOX_SIZE[0] - CHECK_BOX_SIZE[1] * 0.5, CHECK_BOX_SIZE[1] * 0.5)
        )
        color = (COLOR_TOGGLE_BACK_OFF, COLOR_TOGGLE_HANDLE_OFF)
        if self.is_toggled:
            color = (COLOR_TOGGLE_BACK_ON, COLOR_TOGGLE_HANDLE_ON)
        if self.is_hovered:
            color = (lighten(color[0], 20), lighten(color[1], 20))

        pygame.draw.rect(self.check_surface, color[0], (CHECK_BOX_SIZE * 0.25, CHECK_BOX_SIZE * 0.5), 0, border_radius=int(CHECK_BOX_SIZE[0]))
        pygame.draw.circle(self.check_surface, color[1], pos, CHECK_BOX_SIZE[1] * 0.5)


class ToggleButton(ToggleableButton):
    def initialize(self, assets: GuiAssets) -> None:
        self.check_element = ToggleElement(self.is_toggled)
        self.layout = [[self.check_element, Label(self.text)]]
        super().initialize(assets)

