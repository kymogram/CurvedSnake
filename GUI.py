from tkinter import *
from random import randint, random
from math import cos, sin, pi

from Snake import Snake

class GUI:
    DEFAULT_WIDTH = 480
    DEFAULT_HEIGHT = 480
    DEFAULT_SPAWN_OFFSET = 60
    DEFAULT_REFRESH_TIMER = 25
    def __init__(self):
        self.window = Tk()
        self.window.geometry('{}x{}'.format(GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT))
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        self.current_loop = 0
        self.menuStart()
        self.window.mainloop()
    
    def refresh(self):
        self.snake.move(self.current_loop)
        self.current_loop = self.window.after(self.timer, self.refresh)
    
    def keyPressed(self, e):
        touche = e.keysym
        if touche in ('Right', 'Left'):
            self.snake.angle += 0.15 * {'R': 1, 'L': -1}[touche[0]]
        elif touche.lower() == 'q':
            self.quitCurrentPlay()
    
    def quitCurrentPlay(self):
        self.window.after_cancel(self.current_loop)
        self.menuStart()
    
    def clearWindow(self):
        for child in self.window.winfo_children():
            child.pack_forget()
    
    def menuStart(self):
        self.clearWindow()
        Label(self.window, width=100, text='Curved Snake').pack()
        playButton = Button(self.window, text='Play!', command=self.playPressed).pack()
    
    def playPressed(self):
        self.clearWindow()
        self.window.after(1000, self.play)
    
    def play(self):
        self.canvas = Canvas(self.window, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        xmin = ymin = GUI.DEFAULT_SPAWN_OFFSET
        xmax, ymax = GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT
        self.snake = Snake(self.canvas, randint(xmin, xmax-xmin),
                           randint(ymin, ymax-ymin), random()*2*pi, 'orange')
        self.refresh()
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)

if __name__ == '__main__':
    GUI()
