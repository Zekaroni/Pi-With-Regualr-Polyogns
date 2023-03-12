import math

class RegularPolygon:
    def __init__(self, num_sides, x, y):
        self._num_sides = num_sides
        self._vertices = [(x, y)]
        pass

    @property
    def area(self):
        x, y = self._vertices[0]
        hyp = math.sqrt(x ** 2 + y ** 2)
        angle = math.pi / self._num_sides
        area = self._num_sides * (hyp ** 2) * math.sin(angle) * math.cos(angle)
        return area

    @property
    def vertices(self):
        if(len(self._vertices) == self._num_sides):
            return self._vertices
        angle_of_rotation = 360 / self._num_sides
        for i in range(1, self._num_sides):
            self._vertices.append(self.rotate(*self._vertices[0], angle_of_rotation * i))
        return self._vertices
        
    @staticmethod
    def rotate(x, y, angle):
        angle = math.radians(angle)
        rotated_x = math.cos(angle) * x - math.sin(angle) * y
        rotated_y = math.sin(angle) * x + math.cos(angle) * y
        return rotated_x, rotated_y
