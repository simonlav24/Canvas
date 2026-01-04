
from typing import Protocol
from enum import Enum

import pygame
from pygame import Vector2

from world_canvas.transformation import Transformation
from world_canvas.viewport import Viewport
from world_canvas.handle import Selectable


class SelectToolMode(Enum):
    HANDLE = 0
    ELEMENT = 1

class EditTool:
    """Base class for editor tools using State pattern"""
    def __init__(self, context: Viewport):
        self.viewport = context

    def handle_mouse_down(self, event) -> 'EditTool':
        """Handles mouse button down event"""
        return self

    def handle_mouse_up(self, event) -> 'EditTool':
        """Handles mouse button up event"""
        return self

    def handle_mouse_motion(self, event) -> 'EditTool':
        """Handles mouse motion event"""
        return self

    def handle_key_down(self, event) -> 'EditTool':
        """Handles key down event"""
        return self

    def handle_key_up(self, event) -> 'EditTool':
        """Handles key up event"""
        return self

    def step(self) -> None:
        """Updates tool state each frame"""
        ...

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        """Draws tool-specific overlays"""
        ...

class SelectTool(EditTool):
    """Default tool state for hovering and detection handles"""
    def __init__(self, viewport: Viewport):
        super().__init__(viewport)
        self.clicked_on_empty_space = False
        self.hovered: Selectable = None
        self.mode = SelectToolMode.HANDLE

    def handle_mouse_down(self, event) -> 'EditTool':
        """Determines next tool based on what was clicked"""
        self.clicked_on_empty_space = False
        next_tool = self

        if self.hovered:
            next_tool = DragElementTool(self.viewport, self.hovered)
        
        else:
            # click in empty space
            self.clicked_on_empty_space = True
            next_tool = HandTool(self.viewport)

        return next_tool

    def step(self):
        """Updates hover detection each frame"""
        mouse_in_world = self.viewport.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos()))).pos
        if self.mode == SelectToolMode.HANDLE:
            self.hovered = self.viewport.get_handle_at(mouse_in_world)
        else:
            self.hovered = self.viewport.get_element_at(mouse_in_world)

    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        if self.mode == SelectToolMode.HANDLE and self.hovered:
            self.hovered.draw(win, transform)



class DragElementTool(EditTool):
    """Handles dragging of single or multiple handles"""
    def __init__(self, viewport, main_element: Selectable):
        super().__init__(viewport)
        self.main_element = main_element
        mouse_pos = self.viewport.world_transform.transform_back(Transformation(Vector2(pygame.mouse.get_pos())))
        self.drag_offset = mouse_pos.pos - self.main_element.transformation.pos

    def handle_mouse_motion(self, event):
        """Updates positions maintaining relative offsets"""
        pos = self.viewport.world_transform.transform_back(Transformation(Vector2(event.pos))).pos

        self.main_element.transformation.pos = Vector2(pos - self.drag_offset)
        return self

    def handle_mouse_up(self, event):
        """Completes drag and returns to idle"""
        return SelectTool(self.viewport)


class HandTool(EditTool):
    """Handles canvas panning"""
    def __init__(self, context):
        super().__init__(context)

    def handle_mouse_motion(self, event):
        """Pans the canvas"""
        self.viewport.world_transform.pos -= Vector2(event.rel) * 1 / self.viewport.world_transform.scale
        return self

    def handle_mouse_up(self, event):
        """stop panning"""
        return SelectTool(self.viewport)
