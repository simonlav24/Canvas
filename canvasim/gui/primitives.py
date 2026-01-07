

import pygame
from pygame import Vector2

from .gui_element import GuiElement, GuiAssets, GuiEvent, GuiEventType, calculate_layout
from .gui_globals import *

CHECK_BOX_SIZE = Vector2(50, 25)


class Label(GuiElement):
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.surf: pygame.Surface = None   

    def initialize(self, assets: GuiAssets) -> None:
        self.surf = assets.font.render(self.text, True, COLOR_LABEL)

    def get_size(self) -> Vector2:
        return Vector2(self.surf.get_size()) + Vector2(margin, margin) * 2

    def draw(self, win: pygame.Surface) -> None:
        # pygame.draw.rect(win, COLOR_BACKGROUND, (self.pos, self.get_size()))
        win.blit(self.surf, self.pos + Vector2(margin, margin))



class Button(GuiElement):
    def __init__(self, text: str, layout: list[list[GuiElement]]=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        if self.key is None:
            self.key = self.text
        self.elements: list[GuiElement] = []
        self.layout = layout
        self.is_hovered = False

    def initialize(self, assets: GuiAssets) -> None:
        if self.layout is None:
            self.layout = [[Label(self.text)]]
        elements, size = calculate_layout(self.layout, self.pos, assets)
        self.size = size
        self.elements = elements
    
    def handle_event(self, event) -> GuiEvent:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = False
            mouse_pos = Vector2(event.pos)
            rect = pygame.Rect(self.pos, self.get_size())
            if rect.collidepoint(mouse_pos):
                self.is_hovered = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return GuiEvent(GuiEventType.BUTTON_CLICK, {'key': self.key}, self)
        return None

    def step(self) -> None:
        for element in self.elements:
            element.step()

    def get_size(self) -> Vector2:
        return self.size

    def draw(self, win: pygame.Surface) -> None:
        back_color = COLOR_BUTTON if not self.is_hovered else COLOR_BACKGROUND_HOVER
        pygame.draw.rect(win, back_color, (self.pos, self.get_size()))
        for element in self.elements:
            element.draw(win)



class SurfaceElement(GuiElement):
    def __init__(self, surface: pygame.Surface, **kwargs):
        super().__init__(**kwargs)
        self.surface = surface

    def get_size(self) -> Vector2:
        return Vector2(self.surface.get_size()) + Vector2(margin, margin) * 2

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.surface, self.pos)


class ToggleableElement(GuiElement):
    def __init__(self, is_toggled: bool=False, **kwargs):
        super().__init__(**kwargs)
        self.is_toggled = is_toggled
        self.is_hovered = False
        self.animation_factor = 0.0
        self.check_surface = None
    
    def initialize(self, assets):
        ...

    def get_size(self) -> Vector2:
        return self.check_surface.get_size()
    
    def update(self, value: bool) -> None:
        self.is_toggled = value

    def step(self) -> None:
        target = 1.0 if self.is_toggled else 0.0
        if abs(target - self.animation_factor) < 0.01:
            self.animation_factor = target
        else:
            self.animation_factor = self.animation_factor + (target - self.animation_factor) * 0.2

    def redraw(self) -> None:
        ...

    def draw(self, win: pygame.Surface) -> None:
        self.redraw()
        win.blit(self.check_surface, self.pos)


class ToggleableButton(Button):
    def __init__(self, text: str, toggle: bool=False, **kwargs):
        self.is_toggled = toggle
        self.check_element: ToggleableElement = None
        super().__init__(text, None, **kwargs)

    def initialize(self, assets: GuiAssets) -> None:
        super().initialize(assets)

    def get_value(self):
        return self.is_toggled

    def update(self, value: bool) -> None:
        self.is_toggled = value
        self.check_element.is_toggled = value

    def handle_event(self, event):
        output_event = super().handle_event(event)
        if output_event is not None:
            if self.is_hovered:
                self.is_toggled = not self.is_toggled
                self.check_element.is_toggled = self.is_toggled
                output_event = GuiEvent(GuiEventType.TOGGLE_BUTTON_CLICK, {'key': self.key}, self)
        self.check_element.is_hovered = self.is_hovered
        return output_event
    
    def draw(self, win: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(win)