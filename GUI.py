from tkinter import *
from random import randint
from math import cos, sin, pi

from Snake import Snake

class GUI:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.geometry('480x480')
        self.canvas = Canvas(self.fenetre, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)

        self.w = 8
        self.createSnakeHead(randint(0, 480), randint(0, 480))
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.turning)

    def createSnakeHead(self,x,y):
        self.pos = [x, y]
        self.direction = randint(0,360)
        r = self.w//2
        self.head = self.canvas.create_rectangle(x-r, y-r, x+r, y+r,
                                                fill='white')

        self.goDirection(self.head, 90, 4)

    def goDirection(self, obj, direction=0, speed=0):
        x, y = self.pos
        dir_rad = direction*pi/180
        x += speed*cos(dir_rad)
        y += speed*sin(dir_rad) 
        self.pos = [x, y]
        r = self.w//2
        self.canvas.coords(obj, x-r, y-r, x+r, y+r)
        #y_dep = obj['y']

    def turning(self, e):
        touche = e.keysym
        if touche == 'Right':
            self.direction += 10
        elif touche == 'Left':
            self.direction -= 10
        self.goDirection(self.head, self.direction, 4)
    
    def mainloop(self):
        self.fenetre.mainloop()

if __name__ == '__main__':
    GUI().mainloop()