from tkinter import *
from tkinter.messagebox import showwarning
from tkinter.ttk import Combobox
import tkinter.font

import pyglet

from random import randint, random, choice
from math import pi

from Snake import *
from Bonus import *
from InputManager import *
from MusicManager import *

class GUI:
    DEFAULT_WIDTH = 700        #pixels
    DEFAULT_HEIGHT = 700       #pixels
    DEFAULT_SPAWN_OFFSET = 60  #pixels
    DEFAULT_REFRESH_TIMER = 15 #ms
    DEFAULT_TIME_AFTER_GAME = 5#s
    BONUS_PROBABILITY = 0.01
    DEFAULT_NAME = 'GuestMooh'
    DEFAULT_COLORS = ['yellow', 'pink', 'red', 'blue', 'green', 'orange']
    DEFAULT_COMMANDS = [('Left', 'Right'),
                        ('s', 'd'),
                        ('o', 'p'),
                        ('b', 'n'),
                        ('1', '2'),
                        ('asterisk', 'minus')]
    
    MAXIMUM_NAME_LENGTH = 16 #chars
    MAX_CANVAS_BORDER = 200 #pixels
    
    BACKGROUND_MUSIC = 'data/background_music.wav'
    
    BONUS_TIME = 300 #frames
    BONUS_SPRITES_DIMENSIONS = (32, 32) #pixels
    BONUS_DIRECTORY = './sprites/'
    IMAGE_EXTENSION = 'gif'
    BONUS_FILES = ['self_speedup', 'self_speeddown',
                   'thickness_down', 'all_speeddown',
                   'reversed_commands', 'all_speedup',
                   'right_angles', 'thickness_up',
                   'rotation_angle_down', 'bonus_chance',
                   'change_color', 'change_chance_hole',
                   'clean_map', 'negative',
                   'invincible', 'shrink_map']
    BONUS_TIMES = [300, 600,
                   500, 250,
                   300, 250,
                   300, 300,
                   300,  50,
                   350, 750,
                   300, 300,
                   300, 300,]
    
    def __init__(self):
        #window
        self.window = Tk()
        self.default_values()
        self.mini_map = IntVar(value=2)
        self.one_vs_one = IntVar()
        self.window.geometry(
                        '{}x{}'.format(self.window_width, self.window_height))
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.wm_title('Curved Snake')
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        #GUI variables
        self.first_open_game  = True
        self.snakes_colors    = []
        self.commands_list    = []
        self.snakes_names     = []
        self.regular_player   = []
        self.regular_colors   = []
        self.regular_commands = []
        self.left_key = self.right_key = False
        self.is_regular_list = False
        #other variables
        self.play_once_music = True
        self.sound_activate = True
        self.inputs = InputManager()
        self.current_loop = 0
        self.step = 0
        self.bonus_percent = 30
        self.time_before_round = 5
        self.bonus_proba = (GUI.BONUS_PROBABILITY/100)*self.bonus_percent
        self.events_queue = list()
        self.music_manager = MusicManager(GUI.BACKGROUND_MUSIC)
        self.music_manager.start()
        #init
        self.loadBonusImages()
        self.loadSave()
        self.menuStart()
        self.window.protocol("WM_DELETE_WINDOW", self.saveParameters)
        self.window.mainloop()
    
    def default_values(self):
        '''
            set default values
        '''
        self.random_colors_used   = []
        self.random_commands_used = []
        self.window_height = GUI.DEFAULT_HEIGHT
        self.window_width  = GUI.DEFAULT_WIDTH
        self.canvas_height = self.window_height - 200
        self.canvas_width  = self.window_width - 200
        self.new_game = True
        self.finish_game = False
        
    def loadCurveImages(self):
        self.images_curves = []
        for i in range(1,4):
            path = '{}{}.{}'.format('./curves/curveideasnake', i, GUI.IMAGE_EXTENSION)
            self.images_curves.append(PhotoImage(file=path))
    
    def loadBonusImages(self):
        '''
            loads all the bonus image
        '''
        self.bonus_dict = dict()
        for i in range(len(GUI.BONUS_FILES)):
            path = '{}{}.{}'.format(GUI.BONUS_DIRECTORY, GUI.BONUS_FILES[i],
                                    GUI.IMAGE_EXTENSION)
            bonus = Bonus(GUI.BONUS_FILES[i], path, GUI.BONUS_TIMES[i])
            self.bonus_dict[GUI.BONUS_FILES[i]] = bonus
        self.add_bonus_bool = [IntVar(value=1) for i in range(len(self.bonus_dict))]
        
    def generateBonus(self):
        '''
            generates a random bonus and puts it on canvas
        '''
        xmin, ymin = GUI.BONUS_SPRITES_DIMENSIONS
        xmax, ymax = self.canvas_width-xmin, self.canvas_height-ymin
        x, y = self.findRandomFreePosition(xmin, xmax, ymin, ymax)
        if len(self.available_bonus) > 0:
            bonus = choice(self.available_bonus)
            self.canvas.create_image(x, y, image=bonus.image,
                                     tags='bonus,{}'.format(bonus.name))
    
    def findRandomFreePosition(self, xmin, xmax, ymin, ymax):
        '''
            returns a (X, Y) coordinate on canvas
        '''
        return randint(xmin, xmax), randint(ymin, ymax) 
    
    def changeDirections(self):
        '''
            updates the snakes direction according to the pressed keys
        '''
        for i in range(len(self.commands_list)):
            left, right = self.commands_list[i]
            if self.inputs.isPressed(left):
                self.snakes[i].turn(TURN_LEFT)
            elif self.inputs.isPressed(right):
                self.snakes[i].turn(TURN_RIGHT)
            if abs(self.snakes[i].rotating_angle - pi/2) < 0.0001:
                self.inputs.release(left if self.inputs.isPressed(left) else right)
    
    def refresh(self):
        '''
            refreshes the window every $self.timer seconds
        '''
        self.changeDirections()
        if len(self.events_queue) != 0:
            for event in self.events_queue:
                event[1] -= 1
            if self.events_queue[0][1] == 0:
                exec(self.events_queue[0][0])
                del self.events_queue[0]
        for snake in self.snakes_alive:
            if len(snake.events_queue) != 0:
                i = 0
                while i < len(snake.events_queue):
                    snake.events_queue[i][1] -= 1
                    if snake.events_queue[i][1] == 0:
                        exec(snake.events_queue[i][0])
                        del snake.events_queue[i]
                        i -= 1
                    i += 1
        if random() < self.bonus_proba:
            self.generateBonus()
        for snake in self.snakes_alive:
            snake.move(self.step)
            if not snake.getAlive():
                self.updateScore(snake)
                self.snakes_alive.remove(snake)
        if len(self.snakes_alive) == 1 and len(self.snakes) != 1 and not self.finished:
            self.save_name_winner = self.snakes_alive[0].getName()
            self.finished = True
            self.text_id = None
            self.updateRemainingTime()
            self.window.after(5000, self.finishRound)
        self.step += 1
        self.current_loop = self.window.after(self.timer, self.refresh)
    
    def updateRemainingTime(self, time=DEFAULT_TIME_AFTER_GAME):
        '''
            manage the timer to prevent for the next round
        '''
        if time != 0:
            text = '{} won this round! {} seconds remaining' \
                   .format(self.save_name_winner, time)
            if not self.text_id:
                self.text_id = self.canvas.create_text(
                                   self.canvas_height//2, self.canvas_width//2,
                                   text=text, fill='white', tags='text_win')
            else:
                self.canvas.itemconfig(self.text_id, text=text)
            self.window.after(1000, lambda: self.updateRemainingTime(time-1))
    
    def stopRefreshing(self):
        '''
            stop refresh to not have an infini loop
        '''
        self.window.after_cancel(self.current_loop)
    
    def finishRound(self):
        '''
            each end of round, this function will be called and check score +
            refresh some variable
        '''
        self.stopRefreshing()
        self.canvas_height = self.window_height - 200
        self.canvas_width = self.window_width - 200
        for elem in self.score_snake_list:
            if elem[0] >= (len(self.snakes)-1)*10:
                self.finish_game = True
        self.new_game = False
        if not self.finish_game:
            self.clearWindow()
            self.scoreShown()
            self.play()
        else:
            self.quitCurrentPlay()
    
    def updateScore(self, snake):
        '''
            update the score
        '''
        for i in range(len(self.snakes)):
            if self.snakes[i].getAlive():
                for j in range(len(self.snakes)):
                    if self.snakes[i].getName() == self.score_snake_list[j][1].getName():
                        self.score_snake_list[j][0] += 1
        self.score_snake_list = list(reversed(sorted(self.score_snake_list, key=self.getKey)))
        self.updateScoreShown()
        
    def getKey(self, item):
        return item[0]
        
    def scoreShown(self):
        '''
            show the score
        '''
        for i in range(len(self.snakes)):
            score_text = Label(self.score_frame,
                               text=str(self.score_snake_list[i][1].getName()) + ' : ' + \
                               str(self.score_snake_list[i][0]),
                               background=self.score_snake_list[i][1].getColor(),
                               font=font.Font(family='fixedsys', size=12))
            score_text.pack(padx=5, pady=5)
            
    def updateScoreShown(self):
        '''
            update the score with the label
        '''
        for child in self.score_frame.winfo_children():
            child.pack_forget()
        for i in range(len(self.score_snake_list)):
            score_text = Label(self.score_frame,
                               text=str(self.score_snake_list[i][1].getName()) + ' : ' + \
                               str(self.score_snake_list[i][0]),
                               background=self.score_snake_list[i][1].getColor(),
                               font=font.Font(family='fixedsys', size=12))
            score_text.pack(padx=5, pady=5)
        
    def geometryMap(self):
        '''
            refresh the geometry used for the main window
        '''
        self.window.geometry('{}x{}' \
                            .format(self.window_width, self.window_height))
        self.window.resizable(width=FALSE, height=FALSE)
    
    def quitCurrentPlay(self):
        '''
            stops the current game and resets the start menu
        '''
        self.stopMusic()
        self.stopRefreshing()
        self.default_values()
        self.geometryMap()
        self.menuStart()
    
    def clearWindow(self):
        '''
            clears the whole content of the window
        '''
        for child in self.window.winfo_children():
            child.pack_forget()
    
    def menuStart(self):
        '''
            sets the whole GUI start menu
        '''
        # self.loadCurveImages()
        self.clearWindow()
        # image_canvas_left = Canvas(self.window, width=500, height=700)
        # x, y = 50, 350
        # for i in range(len(self.images_curves)):
            # image_canvas_left.create_image(x, y, image=self.images_curves[i])
            # x += 80
        # image_canvas_left.pack(side=LEFT)
        Label(self.window, width=100, text='Curved Snake', font=font.Font(family='fixedsys', size=32)).pack()
        Label(self.window, width=250, text='New player').pack()
        self.current_name = StringVar()
        self.name = Entry(self.window, textvariable=self.current_name)
        self.name.bind('<Button-1>', self.removeFocus)
        self.name.pack()
        self.selectRandomName()
        Label(self.window, width=250, text='Already played ?').pack()
        self.player_known = Listbox(self.window, selectmode=SINGLE)
        self.player_known.insert(END, *self.regular_player)
        self.player_known.bind('<<ListboxSelect>>', self.showInfoPlayer)
        self.player_known.pack()
        button_frame = LabelFrame(self.window, text='Left and Right commands')
        button_frame.pack()
        self.button_left = Button(button_frame, text=GUI.DEFAULT_COMMANDS[0][0],
                                  bg='white',
                                  command=lambda: self.modifBgColor('L'))
        self.button_left.pack(side=LEFT, padx=20)
        self.button_right = Button(button_frame, text=GUI.DEFAULT_COMMANDS[0][1],
                                   bg='white',
                                   command=lambda: self.modifBgColor('R'))
        self.button_right.pack(side=RIGHT, padx=20)
        self.selectRandomCommands()
        self.color = Combobox(self.window, state='readonly', exportselection=0)
        self.color['values'] = GUI.DEFAULT_COLORS
        self.selectRandomColor()
        self.color.bind('<<ComboboxSelected>>', self.newSelection)
        self.color.pack()
        Button(self.window, text='Add player', command=self.addPlayer).pack()
        Button(self.window, text='Remove player',
               command=self.removePlayer).pack()
        Label(self.window, width=250, text='Player ready to play').pack()
        self.player_ingame = Listbox(self.window, height=6, selectmode=SINGLE)
        self.player_ingame.bind('<<ListboxSelect>>', self.showInfoPlayer)
        if not self.first_open_game:
            self.player_ingame.insert(END, *self.snakes_names)
        self.first_open_game = False
        self.player_ingame.pack()
        Button(self.window, text='Parameters', command=self.parameters).pack()
        Button(self.window, text='Play!', command=self.playPressed).pack()
        
    def parameters(self):
        '''
            sets powerups and their probability
        '''
        self.top_para = Toplevel()
        self.top_para.grab_set()
        available_bonus_frame = LabelFrame(self.top_para,
                                                text='Available bonus')
        available_bonus_frame.grid()
        for i in range(len(self.bonus_dict)):
            add_bonus = Checkbutton(available_bonus_frame,
                                image=self.bonus_dict[GUI.BONUS_FILES[i]].image,
                                variable=self.add_bonus_bool[i])
            add_bonus.grid(row=i%3, column=i//3)
        Button(available_bonus_frame,
               text='select all',
               command=self.selectAll).grid(row=4, column=1)
        Button(available_bonus_frame,
               text='unselect all',
               command=self.unselectAll).grid(row=4, column=3)
        bonus_scale_frame = LabelFrame(self.top_para,
                                            text='Bonus probability')
        bonus_scale_frame.grid(row=5)
        self.bonus_scale = Scale(bonus_scale_frame,
                                 to=100, orient=HORIZONTAL)
        self.bonus_scale.set(self.bonus_percent)
        self.bonus_scale.grid()
        available_map_frame = LabelFrame(self.top_para,
                                              text='Available map size')
        available_map_frame.grid(row=6)
        Radiobutton(available_map_frame, text='normal',
                    variable=self.mini_map, value=2).grid(row=6, column=2)
        Radiobutton(available_map_frame, text='mini map',
                    variable=self.mini_map, value=0).grid(row=6, column=3)
        Radiobutton(available_map_frame, text='1v1',
                    variable=self.mini_map, value=1).grid(row=6, column=1)
        sound_frame = LabelFrame(self.top_para, text='sound')
        sound_frame.grid(row=7)
        self.sound_button = Button(sound_frame,
                                   text='Sound on' if self.sound_activate else 'Sound off',
                                   command=self.soundActivation)
        self.sound_button.grid()
        b = Button(self.top_para, text='Set', command=self.closeAndGetVal)
        b.grid(row=8)
        
    def soundActivation(self):
        if self.sound_activate:
            self.sound_activate = False
            self.sound_button.configure(text='Sound off')
        else:
            self.sound_activate = True
            self.sound_button.configure(text='Sound on')
    
    def selectAll(self):
        for i in range(len(self.add_bonus_bool)):
            self.add_bonus_bool[i].set(1)
        
    def unselectAll(self):
        for i in range(len(self.add_bonus_bool)):
            self.add_bonus_bool[i].set(0)
    
    def closeAndGetVal(self):
        '''
            refresh values when destroying the parameters toplevel
        '''
        self.bonus_percent = self.bonus_scale.get()
        self.bonus_proba = (GUI.BONUS_PROBABILITY/100) * self.bonus_percent
        self.top_para.destroy()
    
    def selectRandomColor(self):
        '''
            sets a random color in combobox for player
        '''
        availables = [color for color in GUI.DEFAULT_COLORS \
                            if color not in self.random_colors_used]
        if len(availables) > 0:
            self.color.set(choice(availables))
            self.current_color = self.color.get()
    
    def selectRandomCommands(self):
        '''
            sets the default commands for player
        '''
        commands = None
        i = 0
        while i < len(GUI.DEFAULT_COMMANDS) and commands is None:
            if GUI.DEFAULT_COMMANDS[i] not in self.random_commands_used:
                commands = GUI.DEFAULT_COMMANDS[i]
                left_button, right_button = commands
                self.button_left.configure(text=left_button)
                self.move_command_left = left_button
                self.button_right.configure(text=right_button)
                self.move_command_right = right_button
            i += 1
    
    def selectRandomName(self):
        '''
            creates a random name for next player
        '''
        self.current_name.set('{}{}'.format(GUI.DEFAULT_NAME,
                                '' if len(self.snakes_names) == 0 \
                                else '_' + str(randint(0, 666))))
    
    def removePlayer(self):
        '''
            callback fucntion when 'remove player' button is pressed: removes
            selection from current lists
        '''
        if len(self.player_ingame.curselection()) > 0:
            self.player_ingame.delete(self.selected[0])
            try:
                del self.snakes_names[self.selected[0]]
                del self.snakes_colors[self.selected[0]]
                del self.commands_list[self.selected[0]]
            except:
                showwarning('No one to remove', 'You have no one to remove')
        else:
            showwarning('No one chosen', 'Choose a player to remove')
    
    def addPlayer(self):
        '''
            callback function when 'add player' button is pressed: saves
            config to create a new character for the following play.
        '''
        if len(self.player_known.curselection()) > 0:
            if self.regular_player[self.id] in self.snakes_names:
                showwarning('Added player',
                            'This player is already going to play!')
                return
            if self.regular_colors[self.id] in self.snakes_colors:
                showwarning('Color', 'The color chosen is already taken')
                return
            if [commands for commands in self.commands_list \
                         if self.move_command_left in commands or \
                            self.move_command_right in commands] != []:
                showwarning('Commands',
                            'Another player has already those commands')
                return
            self.snakes_colors.append(self.regular_colors[self.id])
            self.commands_list.append(self.regular_commands[self.id])
            self.snakes_names.append(self.regular_player[self.id])
            self.player_ingame.insert(END, self.regular_player[self.id])
            self.random_colors_used.append(self.regular_colors[self.id])
            self.random_commands_used.append(self.regular_commands[self.id])
        else:
            if self.current_name.get() in self.snakes_names:
                showwarning('Added player',
                            'This player is already going to play!')
                return
            if len(self.current_name.get()) > GUI.MAXIMUM_NAME_LENGTH:
                showwarning('Name player',
                            'Your name is too long. Pick a new one')
                return
            if self.current_name.get() in self.regular_player:
                showwarning('Name player', 'This name is already taken')
                return
            if self.current_color in self.snakes_colors:
                showwarning('Color', 'The color chosen is already taken')
                return
            if [commands for commands in self.commands_list \
                         if self.move_command_left in commands or \
                            self.move_command_right in commands] != []:
                showwarning('Commands',
                            'Another player has already those commands')
                return
            self.snakes_names.append(self.current_name.get())
            self.player_ingame.insert(END, self.current_name.get())
            self.snakes_colors.append(self.current_color)
            self.commands_list.append(
                            [self.move_command_left, self.move_command_right])
            self.random_colors_used.append(self.current_color)
            self.random_commands_used.append(
                            (self.move_command_left, self.move_command_right))
            self.selectRandomCommands()
            self.selectRandomColor()
            self.selectRandomName()
    
    def playPressed(self):
        '''
            callback function when play button is pressed
        '''
        if len(self.snakes_names) == 0:
            showwarning('No player', 'You have do add player to play')
        else:
            self.clearWindow()
            for i in range(len(self.snakes_names)):
                if self.snakes_names[i] not in self.regular_player:
                    self.regular_player.append(self.snakes_names[i])
                    self.regular_colors.append(self.snakes_colors[i])
                    self.regular_commands.append(self.commands_list[i])
            self.available_bonus =  [self.bonus_dict[GUI.BONUS_FILES[i]] \
                                     for i in range(len(self.bonus_dict)) \
                                     if self.add_bonus_bool[i].get() == 1]
            if self.mini_map.get() == 0:
                self.canvas_height -= 150
                self.canvas_width -= 150
            elif self.mini_map.get() == 1:
                self.canvas_height -= 300
                self.canvas_width -= 300
            self.geometryMap()
            self.window.after(1000, self.play)
    
    def modifBgColor(self, side):
        '''
            Changes button background color when clicked so user knows when
            he can press a key to set his preferences
        '''
        self.window.focus()
        if side == 'L':
            self.button_left.configure(bg='red')
            self.left_key = True
        else:
            self.button_right.configure(bg='red')
            self.right_key = True
        self.window.bind('<Key>', self.setCommand)
    
    def playMusic(self):
        '''
            starts the music in game
        '''
        
        self.music_manager.reset()
    
    def stopMusic(self):
        '''
            stops the music in game
        '''
        self.music_manager.pause()
    
    def play(self):
        '''
            prepares the game
        '''
        if self.sound_activate:
            if self.play_once_music:
                self.playMusic()
                self.play_once_music = False
        self.finished = False
        self.score_frame = LabelFrame(self.window, relief=GROOVE, bd=2, text='Scores')
        self.score_frame.pack(side=LEFT)
        self.canvas_frame = LabelFrame(self.window, relief=RAISED, bd=15, cursor='none', text='canvas')
        self.canvas_frame.pack(side=RIGHT, padx=25, pady=25)
        self.canvas = Canvas(self.canvas_frame, height=self.canvas_height,
                            width=self.canvas_width,
                            bg='black', highlightthickness=0,
                            bd=0, relief=GROOVE)
        self.canvas.pack()
        xmin = ymin = GUI.DEFAULT_SPAWN_OFFSET
        xmax, ymax = self.canvas_width, self.canvas_height
        self.snakes = list()
        for i in range(len(self.snakes_names)):
            snake = Snake(self, self.snakes_names[i],
                          randint(xmin, xmax-xmin), randint(ymin, ymax-ymin),
                          random()*2*pi, self.snakes_colors[i])
            self.snakes.append(snake)
        self.snakes_alive = self.snakes[:]
        #self.new_game will be used only to initialiate the score
        if self.new_game:
            self.score_snake_list = [[0, self.snakes[i]] for i in range(len(self.snakes))]
        self.scoreShown()
        self.startInvincible()
        #add create_text with command of each player 
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)
        self.canvas.bind('<KeyRelease>',
                         lambda e: self.inputs.release(e.keysym))
        self.refresh()
        
    def startInvincible(self):
        '''
            set invincible at the beggining of the game to situate yourself
        '''
        players = list()
        for snake in self.snakes:
            players.append(snake)
        add_event = lambda l, f: l.append([f, 150])
        for snake in players:
            add_event(snake.events_queue, 'snake.time_before_start = False')
    
    def handleBonus(self, sender_name, bonus_type):
        '''
            sets bonus and handles events queues
        '''
        sender = None
        others = list()
        for snake in self.snakes:
            if snake.name == sender_name:
                sender = snake
            else:
                others.append(snake)
        add_event = lambda l, f, i=0: l.append([f, self.bonus_dict[bonus_type].length])
        if bonus_type == 'self_speedup':
            sender.speed += 1
            sender.addArc(self.bonus_dict[bonus_type])
            add_event(sender.events_queue, 'snake.speed -= 1')
        elif bonus_type == 'all_speedup':
            for snake in others:
                snake.speed += 1
                add_event(snake.events_queue, 'snake.speed -= 1')
        elif bonus_type == 'self_speeddown':
            if sender.speed > 1:
                sender.speed /= 1.5
                add_event(sender.events_queue,'snake.speed *= 1.5')
        elif bonus_type == 'all_speeddown':
            for snake in others:
                if snake.speed > 1:
                    snake.speed /= 1.5
                    add_event(snake.events_queue, 'snake.speed *= 1.5')
        elif bonus_type == 'reversed_commands':
            for snake in others:
                snake.inversed_commands = True
                add_event(snake.events_queue, 'snake.inversed_commands = False')
        elif bonus_type == 'right_angles':
            for snake in others:
                snake.previous_angles.append(snake.rotating_angle)
                snake.rotating_angle = pi/2
                add_event(snake.events_queue, 'snake.restoreAngle()')
        elif bonus_type == 'thickness_up':
            for snake in others:
                snake.thickness += DEFAULT_THICKNESS
                add_event(snake.events_queue,
                          'snake.thickness -= DEFAULT_THICKNESS')
        elif bonus_type == 'thickness_down':
            sender.thickness /= 2
            add_event(sender.events_queue, 'snake.thickness *= 2')
        elif bonus_type == 'bonus_chance':
            #Precaution to not have bonus poping all around the map
            if self.bonus_proba <= 0.16:
                if self.bonus_proba <= 0.04:
                    self.bonus_proba *= 4
                    add_event(self.events_queue, 'self.bonus_proba /= 4')
                else:
                    self.bonus_proba *=2
                    add_event(self.events_queue, 'self.bonus_proba /= 2')
        elif bonus_type == 'rotation_angle_down':
            for snake in others:
                snake.rotating_angle /= 2
                add_event(snake.events_queue, 'snake.rotating_angle *= 2')
        elif bonus_type == 'change_color':
            for snake in others:
                snake.color = sender.color
                add_event(snake.events_queue,
                          'snake.color = snake.color_unchanged')
        elif bonus_type == 'change_chance_hole':
            for snake in others:
                snake.hole_probability *= 10
                add_event(snake.events_queue, 'snake.hole_probability /= 10')
        elif bonus_type == 'invincible':
            sender.invincible = True
            add_event(sender.events_queue, 'snake.invincible = False')
        elif bonus_type == 'clean_map':
            heads = [snake.head_coord for snake in self.snakes]
            self.bonus_list = list()
            for bonus in GUI.BONUS_FILES:
                for el in self.canvas.find_withtag('bonus,' + bonus):
                    self.bonus_list.append(list(self.canvas.coords(el)) + [bonus])
            self.canvas.delete(ALL)
            for i in range(len(heads)):
                x, y = heads[i]
                snake = self.snakes[i]
                r = snake.thickness//2
                snake.head_id = self.canvas.create_oval(
                        x-r, y-r, x+r, y+r, fill=snake.color,
                        outline=snake.color, tag='snake,{},-1'.format(snake.name))
            for x, y, name in self.bonus_list:
                self.canvas.create_image(x, y, image=self.bonus_dict[name].image,
                                         tags='bonus,{}'.format(self.bonus_dict[name].name))
        elif bonus_type == 'negative':
            self.canvas.configure(bg=self.invertColor('black'))
            add_event(self.events_queue, 'self.canvas.configure(bg="black")')
            for snake in self.snakes:
                snake.color = self.invertColor(snake.getColor())
                snake.updateHeadColor()
                add_event(snake.events_queue, 'snake.color = snake.color_unchanged')
                add_event(snake.events_queue, 'snake.updateHeadColor()')
        elif bonus_type == 'shrink_map':
            self.shrinkMap()
    
    def shrinkMap(self):
        '''
            shrink the map if the bonus shrink_map is taken
        '''
        if not self.finished:
            border = int(self.canvas['bd'])
            if border < GUI.MAX_CANVAS_BORDER:
                self.canvas_height -= 4
                self.canvas_width -= 4
                self.canvas.configure(bd=border+2, height=self.canvas_height, width=self.canvas_width)
                self.window.after(100, self.shrinkMap)
    
    #callbacks
    
    def invertColor(self, color):
        rgb = self.canvas.winfo_rgb(color)
        inv_red, inv_green, inv_blue = \
                                255-(rgb[0]//256), 255-(rgb[1]//256), 255-(rgb[2]//256)
        return "#{:02x}{:02x}{:02x}".format(inv_red, inv_green, inv_blue)
    
    def setCommand(self, e):
        '''
            callback function when new command (left/right) is chosen
        '''
        if self.left_key:
            if len(self.player_ingame.curselection()) > 0 or \
               len(self.player_known.curselection()) > 0:
                if self.is_regular_list:
                    self.regular_commands[self.id][0] = e.keysym
                else:
                    self.commands_list[self.id][0] = e.keysym
            self.move_command_left = e.keysym
            self.button_left.configure(text=self.move_command_left)
            self.button_left.configure(bg='white')
        elif self.right_key:
            if self.is_regular_list:
                self.regular_commands[self.id][1] = e.keysym
            if len(self.player_ingame.curselection()) > 0:
                self.commands_list[self.id][1] = e.keysym
            self.move_command_right = e.keysym
            self.button_right.configure(text=self.move_command_right)
            self.button_right.configure(bg='white')
        self.left_key = False
        self.right_key = False
        self.window.unbind('<Key>')
    
    def newSelection(self, e):
        '''
            callback function when combobox selection changes
        '''
        if len(self.player_ingame.curselection()) > 0:
            self.snakes_colors[self.id] = self.color.get().lower()
        elif len(self.player_known.curselection()) > 0:
            self.regular_colors[self.id] = self.color.get().lower()
        self.current_color = self.color.get().lower()
        self.color.selection_clear()
        
    def showInfoPlayer(self, e):
        '''
            resets informations about selected user
        '''
        if len(self.player_known.curselection()) > 0:
            self.is_regular_list = True
        elif len(self.player_ingame.curselection()) > 0:
            self.is_regular_list = False
        self.selected = list(map(int, e.widget.curselection()))
        if self.selected:
            self.colors_list = list(self.color.cget('values'))
            selection = e.widget.get(self.selected[0])
            if self.is_regular_list:
                self.id = self.regular_player.index(selection)
                self.button_left.configure(
                                         text=self.regular_commands[self.id][0])
                self.button_right['text'] = self.regular_commands[self.id][1]
                self.color.current(self.colors_list.index(
                                                self.regular_colors[self.id]))
                self.move_command_left = self.regular_commands[self.id][0]
                self.move_command_right = self.regular_commands[self.id][1]
            else:
                self.id = self.snakes_names.index(selection)
                self.button_left.configure(text=self.commands_list[self.id][0])
                self.button_right.configure(text=self.commands_list[self.id][1])
                self.color.current(
                            self.colors_list.index(self.snakes_colors[self.id]))
    
    def removeFocus(self, e):
        '''
            clears selection from listboxes
        '''
        self.player_ingame.selection_clear(0, END)
        self.player_known.selection_clear(0, END)
    
    def keyPressed(self, e):
        '''
            callback function when any key is pressed in canvas
        '''
        key = e.keysym
        if key.lower() == 'q':
            self.quitCurrentPlay()
        else:
            #move the correct player(s) when key is pressed
            self.inputs.press(key)
    def saveParameters(self):
        '''
            save paramers about players habit
        '''
        save = open("save.txt", "w")
        for i in range(len(self.regular_player)):
            save.write(str(self.regular_player[i])+'\ncommand left = '+str(self.regular_commands[i][0])+
            '\ncommand right = '+str(self.regular_commands[i][1])+'\ncolor = '+str(self.regular_colors[i])+'\n')
        self.window.destroy()
    def loadSave(self):
        '''
            load the parameters saved about players habit
        '''
        try:
            save = open("save.txt", "r")
        except:
            pass
        text = save.readlines()
        for i in range(len(text)):
            x = i%4
            if x == 0:
                name = text[i].strip()
                self.regular_player.append(name)
            elif x == 1:
                Lcommand = text[i].split('=')
                Lcommand = Lcommand[1].strip()

            elif x == 2:
                Rcommand = text[i].split('=')
                Rcommand = Rcommand[1].strip()
                try:
                    self.regular_commands.append([Lcommand, Rcommand])
                except:
                    pass
            else:
                color = text[i].split()
                color = color[2]
                self.regular_colors.append(color)
    
if __name__ == '__main__':
    GUI()
