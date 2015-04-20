DEFAULT_SPEED = 4
DEFAULT_THICKNESS = 8

from math import cos, sin, pi

class Snake:
    def __init__(self, canvas, x_head, y_head, angle, speed=DEFAULT_SPEED, thickness=DEFAULT_THICKNESS):
        #list and not tuple because tuples can't be modified
        self.head_coord = [x_head, y_head]
        self.speed = speed
        self.angle = angle #radians!
        self.canvas = canvas
        self.thickness = thickness
        self.head_id = self.canvas.create_rectangle(x_head - thickness,
                                                    y_head - thickness,
                                                    x_head + thickness,
                                                    y_head + thickness,
                                                    fill='white')
    
    def move(self):
        x, y = self.head_coord
        x += self.speed * cos(self.angle)
        y += self.speed * sin(self.angle)
        self.head_coord = [x, y]
        radius = self.thickness // 2
        self.canvas.coords(self.head_id, x-radius, y-radius, x+radius, y+radius)