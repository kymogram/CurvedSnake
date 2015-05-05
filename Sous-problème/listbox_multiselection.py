from tkinter import *

class A:
	def __init__(self):
		fenetre = Tk()

		self.l = ['Louis','Gazelle Junior', 'Gazelle BG', 'Loan']

		w = Listbox(fenetre, activestyle='underline', 
					exportselection=0, selectmode=EXTENDED)
		w.pack(padx=10,pady=10)

		for item in self.l:
			w.insert(END, item)

		w.bind('<<ListboxSelect>>', self.changeText)

		self.fr = Label(fenetre,text='Yolo')
		self.fr.pack(padx=10) 

		fenetre.mainloop()

	def changeText(self,e):
		w = e.widget
		players = w.curselection()
		player_text = "Joueur : "
		print(w.get(selection_anchor()))
		premier = True
		for index in players:
			if not premier:
				player_text += ', '
			player_text += self.l[index]
			premier = False
		self.fr['text'] = player_text



A()