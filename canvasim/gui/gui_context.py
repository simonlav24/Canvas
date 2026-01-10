
from typing import Any

import pygame
from pygame import Vector2

from .gui_element import GuiElement, GuiEvent, GuiEventType, GuiAssets, calculate_layout
from .gui_globals import *
from .radio_button import RadioButton


class GuiContext:
    def __init__(self, pos: Vector2=None, **kwargs):
        self.elements: list[GuiElement] = []
        self.gui_events: list[GuiEvent] = []
        self.assets: GuiAssets = None
        self.size: Vector2 = Vector2(0, 0)
        self.pos = pos
        if self.pos is None:
            self.pos: Vector2 = Vector2(0, 0)
        self.focused_element: GuiElement = None
        self.font = kwargs.get('font', default_font)
        self.radio_groups: dict[Any, list[RadioButton]] = {}
    
    def set_layout(self, layout: list[list[GuiElement]]):
        self.assets = GuiAssets(pygame.font.SysFont(*self.font))
        elements, size = calculate_layout(layout, self.pos, self.assets)
        self.size = size
        self.elements = elements

        for element in self.elements:
            if isinstance(element, RadioButton):
                group = element.group
                if group not in self.radio_groups:
                    self.radio_groups[group] = []
                self.radio_groups[group].append(element)

    def get_gui_events(self) -> list[GuiEvent]:
        events = self.gui_events.copy()
        self.gui_events.clear()
        return events

    def get_values(self) -> dict[Any, Any]:
        values = {}
        for element in self.elements:
            value = element.get_value()
            if element.key is not None and value is not None:
                values[element.key] = value
        return values
    
    def set_values(self, values: dict[Any, Any]) -> None:
        for element in self.elements:
            if element.key in values:
                element.update(values[element.key])

    def handle_event(self, event) -> None:
        output_event: GuiEvent = None
        for element in self.elements:
            output_event = element.handle_event(event)
            if output_event is not None:
                self.gui_events.append(output_event)

                # Handle radio button logic
                if output_event.type == GuiEventType.RADIO_BUTTON_CLICK:
                    group = self.radio_groups.get(output_event.caller.group, [])
                    is_any_updated = False
                    for radio in group:
                        if radio != output_event.caller:
                            if radio.get_value() == True:
                                radio.update(False)
                                is_any_updated = True
                    if not is_any_updated:
                        output_event.caller.update(True)
        
        # Check if focus changed
        new_focused = None
        for element in self.elements:
            if hasattr(element, 'is_focused') and element.is_focused:
                new_focused = element
                break
        
        if new_focused != self.focused_element:
            if self.focused_element:
                self.focused_element.is_focused = False
            self.focused_element = new_focused
            if self.focused_element:
                pygame.key.start_text_input()
            else:
                pygame.key.stop_text_input()
    
    def step(self):
        for element in self.elements:
            element.step()
    
    def draw(self, win: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(win)


class GuiStandAlone(GuiContext):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', 'CanvaSim App')
        self.frame = pygame.NOFRAME if kwargs.get('no_frame', False) else 0
        
    def initialize(self, layout: list[list[GuiElement]], event_handler=None) -> None:
        pygame.init()
        self.event_handler = event_handler
        self.set_layout(layout)

    def main_loop(self) -> None:
        win = pygame.display.set_mode(self.size, self.frame)
        pygame.display.set_caption(self.title)
        clock = pygame.time.Clock()

        done = False
        while not done:
            for event in pygame.event.get():
                # handle events
                self.handle_event(event)

                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
            
            for event in self.get_gui_events():
                values = self.get_values()
                if self.event_handler:
                    self.event_handler(event, values)

            self.step()
            
            win.fill(COLOR_BACKGROUND)
            self.draw(win)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
