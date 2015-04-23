from tkinter import *
import tkinter as ttk

class A:
	def __init__(self):
		self.fenetre = Tk()

		self.colors = ['','Ab','CD','Autre']

		self.__colorVar = StringVar()  
		om = ttk.OptionMenu(self.fenetre, self.__colorVar, *self.colors)
		om.pack(padx=20,pady=20)
		self.__colorVar.set(self.colors[1])

		om.bind("<Configure>",lambda e:self.checkAutre(om))

		self.fenetre.mainloop()
	
	def checkAutre(self, widget):
		new_col = 'LouisMooh'
		self.colors.append(new_col)
		widget['menu'].add_command(label='wazi',command=self.__colorVar.set(new_col))

A()