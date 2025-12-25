
import pygame
from pygame import Vector2

from world_canvas.transformation import Transformation
from world_canvas import world_globals

RULER_BACK_COLOR = (37, 37, 37)
RULER_TITLE_COLOR = (128, 128, 128)


def draw_axis(win: pygame.Surface, world_transform: Transformation) -> None:
    axis_center = world_transform.transform(Transformation(Vector2(0, 0)))
    axis_x = world_transform.transform(Transformation(Vector2(100, 0)))
    axis_y = world_transform.transform(Transformation(Vector2(0, 100)))

    pygame.draw.line(win, (255,0,0), axis_center.pos + Vector2(1, 0), axis_x.pos, 1)
    pygame.draw.line(win, (0,255,0), axis_center.pos + Vector2(0, 1), axis_y.pos, 1)


def draw_grid(win: pygame.Surface, world_transform: Transformation, base_grid_size: int = 100, draw_ruler: bool=True) -> None:
    # Adjust grid size based on zoom level
    # When zoomed in too much, increase grid size; when zoomed out, decrease it
    grid_size = base_grid_size
    screen_grid_size = grid_size * world_transform.scale
    
    # Keep screen grid size within a reasonable range (e.g., 50-200 pixels)
    while screen_grid_size < 50:
        grid_size *= 2
        screen_grid_size = grid_size * world_transform.scale
    while screen_grid_size > 200:
        grid_size /= 2
        screen_grid_size = grid_size * world_transform.scale
    
    # Calculate visible world bounds
    top_left_world = world_transform.pos
    bottom_right_world = world_transform.pos + Vector2(world_globals.win_width, world_globals.win_height) / world_transform.scale
    
    # Find the first grid line positions (snap to grid)
    start_x = (top_left_world.x // grid_size) * grid_size
    start_y = (top_left_world.y // grid_size) * grid_size
    
    # Draw vertical lines
    x = start_x
    while x <= bottom_right_world.x:
        screen_x = (x - world_transform.pos.x) * world_transform.scale
        pygame.draw.line(win, (60, 60, 60), (screen_x, 0), (screen_x, world_globals.win_height), 1)
        x += grid_size
    
    # Draw horizontal lines
    y = start_y
    while y <= bottom_right_world.y:
        screen_y = (y - world_transform.pos.y) * world_transform.scale
        pygame.draw.line(win, (60, 60, 60), (0, screen_y), (world_globals.win_width, screen_y), 1)
        y += grid_size

    # if draw_ruler:
    #     pygame.draw.rect(win, RULER_BACK_COLOR, ((0, 0), (world_globals.win_width, 16)))