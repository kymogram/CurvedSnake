from tkinter.messagebox import showwarning
from tkinter.font import Font
from tkinter.filedialog import askopenfilename

import shelve

from random import randint, random, choice
from math import pi

from .Snake import *
from .InputManager import InputManager
from .MusicManager import MusicManager
from .ComboColorBox import ComboColorBox
from .Profile import Profile
from .BonusManager import BonusManager


class GUI:
    DEFAULT_WIDTH = 850  # pixels
    DEFAULT_HEIGHT = 850  # pixels
    DEFAULT_SPAWN_OFFSET = 60  # pixels
    DEFAULT_REFRESH_TIMER = 15  # ms
    DEFAULT_TIME_AFTER_GAME = 5  # s
    BONUS_PROBABILITY = 0.01
    DEFAULT_NAME = 'GuestMooh'
    DEFAULT_COLORS = ['yellow', 'pink', 'red', 'blue', 'green', 'orange']
    DEFAULT_COMMANDS = [('Left', 'Right'),
                        ('s', 'd'),
                        ('o', 'p'),
                        ('b', 'n'),
                        ('1', '2'),
                        ('asterisk', 'minus')]

    MAXIMUM_NAME_LENGTH = 16  # chars
    MAX_CANVAS_BORDER = 200  # pixels

    MUSIC_DEFAULT_DIR = 'data/'
    BACKGROUND_MUSIC = 'data/background_music.wav'
    SAVE_FILE = 'save/data.shelf'
    SAVE_FORMAT = '{}\n' \
                  'command left = {}\n' \
                  'command right = {}\n' \
                  'color = {}\n' \
                  'tmp_artic_achiv = {}\n'
    NB_DATA_IN_SAVE = 5

    BONUS_TIME = 300  # frames

    def __init__(self):
        # window
        self.window = Tk()
        self.defaultValues()
        self.mini_map = IntVar(value=2)
        self.one_vs_one = IntVar()
        geom = '{}x{}'.format(self.window_width, self.window_height)
        self.window.geometry(geom)
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.wm_title('Curved Snake')
        self.timer = GUI.DEFAULT_REFRESH_TIMER
        # GUI variables
        self.first_open_game = True
        self.snakes_ingame = []
        self.counter_special = []
        self.left_key = self.right_key = False
        self.current_bg = 'white'
        self.current_fg = 'black'
        # other variables
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
        self.portal_index = 0
        self.profiles = dict()
        self.bonus_manager = BonusManager(self)
        # init
        self.bonus_manager.loadBonus()
        self.loadSave()
        self.menuStart()
        self.window.protocol("WM_DELETE_WINDOW", self.saveParameters)
        self.window.mainloop()

    def defaultValues(self):
        '''
            set default values
        '''
        self.random_colors_used = []
        self.random_commands_used = []
        self.window_height = GUI.DEFAULT_HEIGHT
        self.window_width = GUI.DEFAULT_WIDTH
        self.canvas_height = self.window_height - 200
        self.canvas_width = self.window_width - 200
        self.new_game = True
        self.finish_game = False

    def loadCurveImages(self):
        '''
            not used yet/anymore (to load images)
        '''
        self.images_curves = []
        for i in range(1, 4):
            path = '{}{}.{}'.format('./curves/curveideasnake',
                                    i, GUI.IMAGE_EXTENSION)
            self.images_curves.append(PhotoImage(file=path))

    def changeDirections(self):
        '''
            updates the snakes direction according to the pressed keys
        '''
        for snake in self.snakes:
            left, right = self.profiles[snake.name].commands
            if self.inputs.isPressed(left):
                snake.turn(TURN_LEFT)
            elif self.inputs.isPressed(right):
                snake.turn(TURN_RIGHT)
            if abs(snake.rotating_angle - pi/2) < 0.0001:
                self.inputs.release(left if self.inputs.isPressed(left)
                                    else right)

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
            self.bonus_manager.generateBonus()
        for snake in self.snakes_alive:
            snake.move(self.step)
            if not snake.getAlive():
                self.updateScore(snake)
                self.snakes_alive.remove(snake)
        if len(self.snakes_alive) == 1 and \
           len(self.snakes) != 1 and not self.finished:
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
                self.text_id = self.canvas.create_text(self.canvas_height//2,
                                                       self.canvas_width//2,
                                                       text=text,
                                                       fill='white',
                                                       tags='text_win')
            else:
                self.canvas.itemconfig(self.text_id, text=text)
            self.window.after(1000, lambda: self.updateRemainingTime(time-1))

    def stopRefreshing(self):
        '''
            stop refresh to not have an infinite loop
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
        self.checkResizeMap()
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
                snakeName = self.snakes[i].getName()
                for j in range(len(self.snakes)):
                    if snakeName == self.score_snake_list[j][1].getName():
                        self.score_snake_list[j][0] += 1
        self.score_snake_list = sorted(self.score_snake_list,
                                       key=lambda i: i[0])
        self.score_snake_list = list(reversed(self.score_snake_list))
        self.updateScoreShown()

    def scoreShown(self):
        '''
            show the score
        '''
        for i in range(len(self.snakes)):
            score_text = Label(self.score_frame,
                               text=self.score_snake_list[i][1].getName() +
                               ' : ' + str(self.score_snake_list[i][0]),
                               bg=self.score_snake_list[i][1].getColor(),
                               font=Font(family='fixedsys', size=12))
            score_text.pack(padx=5, pady=5)

    def updateScoreShown(self):
        '''
            update the score with the label
        '''
        for child in self.score_frame.winfo_children():
            child.pack_forget()
        self.scoreShown()

    def geometryMap(self):
        '''
            refresh the geometry used for the main window
        '''
        geom = '{}x{}'.format(self.window_width, self.window_height)
        self.window.geometry(geom)
        self.window.resizable(width=FALSE, height=FALSE)

    def quitCurrentPlay(self):
        '''
            stops the current game and resets the start menu
        '''
        self.stopMusic()
        self.stopRefreshing()
        self.defaultValues()
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
        self.tmp_widget = []
        self.window.configure(bg=self.current_bg)
        self.clearWindow()
        if self.sound_activate:
            self.play_once_music = True
        l = Label(self.window, width=100, text='Curved Snake',
                  font=Font(family='fixedsys', size=32), bg=self.current_bg,
                  fg=self.current_fg)
        l.pack()
        self.tmp_widget.append(l)
        l = Label(self.window, width=250, text='New player',
                  font=Font(family='Arial Unicode MS'), bg=self.current_bg,
                  fg=self.current_fg)
        l.pack()
        self.tmp_widget.append(l)
        self.current_name = StringVar()
        self.name = Entry(self.window, textvariable=self.current_name,
                          bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(self.name)
        self.name.bind('<Button-1>', self.removeFocus)
        self.name.pack()
        self.selectRandomName()
        l = Label(self.window, width=250, text='Already played ?',
                  font=Font(family='Arial Unicode MS'),
                  bg=self.current_bg,
                  fg=self.current_fg)
        l.pack()
        self.tmp_widget.append(l)
        self.player_known = Listbox(self.window, selectmode=SINGLE,
                                    bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(self.player_known)
        self.player_known.insert(END, *list(self.profiles.keys()))
        self.player_known.bind('<<ListboxSelect>>', self.showInfoPlayer)
        self.player_known.pack()
        b = Button(self.window, text='Remove regular player',
                   command=self.removeRegularPlayer, bg=self.current_bg,
                   fg=self.current_fg)
        b.pack()
        self.tmp_widget.append(b)
        font = Font(family='Arial Unicode MS', size=10)
        button_frame = LabelFrame(self.window, text='Left and Right commands',
                                  font=font, bg=self.current_bg,
                                  fg=self.current_fg)
        self.tmp_widget.append(button_frame)
        button_frame.pack()
        self.button_left = Button(button_frame, bg=self.current_bg,
                                  fg=self.current_fg,
                                  text=GUI.DEFAULT_COMMANDS[0][0],
                                  command=lambda: self.modifBgColor('L'))
        self.tmp_widget.append(self.button_left)
        self.button_left.pack(side=LEFT, padx=20)
        self.button_right = Button(button_frame,
                                   text=GUI.DEFAULT_COMMANDS[0][1],
                                   bg=self.current_bg, fg=self.current_fg,
                                   command=lambda: self.modifBgColor('R'))
        self.tmp_widget.append(self.button_right)
        self.button_right.pack(side=RIGHT, padx=20)
        self.selectRandomCommands()
        font = Font(family='Arial Unicode MS', size=10)
        self.color_frame = LabelFrame(self.window, width=100,
                                      text='Choose your color', font=font,
                                      bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(self.color_frame)
        self.color_frame.pack()
        self.color = ComboColorBox(self, self.color_frame, GUI.DEFAULT_COLORS)
        self.selectRandomColor()
        colorVal = self.color.getColorVal()
        colorVal.trace('w', lambda n, m, s: self.newSelection())
        b = Button(self.window, text='Add player', command=self.addPlayer,
                   bg=self.current_bg, fg=self.current_fg)
        b.pack()
        self.tmp_widget.append(b)
        l = Label(self.window, width=250, text='Player ready to play',
                  font=font, bg=self.current_bg,
                  fg=self.current_fg)
        l.pack()
        self.tmp_widget.append(l)
        self.player_ingame = Listbox(self.window, height=6, selectmode=SINGLE,
                                     bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(self.player_ingame)
        self.player_ingame.bind('<<ListboxSelect>>', self.showInfoPlayer)
        self.player_ingame.insert(END, *self.snakes_ingame)
        self.first_open_game = False
        self.player_ingame.pack()
        b = Button(self.window, text='Remove player',
                   command=self.removePlayer, bg=self.current_bg,
                   fg=self.current_fg)
        b.pack()
        self.tmp_widget.append(b)
        ready_to_play = LabelFrame(self.window, text='Finally ready to play ?',
                                   font=font, bg=self.current_bg,
                                   fg=self.current_fg)
        self.tmp_widget.append(ready_to_play)
        ready_to_play.pack()
        b = Button(ready_to_play, text='Parameters', command=self.parameters,
                   bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(b)
        b.pack(padx=5, pady=5)
        b = Button(ready_to_play, text='Play!', command=self.playPressed,
                   bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget.append(b)
        b.pack(padx=5, pady=5)
        b = Button(self.window, text='Change GUI style',
                   command=self.changeStyle, bg=self.current_bg,
                   fg=self.current_fg)
        self.tmp_widget.append(b)
        b.pack()

    def parameters(self):
        '''
            sets powerups and their probability
        '''
        self.top_para = Toplevel(bg=self.current_bg)
        self.top_para.grab_set()
        available_bonus_frame = LabelFrame(self.top_para,
                                           text='Available bonus',
                                           bg=self.current_bg,
                                           fg=self.current_fg)
        available_bonus_frame.grid()
        bonus_dict = self.bonus_manager.getBonusDict()
        for i in range(len(bonus_dict)):
            bonus = bonus_dict[BonusManager.BONUS_FILES[i]]
            add_bonus = Checkbutton(available_bonus_frame,
                                    image=bonus.image,
                                    variable=self.add_bonus_bool[i],
                                    bg=self.current_bg)
            add_bonus.grid(row=i % 3, column=i // 3)
        b = Button(available_bonus_frame,
                   text='select all',
                   command=self.selectAll,
                   bg=self.current_bg,
                   fg=self.current_fg)
        b.grid(row=4, column=2)
        b = Button(available_bonus_frame, text='unselect all',
                   command=self.unselectAll, bg=self.current_bg,
                   fg=self.current_fg)
        b.grid(row=4, column=4)
        bonus_scale_frame = LabelFrame(self.top_para, text='Bonus probability',
                                       bg=self.current_bg, fg=self.current_fg)
        bonus_scale_frame.grid(row=5)
        self.bonus_scale = Scale(bonus_scale_frame,
                                 to=100, orient=HORIZONTAL,
                                 bg=self.current_bg, fg=self.current_fg)
        self.bonus_scale.set(self.bonus_percent)
        self.bonus_scale.grid()
        available_map_frame = LabelFrame(self.top_para,
                                         text='Available map size',
                                         bg=self.current_bg,
                                         fg=self.current_fg)
        available_map_frame.grid(row=6)
        Radiobutton(available_map_frame, text='normal',
                    variable=self.mini_map, value=2).grid(row=6, column=2)
        Radiobutton(available_map_frame, text='mini map',
                    variable=self.mini_map, value=0).grid(row=6, column=3)
        Radiobutton(available_map_frame, text='1v1',
                    variable=self.mini_map, value=1).grid(row=6, column=1)
        sound_frame = LabelFrame(self.top_para, text='Music',
                                 bg=self.current_bg, fg=self.current_fg)
        sound_frame.grid(row=7)
        sound = {True: 'on', False: 'off'}[self.sound_activate]
        self.sound_button = Button(sound_frame, text='Sound ' + sound,
                                   command=self.soundActivation,
                                   bg=self.current_bg, fg=self.current_fg)
        self.sound_button.grid()
        self.choose_sound_button = Button(sound_frame, text='Choose Music',
                                          command=self.choose_music,
                                          bg=self.current_bg,
                                          fg=self.current_fg)
        self.choose_sound_button.grid()
        b = Button(self.top_para, text='Set', command=self.closeAndGetVal,
                   bg=self.current_bg, fg=self.current_fg)
        b.grid(row=8)

    def changeStyle(self):
        self.top_style = Toplevel(bg=self.current_bg)
        self.top_style.grab_set()
        self.tmp_widget_top_style = []
        save_bg = self.current_bg
        save_fg = self.current_fg
        choosebg = LabelFrame(self.top_style, text='Background',
                              bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget_top_style.append(choosebg)
        choosebg.pack()
        self.background_color = ComboColorBox(self, choosebg,
                                              GUI.DEFAULT_COLORS)
        self.background_color.set(self.current_bg)
        choosefg = LabelFrame(self.top_style, text='Foreground',
                              bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget_top_style.append(choosefg)
        choosefg.pack()
        self.foreground_color = ComboColorBox(self, choosefg,
                                              GUI.DEFAULT_COLORS)
        self.foreground_color.set(self.current_fg)
        try_set_frame = LabelFrame(self.top_style, text='Test it and Adopt it',
                                   bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget_top_style.append(try_set_frame)
        try_set_frame.pack()
        try_option = Button(try_set_frame, text='Try',
                            command=self.updateStyle,
                            bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget_top_style.append(try_option)
        try_option.grid(padx=10, pady=5)
        set_option = Button(try_set_frame, text='Set',
                            command=self.setStyle,
                            bg=self.current_bg, fg=self.current_fg)
        self.tmp_widget_top_style.append(set_option)
        set_option.grid(row=0, column=1, padx=10, pady=5)
        callback = lambda: self.updateStyle(save_bg, save_fg)
        cancel_option = Button(try_set_frame, text='Cancel',
                               command=callback, bg=self.current_bg,
                               fg=self.current_fg)
        self.tmp_widget_top_style.append(cancel_option)
        cancel_option.grid(row=0, column=2, padx=10, pady=5)
        self.top_style.protocol('WM_DELETE_WINDOW',
                                lambda: self.destroyStyle(save_bg, save_fg))

    def destroyStyle(self, old_bg, old_fg):
        self.updateStyle(old_bg, old_fg)
        self.top_style.destroy()

    def setStyle(self):
        self.updateStyle()
        self.top_style.destroy()

    def updateStyle(self, old_bg=None, old_fg=None):
        if old_bg is None:  # if old_bg is None, old_fg is None too
            self.current_bg = self.background_color.getColor()
            self.current_fg = self.foreground_color.getColor()
        else:
            self.current_bg = old_bg
            self.current_fg = old_fg
        for w in self.tmp_widget:
            w.configure(bg=self.current_bg, fg=self.current_fg)
        for w in self.tmp_widget_top_style:
            w.configure(bg=self.current_bg, fg=self.current_fg)
        self.top_style.configure(bg=self.current_bg)
        self.window.configure(bg=self.current_bg)
        # If we don't check icon, it disappears
        self.background_color.createColorIcon()

    def soundActivation(self):
        self.sound_activate = False if self.sound_activate else True
        sound = {True: 'on', False: 'off'}[self.sound_activate]
        self.sound_button.configure(text='Sound ' + sound)

    def choose_music(self):
        types = [("WVA files", "*.wav"), ("MP3 files", "*.mp3")]
        tmp = askopenfilename(filetypes=types,
                              initialdir=GUI.MUSIC_DEFAULT_DIR)
        if tmp is not None:
            GUI.BACKGROUND_MUSIC = tmp
            self.music_manager.changeTrack(GUI.BACKGROUND_MUSIC)

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
        availables = [color for color in GUI.DEFAULT_COLORS
                      if color not in self.random_colors_used]
        if len(availables) > 0:
            self.color.set(choice(availables))
            self.current_color = self.color.getColor().lower()

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
                              '' if len(self.snakes_ingame) == 0
                              else '_' + str(randint(0, 666))))

    def removePlayer(self):
        '''
            callback function when 'remove player' button is pressed: removes
            selection from current lists
        '''
        if len(self.player_ingame.curselection()) > 0:
            self.player_ingame.delete(self.selected[0])
            try:
                del self.snakes_ingame[self.selected[0]]
            except:
                showwarning('No one to remove', 'You have no one to remove')
        else:
            showwarning('No one chosen', 'Choose a player to remove')

    def removeRegularPlayer(self):
        '''
            callback function when 'remove player' button is pressed: removes
            selection from current lists
        '''
        if len(self.player_known.curselection()) > 0:
            name = self.player_known.get(self.selected[0])
            self.player_known.delete(self.selected[0])
            print(name)
            if name in self.profiles:
                del self.profiles[name]
                print(self.profiles)
            else:
                showwarning('No one to remove', 'You have no one to remove')
        else:
            showwarning('No one chosen', 'Choose a player to remove')

    def addPlayer(self):
        '''
            callback function when 'add player' button is pressed: saves
            config to create a new character for the following play.
        '''
        if len(self.snakes_ingame) == 6:
            showwarning("can't add another player",
                        'Maximum number of player is 6')
            return
        if len(self.player_known.curselection()) > 0:
            if self.name_selection in self.snakes_ingame:
                showwarning('Added player',
                            'This player is already going to play!')
                return
            current_color = self.profiles[self.name_selection].color
            for snake in self.player_ingame.get(0, END):
                if current_color == self.profiles[snake].color:
                    showwarning('Color', 'The color chosen is already taken')
                    return
            for snake in self.player_ingame.get(0, END):
                commands = self.profiles[snake].commands
                if self.move_command_left in commands or \
                   self.move_command_right in commands:
                    showwarning('Commands',
                                'Another player has already those commands')
                    return
            self.snakes_ingame.append(self.name_selection)
            self.player_ingame.insert(END, self.name_selection)
            color = self.profiles[self.name_selection].color
            self.random_colors_used.append(color)
            commands = self.profiles[self.name_selection].commands
            self.random_commands_used.append(commands)
        else:
            if self.current_name.get() in self.snakes_ingame:
                showwarning('Added player',
                            'This player is already going to play!')
                return
            if len(self.current_name.get()) > GUI.MAXIMUM_NAME_LENGTH:
                showwarning('Name player',
                            'Your name is too long. Pick a new one')
                return
            if self.current_name.get() in self.profiles:
                showwarning('Name player', 'This name is already taken')
                return
            # for snake in self.snakes_ingame:
            for snake in self.player_ingame.get(0, END):
                if self.current_color == self.profiles[snake].color:
                    showwarning('Color', 'The color chosen is already taken')
                return
            for snake in self.player_ingame.get(0, END):
                commands = self.profiles[snake.name].commands
                if self.move_command_left in commands or \
                   self.move_command_right in commands:
                    showwarning('Commands',
                                'Another player has already those commands')
                    return
            self.snakes_ingame.append(self.current_name.get())
            self.player_ingame.insert(END, self.current_name.get())
            self.random_colors_used.append(self.current_color)
            self.random_commands_used.append((self.move_command_left,
                                              self.move_command_right))
            name = self.current_name.get()
            commands = [self.move_command_left, self.move_command_right]
            self.profiles[name] = Profile(name, False, commands,
                                          self.current_color)
            self.selectRandomCommands()
            self.selectRandomColor()
            self.selectRandomName()

    def playPressed(self):
        '''
            callback function when play button is pressed
        '''
        if len(self.snakes_ingame) == 0:
            showwarning('No player', 'You have to add player to play')
        else:
            self.clearWindow()
            self.available_bonus = 1 in [b.get() for b in self.add_bonus_bool]
            self.checkResizeMap()
            self.geometryMap()
            self.window.after(1000, self.play)

    def checkResizeMap(self):
        if self.mini_map.get() == 0:
            self.canvas_height -= 150
            self.canvas_width -= 150
        elif self.mini_map.get() == 1:
            self.canvas_height -= 300
            self.canvas_width -= 300

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
        self.bonus_manager.refreshBonusProba()
        if self.sound_activate:
            if self.play_once_music:
                self.playMusic()
                self.play_once_music = False
        self.finished = False
        self.score_frame = LabelFrame(self.window, relief=GROOVE, bd=2,
                                      text='Scores')
        self.score_frame.pack(side=LEFT)
        self.canvas_frame = LabelFrame(self.window, relief=RAISED, bd=15,
                                       cursor='none', text='canvas',
                                       bg=None)
        self.canvas_frame.pack(side=RIGHT, padx=25, pady=25)
        self.canvas = Canvas(self.canvas_frame, height=self.canvas_height,
                             width=self.canvas_width,
                             bg='black', highlightthickness=0,
                             bd=0, relief=GROOVE)
        self.canvas.pack()
        xmin = ymin = GUI.DEFAULT_SPAWN_OFFSET
        xmax, ymax = self.canvas_width, self.canvas_height
        self.snakes = list()
        for name in self.snakes_ingame:
            snake = Snake(self, name, randint(xmin, xmax-xmin),
                          randint(ymin, ymax-ymin), random()*2*pi,
                          self.profiles[name].color)
            self.snakes.append(snake)
        self.snakes_alive = self.snakes[:]
        # self.new_game will be used only to initialize the score
        if self.new_game:
            self.score_snake_list = [[0, self.snakes[i]]
                                     for i in range(len(self.snakes))]
            self.counter_special = [[0, 0, 0] for i in range(len(self.snakes))]
        self.scoreShown()
        self.startInvincible()
        # add create_text with command of each player
        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.keyPressed)
        self.canvas.bind('<KeyRelease>',
                         lambda e: self.inputs.release(e.keysym))
        self.refresh()

    def startInvincible(self):
        '''
            set invincible at the beggining of the game to situate yourself
        '''
        add_event = lambda l, f: l.append([f, 150])
        for snake in self.snakes:
            add_event(snake.events_queue, 'snake.in_time_before_start = False')

    def handleBonus(self, sender, bonus_type):
        '''
            sets bonus and handles events queues
        '''
        self.checkSpecialCounter(sender, bonus_type)
        self.bonus_manager.handleBonus(sender, bonus_type, self.bonus_proba)

    def checkSpecialCounter(self, snake, bonus_type):
        idx = self.snakes.index(snake)
        if bonus_type == 'negative':
            self.counter_special[idx][0] += 1
        elif bonus_type == 'change_color':
            self.counter_special[idx][1] += 1
        elif bonus_type == 'artic':
            self.counter_special[idx][2] += 1
        if self.counter_special[idx][2] >= 2 and \
           self.counter_special[idx][1] >= 5 and \
           self.counter_special[idx][0] >= 5:
            self.profiles[snake.name].has_artic = True

    def shrinkMap(self):
        '''
            shrink the map if the bonus shrink_map is taken
        '''
        if not self.finished:
            border = int(self.canvas['bd'])
            if border < GUI.MAX_CANVAS_BORDER:
                self.canvas_height -= 4
                self.canvas_width -= 4
                self.canvas.configure(bd=border+2, height=self.canvas_height,
                                      width=self.canvas_width)
                self.window.after(100, self.shrinkMap)

    def setCommand(self, e):
        '''
            callback function when new command (left/right) is chosen
        '''
        if self.left_key:
            if len(self.player_ingame.curselection()) > 0 or \
               len(self.player_known.curselection()) > 0:
                self.profiles[self.name_selection].commands[0] = e.keysym
            self.move_command_left = e.keysym
            self.button_left.configure(text=self.move_command_left)
            self.button_left.configure(bg=self.current_bg)
        elif self.right_key:
            self.profiles[self.name_selection].commands[1] = e.keysym
            self.move_command_right = e.keysym
            self.button_right.configure(text=self.move_command_right)
            self.button_right.configure(bg=self.current_bg)
        self.left_key = False
        self.right_key = False
        self.window.unbind('<Key>')

    def newSelection(self):
        '''
            callback function when combobox selection changes
        '''
        try:
            self.profiles[self.name_selection].color = self.color.getColor()
            self.current_color = self.color.getColor()
        except:
            pass

    def showInfoPlayer(self, e):
        '''
            resets informations about selected user
        '''
        self.selected = list(map(int, e.widget.curselection()))
        if self.selected:
            self.colors_list = self.color.getListAllColors()
            for profile in self.profiles:
                if self.profiles[profile].color not in self.colors_list:
                    self.colors_list.append(self.profiles[profile].color)
            selection = e.widget.get(self.selected[0])
            self.name_selection = selection
            if len(self.player_known.curselection()) > 0:
                left = self.profiles[self.name_selection].commands[0]
                self.button_left['text'] = left
                right = self.profiles[self.name_selection].commands[1]
                self.button_right['text'] = right
                self.color.set(self.profiles[self.name_selection].color)
                self.move_command_left = left
                self.move_command_right = right
            else:
                self.id = self.snakes_ingame.index(selection)
                left = self.profiles[selection].commands[0]
                self.button_left['text'] = left
                right = self.profiles[selection].commands[1]
                self.button_right['text'] = right
                self.color.set(self.profiles[selection].color)

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
            # move the correct player(s) when key is pressed
            self.inputs.press(key)

    def saveParameters(self):
        '''
            save paramers about players habit
        '''
        db = shelve.open(GUI.SAVE_FILE, flag='n')
        for profile in self.profiles:
            print('saving ' + profile)
            db[profile] = self.profiles[profile]
        db['(bg, fg)'] = (self.current_bg, self.current_fg)
        # db.sync()
        db.close()
        self.window.destroy()

    def loadSave(self):
        '''
            load the parameters saved about players habit
        '''
        try:
            db = shelve.open(GUI.SAVE_FILE, flag='r')
        except:
            showwarning('Load error', 'Unable to find a save file')
        else:
            if '(bg, fg)' in db:
                self.current_bg, self.current_fg = db['(bg, fg)']
                del db['(bg, fg)']
            else:
                self.current_bg, self.current_fg = 'white', 'black'
            for profile in db:
                self.profiles[profile] = db[profile]

if __name__ == '__main__':
    GUI()
