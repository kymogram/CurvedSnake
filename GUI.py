from tkinter import *
from random import randint, random
from math import cos, sin, pi

from Snake import Snake

class GUI:
    DEFAULT_REFRESH_TIMER = 25
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre.geometry('480x480')
        self.canvas = Canvas(self.fenetre, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        self.snake = Snake(self.canvas, randint(0, 480),
                           randint(0, 480), random()*2*pi)
        self.refresh()
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)
    
    def refresh(self):
        self.snake.move()
        self.current_loop = self.fenetre.after(self.timer, self.refresh)
    
    def keyPressed(self, e):
        touche = e.keysym
        if touche in ('Right', 'Left'):
            self.snake.angle += 0.15 * {'Right': 1, 'Left': -1}[touche]
        elif touche == 'q':
            self.fenetre.after_cancel(self.current_loop)
        # self.snake.move()
    
    def start(self):
        self.fenetre.mainloop()

if __name__ == '__main__':
    GUI().start()