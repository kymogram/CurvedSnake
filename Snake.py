DEFAULT_SPEED = 3
DEFAULT_THICKNESS = 4

from math import cos, sin, pi

class Snake:
    def __init__(self, canvas, x_head, y_head, angle, color='white',
                            speed=DEFAULT_SPEED, thickness=DEFAULT_THICKNESS):
        #list and not tuple because tuples can't be modified
        self.head_coord = [x_head, y_head]
        self.speed = speed
        self.angle = angle #radians!
        self.canvas = canvas
        self.thickness = thickness
        self.color = color
        self.alive = True
    
    def isCollision(self, collisions, step):
        res = False
        if len(collisions) != 0:
            first_elem = int(collisions[0])
            appearance_step = int(self.canvas.gettags(first_elem)[0])
            if appearance_step < step-self.thickness:
                res = True
        return res
    
    def isInScreen(self, x, y):
        self.canvas.update()
        return 0 <= x < self.canvas.winfo_width() and \
               0 <= y < self.canvas.winfo_height()
    
    def isOutOfScreen(self, x, y):
        return not self.isInScreen(x, y)
    
    def move(self, step):
        #stop moving if snake is dead
        if not self.alive:
            return
        #step is used to handle collisions
        if not isinstance(step, int):
            #if it is under form 'after#{}', remove 'after#'
            step = int(step[step.find('#')+1:])
        #find new coordinates
        x, y = self.head_coord
        x += self.speed * cos(self.angle)
        y += self.speed * sin(self.angle)
        #update head_coord
        self.head_coord = [x, y]
        #radius of oval
        r = self.thickness // 2
        #find all items in contact with new position
        collisions = self.canvas.find_overlapping(x-r, y-r, x+r, y+r)
        #if there is contact, snake is dead
        #WARNING: when the snake moves, it always touches its previous position
        #so step of appearance is written as a tag.
        if self.isCollision(collisions, step) or self.isOutOfScreen(*self.head_coord):
            self.alive = False
        self.canvas.create_rectangle(x-r, y-r, x+r, y+r, fill=self.color,
                                     outline=self.color, tag=str(step))
    #
