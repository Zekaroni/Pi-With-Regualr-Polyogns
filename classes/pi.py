from polygon import RegularPolygon

class PiFromPolygons:
    def __init__(self):
        pass
    
    @property
    def interior_polygon(self):
        return 'RegularPolygon object for interior'

    @property
    def exterior_polygon(self):
        return 'RegularPolygon object for exterior'
    
    @property
    def pi(self):
        return 'pi approximation'
