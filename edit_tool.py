
from typing import Protocol

import pygame
from pygame import Vector2


class Context(Protocol):
    ...


class EditTool:
    """Base class for editor tools using State pattern"""
    def __init__(self, context: Context):
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

    def draw(self, win: pygame.Surface) -> None:
        """Draws tool-specific overlays"""
        ...


class IdleTool(EditTool):
    """Default tool state for hovering and detection"""
    def __init__(self, viewport: Context):
        super().__init__(viewport)
        self.clicked_on_empty_space = False

    def handle_mouse_down(self, event) -> 'EditTool':
        """Determines next tool based on what was clicked"""
        self.clicked_on_empty_space = False
        next_tool = self

        if False:
            # check for elements
            ...
        
        else:
            # click in empty space
            self.clicked_on_empty_space = True
            next_tool = HandTool(self.viewport)

        return next_tool

    def step(self):
        """Updates hover detection each frame"""
        ...


class DragElementTool(EditTool):
    """Handles dragging of single or multiple nodes"""
    def __init__(self, viewport, main_element):
        super().__init__(viewport)
        self.main_element = main_element
        mouse_pos = self.viewport.world_transform.transform_back(pygame.mouse.get_pos())
        self.drag_offset = mouse_pos - self.main_element.pos

    def handle_mouse_motion(self, event):
        """Updates node positions maintaining relative offsets"""
        pos = self.viewport.world_transform.transform_back(event.pos)

        for node in self.viewport.selected_elements:
            if node is self.main_element:
                continue
            node_to_main = node.pos - self.main_element.pos
            node.pos = Vector2(pos - self.drag_offset + node_to_main)

        self.main_element.pos = Vector2(pos - self.drag_offset)
        return self

    def handle_mouse_up(self, event):
        """Completes drag and returns to idle"""
        return IdleTool(self.viewport)


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
        return IdleTool(self.viewport)
