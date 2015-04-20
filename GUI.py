from tkinter import *
from random import randint
from math import cos,sin,pi

class GUI:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.geometry('480x480')
        self.canva = Canvas(self.fenetre, bg='black',highlightthickness=0)
        self.canva.pack(fill='both',expand=1)

        self.w = 8
        self.createSnakeHead(randint(0,480),randint(0,480))
        self.canva.focus_set()
        self.canva.bind("<Key>", self.turning)
        self.fenetre.mainloop()

    def createSnakeHead(self,x,y):
        self.pos = [x,y]
        self.direction = randint(0,360)
        r = self.w//2
        self.head = self.canva.create_rectangle(x-r,y-r,x+r,y+r,fill='white')

        self.goDirection(self.head, 90, 4)

    def goDirection(self, obj, direction=0, speed=0):
        x,y = self.pos
        dir_rad = direction*pi/180
        x += speed*cos(dir_rad)
        y += speed*sin(dir_rad) 
        self.pos = [x,y]
        r = self.w//2
        self.canva.coords(obj,x-r,y-r,x+r,y+r)
        #y_dep = obj['y']

    def turning(self,e):
        touche = e.keysym

        if touche == "Up":
            self.goDirection(self.head,self.direction,4)
        if touche == "Right":
            self.direction += 10
            self.goDirection(self.head,self.direction,4)
        elif touche == "Left":
            self.direction -= 10
            self.goDirection(self.head,self.direction,4)


if __name__ == '__main__':
    GUI()