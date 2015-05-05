from tkinter import *
from random import randint, uniform # randint pour flottants, entre 0 et 2π
from random import choice # A enlever
from math import cos, sin, pi

class Particule:
	def __init__(self, canva, x, y, color):
		self.GAMESPEED = 30
		self.canva = canva
		self.x = x 
		self.y = y
		self.startSystem(color)

	def startSystem(self, color):
		"""
		Initiation du systeme de particule.
		Puvait être placé dans le init, mais la fonction reset, n'aurai pas pu
		l'apeller.
		Remarque : 'PAR' est l'abréviation pour particule
		"""
		# Intervalles des différents paramètres
		MIN_PAR_NBR = 30
		MAX_PAR_NBR = 50
		MIN_PAR_SIZE = 2
		MAX_PAR_SIZE = 6
		MIN_PAR_SPEED = 1
		MAX_PAR_SPEED = 2.5
		MIN_PAR_LIFE = 15
		MAX_PAR_LIFE = 60

		par_nbr = randint(MIN_PAR_NBR,MAX_PAR_NBR)
		self.particules = [None]*par_nbr # Mieux que append car on sait la taille
		self.par_sizes = [randint(MIN_PAR_SIZE, MAX_PAR_SIZE) 
						  for i in range(par_nbr)] # taille de chaque particule
		self.par_directions = [uniform(0,2*pi) for i in range(par_nbr)]
		self.par_speeds = [uniform(MIN_PAR_SPEED,MAX_PAR_SPEED) for i in range(par_nbr)]
		# Constantes des vies pour chaque particule
		par_lifes = [randint(MIN_PAR_LIFE,MAX_PAR_LIFE) for i in range(par_nbr)]
		self.par_life_diminution = [self.par_sizes[i]/par_lifes[i] 
									for i in range(par_nbr)] 
		# Valeur de diminution de sa taille, correspondant à la durée de vie, car
		# quand la particule à une taille < à 1 elle est détruite.
		for i in range(par_nbr):
			w = self.par_sizes[i]
			# On dessinne une ligne car le width gére automatiquement l'épaisseur
			# A l'opposé d'un carré ou on aurai du modifier les coordonnées x
			particule = self.canva.create_line(self.x, self.y-w//2, self.x, self.y+w//2,
											   fill=color, stipple="gray50",
											   width = w)
			self.particules[i] = particule # id de notre particule sauvegardé:
		self.refreshSystem()


	def refreshSystem(self):
		for index, particule in enumerate(self.particules):
			# Gérer sa taille en fonction de sa vie
			size_save = self.par_sizes[index]
			self.par_sizes[index] -= self.par_life_diminution[index]
			if self.par_sizes[index] < 1:
				# Enlever dans les autres listes ces attributs associé
				del self.particules[index]
				del self.par_sizes[index]
				del self.par_directions[index]
				del self.par_speeds[index]
				del self.par_life_diminution[index]
				self.canva.delete(particule)
			else: # S'il est visible à l'écran:
				self.canva.itemconfigure(particule,width=self.par_sizes[index])

				# Déplacer la particule
				speed = self.par_speeds[index]
				direction = self.par_directions[index]
				x_offset = speed*cos(direction)
				y_offset = -speed*sin(direction)
				# Ne peux pas etre utiliser car la hauteur de la particule est géré par le y
#				self.canva.move(particule,x_offset,y_offset)

				pos = self.canva.coords(particule)
				for i in range(len(pos)):
					if i == 0 or i == 2: # Coordonnées x
						pos[i] += x_offset
					elif i == 1: # y0
						pos[i] += y_offset-(self.par_sizes[index]-size_save)/2
					else: 		 # y1
						pos[i] += y_offset+(self.par_sizes[index]-size_save)/2

				self.canva.coords(particule,tuple(pos))

		if self.particules != []: 
			# Plus de particules, donc on arette de boucler
			self.canva.after(self.GAMESPEED,self.refreshSystem)



class Test:
	def __init__(self):
		fenetre = Tk()
		w = 1000
		h = 700
		canva = Canvas(fenetre,bg='black',width=w,height=h)
		canva.pack()
		canva.create_text(w//2,16,text="<r> pour relancer",fill='white')
		self.col_list = ('white','yellow','cyan','red','green','orange')
		system1 = Particule(canva,w//4,h//4,choice(self.col_list))
		system2 = Particule(canva,3*w//4,3*h//4,choice(self.col_list))
		system3 = Particule(canva,3*w//4,h//4,choice(self.col_list))
		system4 = Particule(canva,w//4,3*h//4,choice(self.col_list))

		fenetre.bind("<r>",lambda e:self.reset(canva, system1, system2,system3,system4))
		fenetre.mainloop()

	def reset(self, canva, *systems):
		canva.delete('all')
		for system in systems:
			system.startSystem(choice(self.col_list))


Test()