from tkinter import *
from math import cos, sin, pi

class Arc:
    '''
        the Arc class is used to be placed around snake's head to show
        the remaining time before bonus effect is down
    '''

    def __init__(self, snake, length, offset, color='pink'):
        # val is current evolution in bonus time
        self.val = 0
        # max is upper limit (when arc must be destroyed)
        self.max = length
        # must keep a link to snake
        self.snake = snake
        # offset is distance between head and arc
        self.offset = offset
        x, y = self.snake.head_coord
        # r stands for radius of arc
        r = (self.snake.thickness + 2*self.offset) * 2
        # create arc which will be edited at each update
        precision = 20
        step = 0.15
        angle = 2*pi*(1-self.val/self.max)
        for i in range(0,int(angle*precision), int(step*precision)):
            i /= precision
            self.arc_id = self.snake.canvas.create_line(x+r*cos(i),
                                                        y-r*sin(i),
                                                        x+r*cos(i+step),
                                                        y-r*sin(i+step),
                                                        width=2,
                                                        fill=color)

    def updateArc(self):
        # move one step further in bonus effect
        self.val += 1
        x, y = self.snake.head_coord
        r = (self.snake.thickness + 2*self.offset) * 2
        angle = 2*pi*(1-self.val/self.max)
        step = 0.15
        precision = 20
        # replace it correctly
        for i in range(0,int(angle*precision), int(step*precision)):
            i /= precision
            self.snake.canvas.coords(self.arc_id,
                                     x+r*cos(i),
                                     y-r*sin(i),
                                     x+r*cos(i+step),
                                     y-r*sin(i+step))
    
    def setOffset(self, new_offset):
        self.offset = new_offset

    def getOffset(self):
        return self.offset
