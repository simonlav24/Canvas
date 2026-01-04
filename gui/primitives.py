

import pygame
from pygame import Vector2

from gui.gui_element import GuiElement, GuiAssets, GuiEvent, GuiEventType, calculate_layout
from gui.gui_globals import *



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
        pygame.draw.rect(win, COLOR_BACKGROUND, (self.pos, self.get_size()))
        win.blit(self.surf, self.pos + Vector2(margin, margin))



class Button(GuiElement):
    def __init__(self, text: str, layout: list[list[GuiElement]]=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        if self.key is None:
            self.key = self.text
        self.elements: list[GuiElement] = []
        self.layout = layout
        if self.layout is None:
            self.layout = [[Label(text)]]
        self.is_hovered = False

    def initialize(self, assets: GuiAssets) -> None:
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
                return GuiEvent(GuiEventType.BUTTON_CLICK, {'key': self.key})
        return None

    def step(self) -> None:
        for element in self.elements:
            element.step()

    def get_size(self) -> Vector2:
        return self.size

    def draw(self, win: pygame.Surface) -> None:
        back_color = COLOR_BACKGROUND if not self.is_hovered else COLOR_BACKGROUND_HOVER
        pygame.draw.rect(win, back_color, (self.pos, self.get_size()))
        for element in self.elements:
            element.draw(win)
