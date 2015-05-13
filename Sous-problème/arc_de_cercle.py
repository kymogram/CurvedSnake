
from tkinter import *
from math import cos, sin

class Test:
	def __init__(self, x, y, dist, size, dep_angle, end_angle, step=0.05):
		fenetre = Tk()
		self.can = Canvas(fenetre, width= 300,height=200, bg='black')
		self.can.pack(padx=20, pady=20)
		
		self.drawArc(self.can, x, y, dist, size, dep_angle, end_angle, step)
		
		fenetre.mainloop()
	
	def drawArc(self, can, x, y, dist, size, dep_angle, end_angle, step):
		can.delete(ALL)
		print("refresh")
		
		#for i in range(dep_angle, end_angle, step):
		# marche pas car un for ne prend pas de floats
		preci_for = 20 # Attention a ne pas mettre trop bas, sinon le 3eme argument du for seras 0
		for i in range(int(dep_angle*preci_for), int(end_angle*preci_for), int(step*preci_for)):
			i /= preci_for
			can.create_line(x+dist*cos(i),
							y-dist*sin(i),
							x+dist*cos(i+step),
							y-dist*sin(i+step),
							w=size,
							fill='white')
			print(i,x+dist*cos(i))
		
		

	
	
Test(150, 100, 32, 2, 0, 3.1415)
