
from dataclasses import dataclass

from pygame import Vector2


@dataclass
class Transformation:
    pos: Vector2
    scale: float = 1.0

    def transform(self, transformation: 'Transformation') -> 'Transformation':
        return Transformation((transformation.pos - self.pos) * self.scale, self.scale * transformation.scale)
    
    def transform_back(self, transformation: 'Transformation') -> 'Transformation':
        return Transformation(transformation.pos / self.scale + self.pos, transformation.scale / self.scale)
