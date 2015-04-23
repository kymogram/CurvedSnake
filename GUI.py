from tkinter import *
from random import randint, random, choice
from math import pi
import tkinter.ttk as ttk

from Snake import Snake
from Bonus import Bonus

class GUI:
    DEFAULT_WIDTH = 800        #pixels
    DEFAULT_HEIGHT = 800       #pixels
    DEFAULT_SPAWN_OFFSET = 60  #pixels
    DEFAULT_REFRESH_TIMER = 15 #ms
    BONUS_PROBABILITY = 0.01
    DEFAULT_NAME = 'GuestMooh'
    DEFAULT_COLORS = ('yellow', 'pink', 'red', 'blue', 'green', 'orange')
    
    BONUS_TIME = 100 #frames
    BONUS_SPRITES_DIMENSIONS = (32, 32) #pixels
    BONUS_DIRECTORY = './sprites/'
    BONUS_FILES = ['self_speedup.gif', 'all_speedup.gif',
                   'self_speeddown.gif', 'all_speeddown.gif',
                   'reversed_commands.gif', 'right_angles.gif']
    def __init__(self):
        self.window = Tk()
        self.window.geometry('{}x{}'.format(GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT))
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.wm_title('Curved Snake')
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        self.current_loop = 0
        self.loadBonusImages()
        self.left_key = False
        self.right_key = False
        self.regular_list = None
        self.current_color = 'yellow'
        self.move_command_left = 'Left'
        self.move_command_right = 'Right'
        self.snakes_colors = []
        self.commands_list = []
        self.snakes_names = []
        self.regular_player = []
        self.regular_colors = []
        self.regular_commands = []
        self.step = 0
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
        self.canvas.create_image(x, y, image=bonus.image,
                                 tags='bonus,{}'.format(bonus.name))
    
    def findRandomFreePosition(self, xmin, xmax, ymin, ymax):
        return randint(xmin, xmax), randint(ymin, ymax) 
    
    def refresh(self):
        for snake in self.snakes:
            if len(snake.events_queue) != 0:
                for event in snake.events_queue:
                    event[1] -= 1
                if snake.events_queue[0][1] == 0:
                    exec(snake.events_queue[0][0])
                    del snake.events_queue[0]
        if random() < GUI.BONUS_PROBABILITY:
            self.generateBonus()
        self.snakes[0].move(self.step)
        self.step += 1
        self.current_loop = self.window.after(self.timer, self.refresh)
    
    def keyPressed(self, e):
        touche = e.keysym
        if touche.lower() == 'q':
            self.quitCurrentPlay()
        for i in range(len(self.commands_list)):
            if touche in self.commands_list[i]:
                if touche == self.commands_list[i][0] and not self.snakes[i].inversed_commands or \
                   self.snakes[i].inversed_commands and touche == self.commands_list[i][1]:
                    self.snakes[i].angle -= self.snakes[i].rotating_angle
                elif touche == self.commands_list[i][1] and not self.snakes[i].inversed_commands or \
                   self.snakes[i].inversed_commands and touche == self.commands_list[i][0]:
                    self.snakes[i].angle += self.snakes[i].rotating_angle
    
    def quitCurrentPlay(self):
        self.window.after_cancel(self.current_loop)
        self.menuStart()
        self.snakes_colors = []
        self.commands_list = []
        self.snakes_names = []
    
    def clearWindow(self):
        for child in self.window.winfo_children():
            child.pack_forget()
    
    def menuStart(self):
        self.clearWindow()
        Label(self.window, width=100, text='Curved Snake').pack()
        Label(self.window, width=250, text='New player').pack()
        self.current_name = StringVar()
        self.name = Entry(self.window, textvariable=self.current_name)
        self.name.pack()
        self.current_name.set(GUI.DEFAULT_NAME)
        Label(self.window, width=250, text='Already played ?').pack()
        self.player_known = Listbox(self.window, selectmode=SINGLE)
        self.player_known.insert(END, *self.snakes_names)
        self.player_known.bind('<<ListboxSelect>>', self.showInfoPlayer)
        self.player_known.pack()
        self.button_left = Button(self.window, text='Left', bg='white',
                                  command=lambda:self.modifBgColor('L'))
        self.button_left.pack()
        self.button_right = Button(self.window, text='Right', bg='white',
                                   command=lambda:self.modifBgColor('R'))
        self.button_right.pack()
        self.color = ttk.Combobox(self.window, state='readonly', exportselection=0)
        self.color['values'] = GUI.DEFAULT_COLORS
        self.color.current(0)
        self.color.bind('<<ComboboxSelected>>', self.newSelection)
        self.color.pack()
        Button(self.window, text='Add player', command=self.addPlayer).pack()
        Label(self.window, width=250, text='Player ready to play').pack()
        self.player_ingame = Listbox(self.window, height=6, selectmode=SINGLE)
        self.player_ingame.bind('<<ListboxSelect>>', self.showInfoPlayer)
        self.player_ingame.pack()
        Button(self.window, text='Play!', command=self.playPressed).pack()
        
    def addPlayer(self):
        #ajouter couleur, contrôle, etc
        if len(self.player_known.curselection()) > 0:
            self.snakes_names.append(self.regular_player[self.id])
            self.snakes_colors.append(self.regular_colors[self.id])
            self.commands_list.append(self.regular_commands[self.id])
            self.player_ingame.insert(END, self.regular_player[self.id])
            
        else:
            self.snakes_names.append(self.current_name.get())
            self.player_ingame.insert(END, self.current_name.get())
        self.snakes_colors.append(self.current_color)
        self.commands_list.append([self.move_command_left, self.move_command_right])
        
    def newSelection(self, e):
        if len(self.player_ingame.curselection()) > 0:
            self.snakes_colors[self.id] = self.color.get().lower()
        elif len(self.player_known.curselection()) > 0:
            self.regular_colors[self.id] = self.color.get().lower()
        self.current_color = self.color.get().lower()
        self.color.selection_clear()
        
    def showInfoPlayer(self, e):
        if len(self.player_known.curselection()) > 0:
            self.regular_list = 'regular_player'
        elif len(self.player_ingame.curselection()) > 0:
            self.regular_list = None
        selected = list(map(int, e.widget.curselection()))
        if selected:
            self.colors_list = list(self.color.cget('values'))
            if self.regular_list:
                self.id = self.regular_player.index(e.widget.get(selected[0]))
                self.button_left.configure(text=self.regular_commands[self.id][0])
                self.button_right.configure(text=self.regular_commands[self.id][1])
                self.color.current(self.colors_list.index(self.regular_colors[self.id]))
            else:
                self.id = self.snakes_names.index(e.widget.get(selected[0]))
                self.button_left.configure(text=self.commands_list[self.id][0])
                self.button_right.configure(text=self.commands_list[self.id][1])
                # self.left_key = True
                # self.right_key = True
                self.color.current(self.colors_list.index(self.snakes_colors[self.id]))
            
    def playPressed(self):
        self.clearWindow()
        for i in range(len(self.snakes_names)):
            if self.snakes_names[i] not in self.regular_player:
                self.regular_player.append(self.snakes_names[i])
                self.regular_colors.append(self.snakes_colors[i])
                self.regular_commands.append(self.commands_list[i])
        self.window.after(1000, self.play)
        
    def modifBgColor(self, side):
        """
        Change la couleur de fond du boutton lorsque l'on clique dessus,
        ansi l'utilisateur sait qu'il a cliqué dessus et peut appuyer
        sur une touche pour changer ses préférences de directions
        """
        self.window.focus()
        if side == 'L':
            self.button_left.configure(bg = "red")
            self.left_key = True
        else:
            self.button_right.configure(bg = "red")
            self.right_key = True
        self.window.bind('<Key>', self.setCommand)
        
    def setCommand(self, e):
        if self.left_key:
            if len(self.player_ingame.curselection()) > 0 or len(self.player_known.curselection()) > 0:
                if self.regular_list:
                    self.regular_commands[self.id][0] = e.keysym
                else:
                    self.commands_list[self.id][0] = e.keysym
            self.move_command_left = e.keysym
            self.button_left.configure(text=self.move_command_left)
            self.button_left.configure(bg="white")
        elif self.right_key:
            if self.regular_list:
                self.regular_commands[self.id][1] = e.keysym
            if len(self.player_ingame.curselection()) > 0:
                self.commands_list[self.id][1] = e.keysym
            self.move_command_right = e.keysym
            self.button_right.configure(text=self.move_command_right)
            self.button_right.configure(bg="white")
        self.left_key = False
        self.right_key = False
        self.window.unbind('<Key>')

    def play(self):
        self.canvas = Canvas(self.window, bg='grey', highlightthickness=0)
        self.canvas.pack(fill='both', expand=1)
        xmin = ymin = GUI.DEFAULT_SPAWN_OFFSET
        xmax, ymax = GUI.DEFAULT_WIDTH, GUI.DEFAULT_HEIGHT
        self.snakes = list()
        for i in range(len(self.snakes_names)):
            self.snakes.append(Snake(self,
                                     self.snakes_names[i],
                                     randint(xmin, xmax-xmin),
                                     randint(ymin, ymax-ymin),
                                     random()*2*pi,
                                     self.snakes_colors[i]))
        self.refresh()
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)
    
    def handleBonus(self, sender_name, bonus_type):
        sender = None
        others = list()
        for snake in self.snakes:
            if snake.name == sender_name:
                sender = snake
            else:
                others.append(snake)
        if bonus_type == 'self_speedup':
            sender.speed += 1
            sender.events_queue.append(['snake.speed -= 1', GUI.BONUS_TIME])
        elif bonus_type == 'all_speedup':
            for snake in others:
                snake.speed += 1
                snake.events_queue.append(['snake.speed -= 1', GUI.BONUS_TIME])
        elif bonus_type == 'self_speeddown':
            if sender.speed > 1:
                sender.speed -= 1
                sender.events_queue.append(['snake.speed += 1', GUI.BONUS_TIME])
        elif bonus_type == 'all_speeddown':
            for snake in others:
                if snake.speed > 1:
                    snake.speed -= 1
                    snake.events_queue.append(['snake.speed += 1', GUI.BONUS_TIME])
        elif bonus_type == 'reversed_commands':
            for snake in others:
                snake.inversed_commands = True
                snake.events_queue.append(['snake.inversed_commands = False', GUI.BONUS_TIME])
        elif bonus_type == 'right_angles':
            for snake in others:
                snake.previous_angles.append(snake.rotating_angle)
                snake.rotating_angle = pi/2
                snake.events_queue.append(['snake.rotating_angle = snake.previous_angles.pop(0)', GUI.BONUS_TIME])

if __name__ == '__main__':
    GUI()
