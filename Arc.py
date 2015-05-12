from tkinter import *

class Arc:
    '''
        the Arc class is used to be placed around snake's head to show
        the remaining time before bonus effect is down
    '''
    
    def __init__(self, snake, length, offset, color='pink'):
        #val is current evolution in bonus time
        self.val = 0
        #max is upper limit (when arc must be destroyed)
        self.max = length
        #must keep a link to snake
        self.snake = snake
        #offset is distance between head and arc
        self.offset = offset
        x, y = self.snake.head_coord
        #r stands for radius of arc
        r = (self.snake.thickness + 2*self.offset) * 2
        #create arc which will be edited at each update
        self.arc_id = self.snake.canvas.create_arc(x-r, y-r, x+r, y+r,
                                                   style=ARC, extent=360,
                                                   width=2, outline=color)
    
    def updateArc(self):
        #move one step further in bonus effect
        self.val += 1
        #change angle of arc
        self.snake.canvas.itemconfig(self.arc_id, extent=360*(1-(self.val/self.max)))
        x, y = self.snake.head_coord
        r = (self.snake.thickness + 2*self.offset) * 2
        #replace it correctly
        self.snake.canvas.coords(self.arc_id, x-r, y-r, x+r, y+r)
    
    def setOffset(self, new_offset):
        self.offset = new_offset
    
    def getOffset(self):
        return self.offset
    
    #
