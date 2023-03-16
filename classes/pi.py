from math import pi, tan
from classes.polygon import RegularPolygon


class PiFromPolygons:
    def __init__(self, num_sides):
        self._num_sides = num_sides
        self._interior_polygon = RegularPolygon(num_sides, 1, 0)
        self._exterior_polygon = RegularPolygon(num_sides, 1, tan(pi / num_sides))
    
    @property
    def pi(self):
        return (self._interior_polygon.area + self._exterior_polygon.area) / 2
