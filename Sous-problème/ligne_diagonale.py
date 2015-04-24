from tkinter import *
from math import cos, sin, pi

class A:
	def __init__(self):
		self.fenetre = Tk()

		self.angle = IntVar()
		self.angle.set(90)

		self.r = 64 # Rayon dans lequel le carré est inscrit
		self.pos_dep = (128,128) # Position du centre du cercle
		self.pos_fin = (400,400)

		self.canva = Canvas(self.fenetre,bg='yellow',width=640,height=480)
		self.canva.pack()

		# Pour avoir une idée d'ou les traits iront
		self.canva.create_oval(self.pos_dep[0]-self.r//2,self.pos_dep[1]-self.r//2,self.pos_dep[0]+self.r//2,self.pos_dep[1]+self.r//2)
		self.canva.create_oval(self.pos_fin[0]-self.r//2,self.pos_fin[1]-self.r//2,self.pos_fin[0]+self.r//2,self.pos_fin[1]+self.r//2)
		
		self.canva.create_line(self.pos_dep,self.pos_fin,width=self.r)
		"""
		ang_rad = self.angle.get()*pi/180
		x1 = self.r*cos(ang_rad) + self.pos[0]
		y1 = self.r*sin(ang_rad) + self.pos[0]
		x2 = - self.r*cos(ang_rad) + self.pos[0]
		y2 = - self.r*sin(ang_rad) + self.pos[0]
		print((x1,y1,x2,y2))
		self.canva.create_polygon([x1,y1,x2,y2],fill='red')
		self.canva.create_polygon([100, 140, 140, 100, 100, 60, 60, 100],fill='red')
		self.canva.create_rectangle(0,0,128.0,118)
"""

		self.fenetre.mainloop()
A()