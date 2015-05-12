from tkinter import *
from random import randint, uniform
from math import cos, sin, pi

class Particles:
    DELAY = 30
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x, self.y = x, y
        #parameters
        NBR_PARTICLES_MIN = 30
        NBR_PARTICLES_MAX = 100
        SIZE_PARTICLES_MIN = 2
        SIZE_PARTICLES_MAX = 6
        SPEED_PARTICLES_MIN = 1.2
        SPEED_PARTICLES_MAX = 3
        LIFE_PARTICLES_MIN = 45
        LIFE_PARTICLES_MAX = 80

        nbr_particles = randint(NBR_PARTICLES_MIN, NBR_PARTICLES_MAX)
        if randint(1, 1000) == 666:
            nbr_particles = 500
        
        self.particles = [None] * nbr_particles
        self.particles_size = [randint(SIZE_PARTICLES_MIN, SIZE_PARTICLES_MAX) \
                                        for i in range(nbr_particles)]
        self.particles_direction = [uniform(0, 2*pi) \
                                        for i in range(nbr_particles)]
        self.particles_speed = [uniform(SPEED_PARTICLES_MIN, SPEED_PARTICLES_MAX) \
                                        for i in range(nbr_particles)]
        particles_life = [randint(LIFE_PARTICLES_MIN, LIFE_PARTICLES_MAX) \
                                        for i in range(nbr_particles)]
        self.particles_life_diminution = [self.particles_size[i] / particles_life[i] \
                                        for i in range(nbr_particles)] 
        #when particle's life < 1, it is destroyed
        for i in range(nbr_particles):
            w = self.particles_size[i]
            self.particles[i] = self.canvas.create_line(self.x, self.y-w//2,
                                     self.x, self.y+w//2, fill=color, width=w)
        self.refreshSystem()

    def refreshSystem(self):
        for index, particle in enumerate(self.particles):
            #change size according to life
            size_save = self.particles_size[index]
            self.particles_size[index] -= self.particles_life_diminution[index]
            #if size means 'dead'
            if self.particles_size[index] < 1:
                #remove it
                del self.particles[index]
                del self.particles_size[index]
                del self.particles_direction[index]
                del self.particles_speed[index]
                del self.particles_life_diminution[index]
                self.canvas.delete(particle)
            else:
                self.canvas.itemconfigure(particle,
                                          width=self.particles_size[index])
                #move the particle
                speed = self.particles_speed[index]
                x_offset = speed*cos(self.particles_direction[index])
                y_offset = -speed*sin(self.particles_direction[index])
                #get current coordinate
                pos = self.canvas.coords(particle)
                #update coord
                for i in range(len(pos)):
                    if i == 0 or i == 2: #X coordinate
                        pos[i] += x_offset
                    #y0
                    elif i == 1:
                        pos[i] += y_offset-(self.particles_size[index]-size_save)/2
                    #y1
                    else:
                        pos[i] += y_offset+(self.particles_size[index]-size_save)/2
                #apply offset
                self.canvas.coords(particle, tuple(pos))
        #loop
        if self.particles != []: 
            self.canvas.after(Particles.DELAY, self.refreshSystem)
    #
