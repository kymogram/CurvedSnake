from tkinter import *
from random import randint, uniform #randint pour flottants, entre 0 et 2π
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
        #Intervalles des différents paramètres
        MIN_PAR_NBR = 30
        MAX_PAR_NBR = 100
        MIN_PAR_SIZE = 2
        MAX_PAR_SIZE = 6
        MIN_PAR_SPEED = 1.2
        MAX_PAR_SPEED = 3
        MIN_PAR_LIFE = 45
        MAX_PAR_LIFE = 80

        par_nbr = randint(MIN_PAR_NBR,MAX_PAR_NBR)
        
        lucky = randint(1, 1000)
        if lucky == 666:
            par_nbr = 500
        self.particules = [None]*par_nbr #Mieux que append car on sait la taille
        self.par_sizes = [randint(MIN_PAR_SIZE, MAX_PAR_SIZE) 
                          for i in range(par_nbr)] #taille de chaque particule
        self.par_directions = [uniform(0,2*pi) for i in range(par_nbr)]
        self.par_speeds = \
                  [uniform(MIN_PAR_SPEED,MAX_PAR_SPEED) for i in range(par_nbr)]
        #Constantes des vies pour chaque particule
        par_lifes = [randint(MIN_PAR_LIFE,MAX_PAR_LIFE) for i in range(par_nbr)]
        self.par_life_diminution = [self.par_sizes[i]/par_lifes[i] 
                                    for i in range(par_nbr)] 
        #Valeur de diminution de sa taille, correspondant à la durée de vie, car
        #quand la particule à une taille < à 1 elle est détruite.
        for i in range(par_nbr):
            w = self.par_sizes[i]
            #On dessinne une ligne car le width gére automatiquement l'épaisseur
            #A l'opposé d'un carré ou on aurait du modifier les coordonnées x
            particule = self.canva.create_line(
                                        self.x, 
                                        self.y-w//2,
                                        self.x,
                                        self.y+w//2,
                                        fill=color,
                                        width = w
                                    )
            self.particules[i] = particule #id de notre particule sauvegardée:
        self.refreshSystem()

    def refreshSystem(self):
        for index, particule in enumerate(self.particules):
            #Gérer sa taille en fonction de sa vie
            size_save = self.par_sizes[index]
            self.par_sizes[index] -= self.par_life_diminution[index]
            if self.par_sizes[index] < 1:
                #Enlever dans les autres listes ces attributs associé
                del self.particules[index]
                del self.par_sizes[index]
                del self.par_directions[index]
                del self.par_speeds[index]
                del self.par_life_diminution[index]
                self.canva.delete(particule)
            else: #S'il est visible à l'écran:
                self.canva.itemconfigure(particule,width=self.par_sizes[index])
                #Déplacer la particule
                speed = self.par_speeds[index]
                direction = self.par_directions[index]
                x_offset = speed*cos(direction)
                y_offset = -speed*sin(direction)
                #Ne peux pas etre utiliser car la hauteur de la particule est
                #géré par le y

                pos = self.canva.coords(particule)
                for i in range(len(pos)):
                    if i == 0 or i == 2: #Coordonnées x
                        pos[i] += x_offset
                    elif i == 1: #y0
                        pos[i] += y_offset-(self.par_sizes[index]-size_save)/2
                    else:        #y1
                        pos[i] += y_offset+(self.par_sizes[index]-size_save)/2

                self.canva.coords(particule,tuple(pos))

        if self.particules != []: 
            #Plus de particules, donc on arette de boucler
            self.canva.after(self.GAMESPEED,self.refreshSystem)