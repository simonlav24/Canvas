

import pygame
from pygame import Vector2

from gui.gui_element import GuiElement, GuiAssets, GuiEvent, GuiEventType, calculate_layout
from gui.gui_globals import *

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



class ToggleElement(GuiElement):
    def __init__(self, is_toggled: bool=False, **kwargs):
        super().__init__(**kwargs)
        self.is_toggled = is_toggled
        self.is_hovered = False
        self.position_factor = 0.0
        self.check_surface = pygame.Surface(CHECK_BOX_SIZE, pygame.SRCALPHA)
    
    def get_size(self) -> Vector2:
        return self.check_surface.get_size()
    
    def update(self, value: bool) -> None:
        self.is_toggled = value

    def step(self) -> None:
        target = 1.0 if self.is_toggled else 0.0
        if abs(target - self.position_factor) < 0.01:
            self.position_factor = target
        else:
            self.position_factor = self.position_factor + (target - self.position_factor) * 0.2

    def redraw(self) -> None:
        self.check_surface.fill((0, 0, 0, 0))
        pos = (
            (1 - self.position_factor) * Vector2(CHECK_BOX_SIZE[1] * 0.5, CHECK_BOX_SIZE[1] * 0.5) +
            (self.position_factor) * Vector2(CHECK_BOX_SIZE[0] - CHECK_BOX_SIZE[1] * 0.5, CHECK_BOX_SIZE[1] * 0.5)
        )
        if self.is_toggled:
            pygame.draw.rect(self.check_surface, COLOR_TOGGLE_BACK_ON, (CHECK_BOX_SIZE * 0.25, CHECK_BOX_SIZE * 0.5), 0, border_radius=int(CHECK_BOX_SIZE[0]))
            pygame.draw.circle(self.check_surface, COLOR_TOGGLE_HANDLE_ON, pos, CHECK_BOX_SIZE[1] * 0.5)
        else:
            pygame.draw.rect(self.check_surface, COLOR_TOGGLE_BACK_OFF, (CHECK_BOX_SIZE * 0.25, CHECK_BOX_SIZE * 0.5), 0, border_radius=int(CHECK_BOX_SIZE[0]))
            pygame.draw.circle(self.check_surface, COLOR_TOGGLE_HANDLE_OFF, pos, CHECK_BOX_SIZE[1] * 0.5)

    def draw(self, win: pygame.Surface) -> None:
        self.redraw()
        win.blit(self.check_surface, self.pos)



class ToggleButton(Button):
    def __init__(self, text: str, toggle: bool=False, **kwargs):
        self.is_toggled = toggle
        self.check_surface = pygame.Surface(CHECK_BOX_SIZE, pygame.SRCALPHA)
        self.check_element = ToggleElement(toggle)
        layout = [[self.check_element, Label(text)]]
        super().__init__(text, layout, **kwargs)

    def get_value(self):
        return self.is_toggled

    def update(self, value: str) -> None:
        self.is_toggled = value
        self.check_element.is_toggled = value

    def handle_event(self, event):
        output_event = super().handle_event(event)
        if output_event is not None:
            if self.is_hovered:
                self.check_element.is_toggled = self.is_toggled
                self.is_toggled = not self.is_toggled
                self.check_element.is_toggled = self.is_toggled
                output_event = GuiEvent(GuiEventType.TOGGLE_BUTTON_CLICK, {'key': self.key})
        self.check_element.is_hovered = self.is_hovered
        return output_event
    
    def draw(self, win: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(win)



class Textbox(GuiElement):
    def __init__(self, initial_text: str="", width: int=200, **kwargs):
        super().__init__(**kwargs)
        self.text = initial_text
        self.cursor_pos = len(self.text)
        self.selection_start = self.cursor_pos
        self.selection_end = self.cursor_pos
        self.is_focused = False
        self.cursor_blink_timer = 0
        self.width = width
        self.height = 30  # Fixed height for now
        self.font = None
        self.scroll_x = 0

    def initialize(self, assets: GuiAssets) -> None:
        self.font = assets.font

    def get_size(self) -> Vector2:
        return Vector2(self.width, self.height)

    def get_cursor_index_from_pos(self, mouse_x: int) -> int:
        # Calculate cursor position from mouse x
        for i in range(len(self.text) + 1):
            text_width = self.font.size(self.text[:i])[0]
            if text_width > mouse_x - self.pos.x + self.scroll_x:
                return max(0, i - 1)
        return len(self.text)

    def handle_event(self, event) -> GuiEvent:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = Vector2(event.pos)
            rect = pygame.Rect(self.pos, self.get_size())
            if rect.collidepoint(mouse_pos):
                self.is_focused = True
                self.cursor_pos = self.get_cursor_index_from_pos(mouse_pos.x)
                self.selection_start = self.cursor_pos
                self.selection_end = self.cursor_pos
                self.cursor_blink_timer = 0
            else:
                self.is_focused = False

        if not self.is_focused:
            return None

        if event.type == pygame.TEXTINPUT:
            # Insert text at cursor
            self.text = self.text[:self.cursor_pos] + event.text + self.text[self.cursor_pos:]
            self.cursor_pos += len(event.text)
            self.selection_start = self.cursor_pos
            self.selection_end = self.cursor_pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.selection_start != self.selection_end:
                    # Delete selection
                    start = min(self.selection_start, self.selection_end)
                    end = max(self.selection_start, self.selection_end)
                    self.text = self.text[:start] + self.text[end:]
                    self.cursor_pos = start
                elif self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                self.selection_start = self.cursor_pos
                self.selection_end = self.cursor_pos
            elif event.key == pygame.K_DELETE:
                if self.selection_start != self.selection_end:
                    start = min(self.selection_start, self.selection_end)
                    end = max(self.selection_start, self.selection_end)
                    self.text = self.text[:start] + self.text[end:]
                    self.cursor_pos = start
                elif self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                self.selection_start = self.cursor_pos
                self.selection_end = self.cursor_pos
            elif event.key == pygame.K_LEFT:
                if event.mod & pygame.KMOD_SHIFT:
                    if self.cursor_pos > 0:
                        self.cursor_pos -= 1
                    self.selection_end = self.cursor_pos
                else:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                    self.selection_start = self.cursor_pos
                    self.selection_end = self.cursor_pos
            elif event.key == pygame.K_RIGHT:
                if event.mod & pygame.KMOD_SHIFT:
                    if self.cursor_pos < len(self.text):
                        self.cursor_pos += 1
                    self.selection_end = self.cursor_pos
                else:
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                    self.selection_start = self.cursor_pos
                    self.selection_end = self.cursor_pos
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
                if not (event.mod & pygame.KMOD_SHIFT):
                    self.selection_start = self.cursor_pos
                self.selection_end = self.cursor_pos
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                if not (event.mod & pygame.KMOD_SHIFT):
                    self.selection_start = self.cursor_pos
                self.selection_end = self.cursor_pos
            elif event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                self.selection_start = 0
                self.selection_end = len(self.text)
                self.cursor_pos = len(self.text)
            self.cursor_blink_timer = 0

        return None

    def step(self) -> None:
        self.cursor_blink_timer += 1

    def get_value(self):
        return self.text
    
    def update(self, value: str) -> None:
        self.text = value
        self.cursor_pos = len(self.text)
        self.selection_start = self.cursor_pos
        self.selection_end = self.cursor_pos

    def draw(self, win: pygame.Surface) -> None:
        # Draw background
        back_color = COLOR_BACKGROUND if not self.is_focused else COLOR_TEXTBOX_BG_FOCUSED
        pygame.draw.rect(win, back_color, (self.pos, self.get_size()))

        # Draw border
        pygame.draw.rect(win, COLOR_LABEL, (self.pos, self.get_size()), 1)

        # Draw text
        text_surf = self.font.render(self.text, True, COLOR_LABEL)
        text_rect = text_surf.get_rect()
        text_rect.left = self.pos.x + margin - self.scroll_x
        text_rect.centery = self.pos.y + self.height / 2

        if self.is_focused:
            # Draw selection
            if self.selection_start != self.selection_end:
                start = min(self.selection_start, self.selection_end)
                end = max(self.selection_start, self.selection_end)
                start_x = self.font.size(self.text[:start])[0] - self.scroll_x + self.pos.x + margin
                end_x = self.font.size(self.text[:end])[0] - self.scroll_x + self.pos.x + margin
                pygame.draw.rect(win, COLOR_SELECTED, (start_x, self.pos.y + margin, end_x - start_x, self.height - 2 * margin))

            # Draw cursor
            if self.cursor_blink_timer % 60 < 30:  # Blink every 30 frames
                cursor_x = self.font.size(self.text[:self.cursor_pos])[0] - self.scroll_x + self.pos.x + margin
                pygame.draw.line(win, COLOR_LABEL, (cursor_x, self.pos.y + margin), (cursor_x, self.pos.y + self.height - margin))

        # Clip text to textbox
        clip_rect = pygame.Rect(self.pos.x + margin, self.pos.y, self.width - 2 * margin, self.height)
        win.set_clip(clip_rect)
        win.blit(text_surf, text_rect)
        win.set_clip(None)

        