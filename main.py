# BUG: When launching on laptop (Ubuntu), the screen starts not rendered until slider update 
# BUG: Crashes on Raspberian

# Import error handling
from os import system
__found_pygame = False
__found_pygame_widgets = False
try:
    import pygame as PYGAME
    __found_pygame = True
except ModuleNotFoundError: pass
try:
    import pygame_widgets
    __found_pygame_widgets = True
except ModuleNotFoundError: pass
if not __found_pygame or not __found_pygame_widgets:
    if input("Packages are missing. Would you like to install these automatically?  (y/n): ").lower() != 'y':
        exit()
if not __found_pygame: system('pip install pygame'); import pygame as PYGAME
if not __found_pygame_widgets: system('pip install pygame_widgets'); import pygame_widgets
del __found_pygame, __found_pygame_widgets, system

import math
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from classes.pi import PiFromPolygons as CreatePolygon

class Window():
    def __init__(self):
        self.NUM_OF_SHAPES = 2121 # 2121 needed for 6 point precision
        self.POLYGONS = [CreatePolygon(i) for i in range(3, self.NUM_OF_SHAPES+1)] # List of all polygons and verticies
        self.PRIMARY_COLOUR = ((159, 175, 189)) # (r,b,g)
        self.INNER_COLOUR = (89,197,219)
        self.OUTER_COLOUR = (74,104,188)
        self.CIRCLE_COLOUR = (0,0,0)
        self.LINE_WIDTH = 3
        PYGAME.init()
        self.WINDOW = PYGAME.display.set_mode((0,0),PYGAME.FULLSCREEN)
        self.SCREEN_SIZE = self.WINDOW.get_size() # Assumes the user will not change the size of the window
        self.CENTER = (self.SCREEN_SIZE[0]/2, self.SCREEN_SIZE[1]/2) # Center of the screen
        self.SCALE = round(self.SCREEN_SIZE[0]/8)
        self.WINDOW.fill(self.PRIMARY_COLOUR)
        self._old_slider_value = 0
        self._slider_value = 0

    def DrawUI(self):
        self.slider = Slider(
                    self.WINDOW,
                    round(self.SCREEN_SIZE[0]/40), # x
                    round(self.SCREEN_SIZE[1]-self.SCREEN_SIZE[1]/15), # y
                    round(self.SCREEN_SIZE[0]-self.SCREEN_SIZE[0]/20), # width
                    round(self.SCREEN_SIZE[1]/20), # height
                    min=0,
                    max=self.NUM_OF_SHAPES-3,
                    step=1,
                    initial=0
                )
        self.label_names_box = TextBox(
                    self.WINDOW,
                    round(self.CENTER[0]-self.CENTER[0]/7),
                    0,
                    round(self.SCREEN_SIZE[0]/7),
                    round(self.SCREEN_SIZE[1]/30),
                    fontSize=round(self.SCREEN_SIZE[0]/60)
                )
        self.inbtween_values_box = TextBox(
                    self.WINDOW,
                    round(self.CENTER[0]-self.CENTER[0]/7.75),
                    round(self.SCREEN_SIZE[1]/30),
                    round(self.SCREEN_SIZE[0]/7.75),
                    round(self.SCREEN_SIZE[1]/30),
                    fontSize=round(self.SCREEN_SIZE[0]/64)
                )
        self.pi_average_box = TextBox(
                    self.WINDOW,
                    round(self.CENTER[0]-self.CENTER[0]/10),
                    round(self.SCREEN_SIZE[1]/15),
                    self.SCREEN_SIZE[0]/10,
                    self.SCREEN_SIZE[1]/30,
                    fontSize=round(self.SCREEN_SIZE[0]/64)
                )
        self.side_amount_output_box = TextBox(
                    self.WINDOW,
                    self.CENTER[0]-self.CENTER[1]/30,
                    self.SCREEN_SIZE[1]-self.SCREEN_SIZE[1]/9,
                    self.SCREEN_SIZE[0]/30,
                    self.SCREEN_SIZE[1]/30,
                    fontSize=round(self.SCREEN_SIZE[0]/64)
                )
        self.radius_box = TextBox(
                    self.WINDOW,
                    self.CENTER[0]+self.CENTER[0]/15,
                    self.CENTER[1]+self.CENTER[1]/100,
                    self.SCREEN_SIZE[0]/30,
                    self.SCREEN_SIZE[1]/40,
                    fontSize=round(self.SCREEN_SIZE[0]/76)
                )
        self.theta_box = TextBox(
                    self.WINDOW,
                    self.CENTER[0]-self.CENTER[0]/10,
                    self.CENTER[1]-self.CENTER[1]/50,
                    self.SCREEN_SIZE[0]/23,
                    self.SCREEN_SIZE[0]/70,
                    fontSize=round(self.SCREEN_SIZE[0]/76)
                )
        
        self.label_names_box.disable() # Act as label instead of textbox
        self.inbtween_values_box.disable()
        self.pi_average_box.disable()
        self.side_amount_output_box.disable() 
        self.radius_box.disable()
        self.theta_box.disable()
        
        self.DrawShapes()

    def DrawShapes(self):
        self.WINDOW.fill(self.PRIMARY_COLOUR)
        self.active_polygon_index = 0 if self._slider_value == 0 else round(self._slider_value ** (self._slider_value/(self.NUM_OF_SHAPES-3)))
        self.active_polygons = self.POLYGONS[self.active_polygon_index]

        self.adjusted_vertices = [
        [
            [
                self.CENTER[i] + self.SCALE * vertex[i] for i in range(2)
            ]
            for vertex in polygon.vertices
        ]
        for polygon in [self.active_polygons._interior_polygon, self.active_polygons._exterior_polygon]
        ]
        
        # Drawing objects
        PYGAME.draw.circle( # Main circle
                        self.WINDOW, # Surface
                        self.CIRCLE_COLOUR, # Colour
                        self.CENTER, # Cords
                        self.SCALE, # Scale
                        self.LINE_WIDTH # Line Width
                    )
        PYGAME.draw.circle( # Center dot
                        self.WINDOW,
                        self.CIRCLE_COLOUR,
                        self.CENTER,
                        self.SCALE,
                        1 
                    )
        PYGAME.draw.line( # Radius
                        self.WINDOW,
                        self.CIRCLE_COLOUR,
                        self.CENTER,
                        (self.CENTER[0]+self.SCALE,self.CENTER[1]),
                        self.LINE_WIDTH
                    )
        PYGAME.draw.line( # Line to form inner triangle
                        self.WINDOW,
                        self.INNER_COLOUR,
                        self.CENTER,
                        ((self.adjusted_vertices[0][-1][0]+self.adjusted_vertices[0][0][0])/2,(self.adjusted_vertices[0][-1][1]+self.adjusted_vertices[0][0][1])/2),
                        self.LINE_WIDTH
                    )
        PYGAME.draw.arc( # Theta angle
                        self.WINDOW,
                        self.INNER_COLOUR,
                        (bounding_box := ([i-self.SCALE/12 for i in self.CENTER], [self.SCALE/6,self.SCALE/6])),
                        0,
                        math.radians(180/(self.active_polygon_index+3)),
                        round(self.LINE_WIDTH/2)
                    )
        # PYGAME.draw.rect( # Theta angle bounding box
        #                 self.WINDOW,
        #                 self.INNER_COLOUR,
        #                 bounding_box,
        #                 1
        #             )
        PYGAME.draw.polygon( # Inner polygon
                        self.WINDOW, # Surface
                        self.INNER_COLOUR, # Colour
                        self.adjusted_vertices[0], # Verticies of points
                        self.LINE_WIDTH # Line Width
                    )
        PYGAME.draw.polygon( # Outer polygon
                        self.WINDOW,
                        self.OUTER_COLOUR,
                        self.adjusted_vertices[1],
                        self.LINE_WIDTH
                    )

        self.label_names_box.setText(f"Inner Area      Outer Area")
        self.inbtween_values_box.setText(f"{format(round(self.active_polygons._interior_polygon.area, 6),'.6f')} < π < {format(round(self.active_polygons._exterior_polygon.area, 6), '.6f')}")
        self.pi_average_box.setText(f"Average: {format(self.active_polygons.pi,'.6f')}")
        self.side_amount_output_box.setText(f"{str(self.active_polygon_index + 3).rjust(4)}")
        self.radius_box.setText(f"r = 1")
        self.theta_box.setText(f'θ = {round(180/(self.active_polygon_index+3),2)}')
        self._old_slider_value = self._slider_value

    def start(self):
        self.DrawUI()
        while True:
            events = PYGAME.event.get()
            for event in events:
                if event.type == PYGAME.QUIT:
                    PYGAME.quit()
                    exit()
            
            self._slider_value = self.slider.getValue()
            if self._slider_value != self._old_slider_value:
                self.DrawShapes()

            pygame_widgets.update(events)
            PYGAME.display.update()

if __name__ == "__main__":
    gui = Window()
    gui.start()