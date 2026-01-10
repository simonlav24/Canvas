
import pygame
from pygame import Vector2

from .gui_element import GuiElement, GuiAssets, GuiEvent
from .gui_globals import *


class Textbox(GuiElement):
    def __init__(self, initial_text: str="", width: int=200, **kwargs):
        super().__init__(**kwargs)
        self.text = str(initial_text)
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

        