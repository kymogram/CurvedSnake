from tkinter import *
import tkinter.ttk as ttk
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
        self.Lcommand = False
        self.Rcommand = False
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
        self.strVar = StringVar()
        self.name = Entry(self.window, textvariable=self.strVar)
        self.name.pack()
        self.strVar.set('GuestMooh')
        self.buttonLeft = Button(
                        self.window,
                        text='Left',
                        bg='white',
                        command=lambda:self.modifBgColor('L')
                    )
        self.buttonLeft.pack()
        self.buttonRight = Button(
                        self.window,
                        text='Right',
                        bg='white',
                        command=lambda:self.modifBgColor('R')
                    )
        self.buttonRight.pack()
        playButton = Button(
                    self.window,
                    text='Play!',
                    command=self.playPressed
                ).pack()
        self.color = ttk.Combobox(self.window, exportselection=0)
        self.color['values'] = ('Yellow', 'Pink', 'Red', 'Blue', 'Green', 'Orange')
        self.color.current(0)
        self.color.bind('<<ComboboxSelected>>', self.newselection)
        self.color.pack()

    def newselection(self, e):
        self.snakeColor = self.color.get()
        
    def playPressed(self):
        for child in self.window.winfo_children():
            child.pack_forget()
        self.play()
        
    def modifBgColor(self, side):
        """
        Change la couleur de fond du boutton lorsque l'on clique dessus,
        ansi l'utilisateur sait qu'il a cliqué dessus et peut appuyer
        sur une touche pour changer ses préférences de directions
        """
        if side == 'L':
            self.buttonLeft.configure(bg = "red")
            self.Lcommand = True
        else:
            self.buttonRight.configure(bg = "red")
            self.Rcommand = True
        self.window.bind('<Key>', self.setCommand)
        
    def setCommand(self, e):
        if self.Lcommand:
            self.moveCommandL = e.keysym
            self.buttonLeft.configure(text=self.moveCommandL)
            self.buttonLeft.configure(bg="white")
            self.Lcommand = False
        elif self.Rcommand:
            self.moveCommandR = e.keysym
            self.buttonRight.configure(text=self.moveCommandR)
            self.buttonRight.configure(bg="white")
            self.Rcommand = False
        self.window.unbind('<Key>')
        
    def multifunctions(self):
        #setSettings ou alors appel directement la classe Snake ?
        setSettings(self.moveCommandL, self.moveCommandR, self.color, self.strVar)
        #save |__NOT_YET__|
        play()

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
