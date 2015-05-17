from tkinter import IntVar

class Profile:
    def __init__(self, name, has_artic, commands, color):
        self.name = name
        self.artic_var = IntVar(value=0)
        self.has_artic = has_artic
        self.commands = commands
        self.color = color

    def getArticVar(self):
        return self.artic_var