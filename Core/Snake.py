from tkinter import *
from math import cos, sin
from random import random, randint

from .Arc import Arc
from .Particles import Particles

DEFAULT_SPEED = 1.6
DEFAULT_THICKNESS = 6
DEFAULT_CHANCE_HOLE = 0.008
DEFAULT_MAX_HOLE_LENGTH = 18
DEFAULT_MIN_HOLE_LENGTH = 15
DEFAULT_ROTATION_ANGLE = 0.05  # rad

TURN_LEFT = 0
TURN_RIGHT = 1


class Snake:
    def __init__(self, parent, name, x_head, y_head, angle, color, is_artic=0,
                 hole_proba=DEFAULT_CHANCE_HOLE,
                 max_hole_length=DEFAULT_MAX_HOLE_LENGTH,
                 min_hole_length=DEFAULT_MIN_HOLE_LENGTH,
                 speed=DEFAULT_SPEED,
                 thickness=DEFAULT_THICKNESS):
        # list and not tuple because tuples can't be modified
        self.head_coord = [x_head, y_head]
        self.speed = speed
        # current angle in canvas
        self.angle = angle  # radians!
        # angle which is added (subtracted) when snake moves
        self.rotating_angle = DEFAULT_ROTATION_ANGLE
        self.canvas = parent.canvas
        # must be linked to GUI to handle bonuses
        self.parent = parent
        self.thickness = thickness
        self.color = 'white' if is_artic else color
        # when color is changed by bonus, original color must be kept somewhere
        self.color_unchanged = color
        self.artic = False
        self.is_artic = is_artic
        self.alive = True
        self.invincible = False
        self.in_time_before_start = True
        # boolean to be able to go throught the wall
        self.penetrate = False
        # used to tag items in canvas
        self.name = str(name)
        # number of frames still to come when snake produces a hole
        self.hole = 0
        # hole parameters
        self.hole_probability = hole_proba
        self.max_hole_length = max_hole_length
        self.min_hole_length = min_hole_length
        # for inversing commands bonus
        self.inversed_commands = False
        # for right angle bonus
        self.previous_angles = list()
        r = self.thickness//2
        # create head (which is moved through canvas and not recreated)
        tag = 'snake,{},-1'.format(self.name)
        self.head_id = self.canvas.create_oval(x_head-r, y_head-r,
                                               x_head+r, y_head+r,
                                               fill=self.color,
                                               outline=self.color,
                                               tag=tag)
        # bonus events to handle
        self.events_queue = list()
        # arcs created when a bonus is applied
        self.arcs = list()

    def addArc(self, bonus):
        '''
            creates a new arc around snake head
        '''
        self.arcs.append(Arc(self, bonus.length, len(self.arcs)))

    def isInScreen(self, x, y):
        '''
            returns True if (x, y) is on canvas and False otherwise.
        '''
        # needed for winfo_width and winfo_height
        self.canvas.update()
        # needed for map shrinking bonus
        border_depth = int(self.canvas['bd'])
        x_ok = border_depth <= x < self.canvas.winfo_width()-border_depth
        y_ok = border_depth <= y < self.canvas.winfo_height()-border_depth
        return x_ok and y_ok

    def handleCollision(self, step, collisions):
        '''
            do the appropriate action when collision appears on canvas.
            Kill the snake or set the bonus.
        '''
        # oldest element placed on canvas is at index 0
        first_elem = int(collisions[0])
        # get its tags (to see whether it is a snake or a bonus)
        tags = self.canvas.gettags(first_elem)
        # every item should have tags but test might still be useful...
        if len(tags) != 0:
            # tags are separated by ',' so split to get all info
            info = tags[0].split(',')
            if info[0] == 'snake':
                # if snake hits another snake or itself, it dies
                if info[1] != self.name or \
                   int(info[2]) < step-self.thickness*3:
                    self.alive = False
                if not self.alive:
                    # throw particles
                    x, y = self.head_coord
                    Particles(self.canvas, x, y, self.color)
            elif info[0] == 'bonus':
                # if snakes catches a bonus delete it from canvas
                # and ask GUI to handle it
                self.canvas.delete(first_elem)
                self.parent.handleBonus(self, info[1])

    def replaceInScreen(self):
        x, y = self.head_coord
        border_depth = int(self.canvas['bd'])
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if x < border_depth:
            x = canvas_width - border_depth
        elif x > canvas_width - border_depth:
            x = border_depth
        if y < border_depth:
            y = canvas_height - border_depth
        elif y > canvas_height - border_depth:
            y = border_depth
        self.head_coord = [x, y]

    def handleMove(self, step):
        '''
            moves the snake to the new (x, y) computed according
            to speed and direction.
        '''
        x, y = self.head_coord
        # if there is contact, snake is dead
        # WARNING: when the snake moves, it always touches its previous
        # position so step of appearance is written as a tag.
        if not self.isInScreen(x, y):
            if not self.penetrate:
                self.alive = False
                Particles(self.canvas, x, y, self.color)
            else:
                self.replaceInScreen()
        else:
            r = self.thickness // 2
            # find all items in contact with new position
            collisions = self.canvas.find_overlapping(x-r, y-r, x+r, y+r)
            if len(collisions) != 0 and collisions[0] == self.head_id:
                collisions = collisions[1:]
            # if there is something
            if len(collisions) != 0:
                self.handleCollision(step, collisions)

    def turn(self, side):
        if (side == TURN_LEFT and not self.inversed_commands) or \
           (side == TURN_RIGHT and self.inversed_commands):
            self.angle -= self.rotating_angle
        else:
            self.angle += self.rotating_angle

    def move(self, step):
        '''
            function when the snake is refreshed to make it move.
        '''
        self.checkSpecialColor(step)
        # stop moving if snake is dead
        if not self.alive:
            return
        # find new coordinates
        x, y = self.head_coord
        x += self.speed * cos(self.angle)
        y += self.speed * sin(self.angle)
        # update head_coord
        self.head_coord = [x, y]
        i = 0
        while i < len(self.arcs):
            self.arcs[i].setOffset(i)
            self.arcs[i].updateArc()
            if self.arcs[i].val == self.arcs[i].max:
                # delete arc # i
                self.canvas.delete(self.arcs[i].arc_id)
                self.arcs.pop(i)
                i -= 1
            i += 1
        # radius of oval
        r = self.thickness // 2
        if not self.invincible and not self.in_time_before_start:
            self.handleMove(step)
            if self.hole == 0:
                tag = 'snake,{},{}'.format(self.name, step)
                self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.color,
                                        outline=self.color, tag=tag)
                if random() < self.hole_probability:
                    self.hole = randint(self.min_hole_length,
                                        self.max_hole_length)
            else:
                self.hole -= 1
        self.canvas.coords(self.head_id, x-r, y-r, x+r, y+r)
        return self.alive

    def checkSpecialColor(self, step):
        if self.artic or self.is_artic:
            if step % 44 == 0:
                self.color = 'white' if self.color == '#00ffff' else \
                             '#0080ff' if self.color == 'white' else \
                             '#00ffff'
                self.updateHeadColor()

    def restoreAngle(self):
        self.rotating_angle = self.previous_angles.pop(0)

    def getName(self):
        return self.name

    def getColor(self):
        return self.color_unchanged

    def updateHeadColor(self):
        self.canvas.itemconfig(self.head_id, fill=self.color,
                               outline=self.color)
