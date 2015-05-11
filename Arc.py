from tkinter import *

class Arc:
    def __init__(self, snake, length, offset, color='pink'):
        self.val = 0
        self.max = length
        self.snake = snake
        self.offset = offset
        x, y = self.snake.head_coord
        r = (self.snake.thickness + 2*self.offset) * 2
        angle = 360-(self.val/self.max) * 360
        self.arc_id = self.snake.canvas.create_arc(x-r, y-r, x+r, y+r,
                                                   style=ARC, extent=angle,
                                                   width=2, outline=color)
    
    def updateArc(self):
        if self.val < self.max:
            self.val += 1
            self.snake.canvas.itemconfig(self.arc_id, extent=360-(self.val/self.max) * 360)
            x, y = self.snake.head_coord
            r = (self.snake.thickness + 2*self.offset) * 2
            self.snake.canvas.coords(self.arc_id, x-r, y-r, x+r, y+r)