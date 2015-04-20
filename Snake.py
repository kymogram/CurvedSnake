DEFAULT_SPEED = 2
DEFAULT_THICKNESS = 4

from math import cos, sin, pi

class Snake:
    def __init__(self, canvas, x_head, y_head, angle, speed=DEFAULT_SPEED,
                                                thickness=DEFAULT_THICKNESS):
        #list and not tuple because tuples can't be modified
        self.head_coord = [x_head, y_head]
        self.speed = speed
        self.angle = angle #radians!
        self.canvas = canvas
        self.thickness = thickness
        self.move()
        # self.head_id = self.canvas.create_rectangle(
                        # x_head - thickness, y_head - thickness,
                        # x_head + thickness, y_head + thickness, fill='white')
    
    def move(self):
        x, y = self.head_coord
        x += self.speed * cos(self.angle)
        y += self.speed * sin(self.angle)
        self.head_coord = [x, y]
        r = self.thickness // 2
        self.canvas.create_rectangle(x-r, y-r, x+r, y+r, fill='white', outline='white')
        # self.canvas.coords(self.head_id, x-r, y-r, x+r, y+r)