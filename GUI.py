from tkinter import *
from random import randint, random, choice
from math import pi

from Snake import Snake
from Bonus import Bonus

class GUI:
    DEFAULT_WIDTH = 800        #pixels
    DEFAULT_HEIGHT = 800       #pixels
    DEFAULT_SPAWN_OFFSET = 60  #pixels
    DEFAULT_REFRESH_TIMER = 15 #ms
    BONUS_PROBABILITY = 0.02
    
    BONUS_SPRITES_DIMENSIONS = (32, 32) #pixels
    BONUS_DIRECTORY = './sprites/'
    BONUS_FILES = ['speedup.gif']
    def __init__(self):
        self.window = Tk()
        self.window.geometry('{}x{}'.format(GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT))
        self.window.resizable(width=FALSE, height=FALSE)
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        self.current_loop = 0
        self.loadBonusImages()
        self.menuStart()
        self.window.mainloop()
    
    def loadBonusImages(self):
        self.bonus_list = list()
        for file_name in GUI.BONUS_FILES:
            self.bonus_list.append(Bonus(GUI.BONUS_DIRECTORY + file_name))
    
    def generateBonus(self):
        xmin, ymin = GUI.BONUS_SPRITES_DIMENSIONS
        xmax, ymax = GUI.DEFAULT_WIDTH-xmin, GUI.DEFAULT_HEIGHT-ymin
        x, y = self.findRandomFreePosition(xmin, xmax, ymin, ymax)
        bonus = choice(self.bonus_list)
        tmp = self.canvas.create_image(x, y, image=bonus.image)
        self.bonus.append(tmp)
    
    def findRandomFreePosition(self, xmin, xmax, ymin, ymax):
        return randint(xmin, xmax), randint(ymin, ymax) 
    
    def refresh(self):
        if random() < GUI.BONUS_PROBABILITY:
            self.generateBonus()
        self.snakes[0].move(self.current_loop)
        self.current_loop = self.window.after(self.timer, self.refresh)
    
    def keyPressed(self, e):
        touche = e.keysym
        if touche in ('Right', 'Left'):
            self.snakes[0].angle += 0.15 * {'R': 1, 'L': -1}[touche[0]]
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
        self.canvas = Canvas(self.window, bg='grey', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        xmin = ymin = GUI.DEFAULT_SPAWN_OFFSET
        xmax, ymax = GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT
        self.bonus = list()
        self.snakes = list()
        self.snakes.append(Snake(self.canvas, randint(xmin, xmax-xmin),
                           randint(ymin, ymax-ymin), random()*2*pi, 'orange'))
        self.refresh()
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)

if __name__ == '__main__':
    GUI()
