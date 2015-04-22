from tkinter import *

class Bonus:
    def __init__(self, path):
        self.name = path[path.rfind('/')+1:path.rfind('.')]
        self.image = PhotoImage(file=path)