from math import cos, pi, radians, sin, sqrt

class RegularPolygon:
    def __init__(self, num_sides, x, y):
        self._num_sides = num_sides
        self._vertices = [(x, y)]

    @property
    def area(self):
        x, y = self._vertices[0]
        hyp = sqrt(x ** 2 + y ** 2)
        angle = pi / self._num_sides
        area = self._num_sides * (hyp ** 2) * sin(angle) * cos(angle)
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
        angle = radians(angle)
        rotated_x = cos(angle) * x - sin(angle) * y
        rotated_y = sin(angle) * x + cos(angle) * y
        return rotated_x, rotated_y
