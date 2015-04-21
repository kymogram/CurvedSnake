from tkinter import *
from random import randint, random
from math import cos, sin, pi
from tkinter import Toplevel

from Snake import Snake

class GUI:
    DEFAULT_REFRESH_TIMER = 25
    def __init__(self):
        self.window = Tk()
        self.window.geometry('480x480')
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        self.menuStart()
        self.window.mainloop()
    
    def refresh(self):
        self.snake.move()
        self.current_loop = self.window.after(self.timer, self.refresh)
    
    def keyPressed(self, e):
        touche = e.keysym
        if touche in ('Right', 'Left'):
            self.snake.angle += 0.15 * {'Right': 1, 'Left': -1}[touche]
        elif touche == 'q':
            self.window.after_cancel(self.current_loop)
        
    def menuStart(self):
        Label(self.window, width=100, text='Curved Snake').pack()
        playButton = Button(self.window, text='Play!', command=self.playPressed).pack()
    
    def playPressed(self):
        for child in self.window.winfo_children():
            child.pack_forget()
        self.play()
    
    def play(self):
        self.canvas = Canvas(self.window, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        
        self.snake = Snake(self.canvas, randint(0, 480),
                           randint(0, 480), random()*2*pi)
        self.refresh()
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)

if __name__ == '__main__':
    GUI()
