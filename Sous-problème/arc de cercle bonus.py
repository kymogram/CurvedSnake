from tkinter import *
from random import randint

class A:
	def __init__(self):
		self.fenetre = Tk()

		self.wcanva = 200
		self.canva = Canvas(self.fenetre,width=self.wcanva,height=self.wcanva,bg='black')
		self.canva.pack()

		self.gameSpeed = 30 # Nombre d'éxécution par secondes (=fps)
		self.maxval = 300 # Valeur maximal possible, en général nbd de frames
		self.val = 0 # Valeur de départ
		# Donc logiquement l'objet restera 10 secondes (maxval/gameSpeed)

		self.r = 16
		self.drawArc() # Initialise le dessin (le step se trouve dans le dessin)
		self.fenetre.mainloop()

	def drawArc(self):
		center = self.wcanva//2
		angle = 360-(self.val/self.maxval) * 360
		self.canva.delete(ALL)
		self.canva.create_arc(center-self.r,
							  center-self.r,
						  	  center+self.r,
						  	  center+self.r,
						  	  style=ARC,
						  	  extent=angle,
						  	  width=2,
						  	  outline='white')
		
		self.val += 1 # Diminuer le rayon
		self.fenetre.after(self.gameSpeed,self.drawArc) # refresh
A()