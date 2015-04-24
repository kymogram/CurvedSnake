from tkinter import *

class A:
	def __init__(self):
		self.fenetre = Tk()
		self.fenetre['bg'] = 'black'
		l = [i for i in range(50)]

		listbox = Listbox(self.fenetre,
						  activestyle='underline',
						  bg='black',
						  fg='white',
						  selectbackground='gray20',
						  bd=5,
						  selectborderwidth=1,
						  borderwidth=3
						  )
		listbox.insert(0,*l)
		listbox.pack(padx=10,pady=10)

		self.fenetre.mainloop()


A()