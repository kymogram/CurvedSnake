from tkinter import *

class Bonus:
    def __init__(self, name, path, length):
        self.name = name
        self.image = PhotoImage(file=path)
        self.length = length
    
    #
