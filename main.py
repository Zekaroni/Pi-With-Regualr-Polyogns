import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from classes.pi import PiFromPolygons as pi

pygame.init()
win = pygame.display.set_mode((1000, 600))

slider = Slider(win, 100, 500, 800, 40, min=0, max=10, step=1)
output = TextBox(win, 475, 550, 50, 50, fontSize=30)

output.disable()  # Act as label instead of textbox

P = [pi(i) for i in range(3, 100)]

center = (300, 250)
scale = 150

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    p = P[slider.getValue()]

    adjusted_vertices = [
        [
            [
                center[i] + scale * vertex[i] for i in range(2)
            ]
            for vertex in polygon.vertices
        ]
        for polygon in [p._interior_polygon, p._exterior_polygon]
    ]

    # circle
    pygame.draw.circle(win, (0, 0, 0), (300, 250), 150, 3)
    pygame.draw.polygon(win, (0, 0, 0), adjusted_vertices[0], 3)
    pygame.draw.polygon(win, (0, 0, 0), adjusted_vertices[1], 3)

    output.setText(slider.getValue() + 3)

    pygame_widgets.update(events)
    pygame.display.update()
