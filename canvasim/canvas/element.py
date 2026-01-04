
from dataclasses import dataclass, field

import pygame
from pygame import Vector2

from .transformation import Transformation
from . import world_globals
from .handle import Handle



class Element:
    def __init__(self):
        self.transformation = Transformation(Vector2())
        self.handles: list[Handle] = []
    
    def draw(self, win: pygame.Surface, transform: Transformation) -> None:
        ...

    def hit_test(self, world_pos: Vector2) -> bool:
        ...



@dataclass
class Database:
    elements: list[Element] = field(default_factory=list)


class TokenElement(Element):
    def __init__(self, surf: pygame.Surface):
        super().__init__()
        self.surf = surf
        self.handles.append(Handle(self.transformation, max(*self.surf.get_size()) / 2, self))
    
    def hit_test(self, world_pos):
        return self.handles[0].hit_test(world_pos)

    def draw(self, win: pygame.Surface, world_transform: Transformation) -> None:
        # Combine element's transform with world transform
        screen_transform = world_transform.transform(self.transformation)
        
        # Calculate scaled size
        surf_width, surf_height = self.surf.get_size()
        scaled_width = int(surf_width * screen_transform.scale)
        scaled_height = int(surf_height * screen_transform.scale)
        
        if scaled_width <= 0 or scaled_height <= 0:
            return
        
        # Scale the surface
        scaled_surf = pygame.transform.scale(self.surf, (scaled_width, scaled_height))
        
        # Draw centered on the position
        draw_pos = screen_transform.pos - Vector2(scaled_width / 2, scaled_height / 2)
        
        win.blit(scaled_surf, draw_pos)
        # for handle in self.handles:
        #     handle.draw(win, world_transform)


class RectanglarSurfElement(Element):
    def __init__(self, surf: pygame.Surface):
        super().__init__()
        self.surf = surf
        # Cache
        self._cached_surf: pygame.Surface = None
        self._cached_draw_pos: Vector2 = None
        self._cached_world_transform: Transformation = None

    def _needs_recalculation(self, world_transform: Transformation) -> bool:
        """Check if the cached surface needs to be recalculated."""
        if self._cached_surf is None or self._cached_world_transform is None:
            return True
        return (self._cached_world_transform.pos != world_transform.pos or
                self._cached_world_transform.scale != world_transform.scale)

    def _calculate_visible_region(self, world_transform: Transformation) -> tuple:
        """
        Calculate the visible region of the surface.
        Returns (src_rect, dest_size, draw_pos) or None if nothing is visible.
        """
        elem_world_pos = self.transformation.pos
        surf_width, surf_height = self.surf.get_size()
        
        # Calculate the element's screen position (top-left corner)
        screen_pos = (elem_world_pos - world_transform.pos) * world_transform.scale
        
        # Calculate scaled dimensions
        scaled_width = surf_width * world_transform.scale
        scaled_height = surf_height * world_transform.scale
        
        # Calculate visible region in screen coordinates
        visible_left = max(0, -screen_pos.x)
        visible_top = max(0, -screen_pos.y)
        visible_right = min(scaled_width, world_globals.win_width - screen_pos.x)
        visible_bottom = min(scaled_height, world_globals.win_height - screen_pos.y)
        
        # Check if any part is visible
        if visible_left >= visible_right or visible_top >= visible_bottom:
            return None
        
        # Convert visible screen region back to source surface coordinates
        src_left = int(visible_left / world_transform.scale)
        src_top = int(visible_top / world_transform.scale)
        src_right = int(visible_right / world_transform.scale)
        src_bottom = int(visible_bottom / world_transform.scale)
        
        # Clamp to surface bounds
        src_left = max(0, min(src_left, surf_width))
        src_top = max(0, min(src_top, surf_height))
        src_right = max(0, min(src_right, surf_width))
        src_bottom = max(0, min(src_bottom, surf_height))
        
        src_width = src_right - src_left
        src_height = src_bottom - src_top
        
        if src_width <= 0 or src_height <= 0:
            return None
        
        # Calculate the destination size for the visible portion
        dest_width = int(src_width * world_transform.scale)
        dest_height = int(src_height * world_transform.scale)
        
        if dest_width <= 0 or dest_height <= 0:
            return None
        
        src_rect = (src_left, src_top, src_width, src_height)
        dest_size = (dest_width, dest_height)
        draw_pos = Vector2(screen_pos.x + visible_left, screen_pos.y + visible_top)
        
        return src_rect, dest_size, draw_pos

    def _update_cache(self, world_transform: Transformation) -> bool:
        """
        Update the cached surface if needed.
        Returns True if there's something to draw, False otherwise.
        """
        result = self._calculate_visible_region(world_transform)
        
        if result is None:
            self._cached_surf = None
            self._cached_world_transform = None
            return False
        
        src_rect, dest_size, draw_pos = result
        
        # Extract and scale the visible portion
        visible_subsurface = self.surf.subsurface(src_rect)
        self._cached_surf = pygame.transform.scale(visible_subsurface, dest_size)
        self._cached_draw_pos = draw_pos
        self._cached_world_transform = Transformation(Vector2(world_transform.pos), world_transform.scale)
        
        return True

    def draw(self, win: pygame.Surface, world_transform: Transformation) -> None:
        if self._needs_recalculation(world_transform):
            if not self._update_cache(world_transform):
                return  # Nothing visible
        
        win.blit(self._cached_surf, self._cached_draw_pos)

