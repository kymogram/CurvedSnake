from tkinter import *
from random import shuffle
from math import pi

ON_SELF, ON_OTHERS, ON_GUI = 0, 1, 2


class BonusManager:
    BONUS_FILES = ['self_speedup', 'self_speeddown',
                   'thickness_down', 'all_speeddown',
                   'reversed_commands', 'all_speedup',
                   'right_angles', 'thickness_up',
                   'rotation_angle_down', 'bonus_chance',
                   'change_color', 'change_chance_hole',
                   'clean_map', 'negative',
                   'invincible', 'shrink_map',
                   'self_right_angles', 'swap_position',
                   'portal', 'penetrating_wall',
                   'artic']

    EXEC_CODE = ['sender.speed += 1; sender.rotating_angle += 0.02; \
                  sender.addArc(self.gui.bonus_dict[bonus_ref])',
                 'if sender.speed > 1: sender.speed /= 1.5',
                 'sender.thickness /= 2',
                 'if snake.speed > 1: snake.speed /= 1.5',
                 'snake.inversed_commands = True',
                 'snake.speed += 1; snake.rotating_angle += 0.02',
                 'snake.previous_angles.append(snake.rotating_angle); \
                  snake.rotating_angle = pi/2',
                 'snake.thickness *= 2',
                 'snake.rotating_angle /= 1.5',
                 'pass  # gui',
                 'snake.color = sender.color; snake.updateHeadColor()',
                 'snake.hole_probability *= 10',
                 'pass  # gui',
                 'pass  # gui',
                 'sender.invincible = True',
                 'pass  # gui',
                 'sender.previous_angles.append(sender.rotating_angle); \
                  sender.rotating_angle = pi/2',
                 'pass  # gui',
                 'e = canvas.find_withtag("bonus,"+bonus_ref)[0]; \
                  sender.head_coord = canvas.coords(e); \
                  canvas.delete(e)',
                 'snake.penetrate = True',
                 'sender.artic = True; sender.color = "white"; \
                  sender.updateHeadColor()']

    TODO_CODE = ['snake.speed -= 1; snake.rotating_angle -= 0.02',
                 'snake.speed *= 1.5',
                 'snake.thickness *= 2',
                 'snake.speed *= 1.5',
                 'snake.inversed_commands = False',
                 'snake.speed -= 1; snake.rotating_angle -= 0.02',
                 'snake.restoreAngle()',
                 'snake.thickness /= 2',
                 'snake.rotating_angle *= 1.5',
                 '',
                 'snake.color = snake.color_unchanged; \
                  snake.updateHeadColor()',
                 'snake.hole_probability /= 10',
                 '',
                 '',
                 'snake.invincible = False',
                 '',
                 'snake.restoreAngle()',
                 '',
                 'pass',
                 'snake.penetrate = False',
                 'snake.artic = False; snake.color = snake.color_unchanged; \
                  snake.updateHeadColor()']

    ON_ACTION = [ON_SELF, ON_SELF,
                 ON_SELF, ON_OTHERS,
                 ON_OTHERS, ON_OTHERS,
                 ON_OTHERS, ON_OTHERS,
                 ON_OTHERS, ON_GUI,
                 ON_OTHERS, ON_OTHERS,
                 ON_GUI, ON_GUI,
                 ON_SELF, ON_GUI,
                 ON_SELF, ON_GUI,
                 ON_SELF, ON_SELF,
                 ON_SELF]

    MAX_PROBA = 0.16

    def __init__(self, parent):
        self.gui = parent
        # self.canvas = parent.canvas

    def listFrom(self, action, bonus):
        return [action, self.gui.bonus_dict[bonus].length]

    def invertColor(self, color):
        rgb = self.gui.canvas.winfo_rgb(color)
        return "#{:02x}{:02x}{:02x}".format(*[255 - c//256 for c in rgb])

    def handleBonus(self, sender, bonus_ref, bonus_proba):
        others = [snake for snake in self.gui.snakes_alive
                  if snake is not sender]
        add_event = lambda l, f: l.append(self.listFrom(f, bonus_ref))
        canvas = self.gui.canvas
        if bonus_ref == 'bonus_chance':
            # Precaution to not have bonus poping all around the map
            if bonus_proba <= BonusManager.MAX_PROBA:
                coeff = 2 if bonus_proba > BonusManager.MAX_PROBA/4 else 4
                action = 'self.bonus_proba /= ' + str(coeff)
                self.gui.bonus_proba *= coeff
                add_event(self.gui.events_queue, action)
        elif bonus_ref == 'clean_map':
            # save head coordinates
            heads = [snake.head_coord for snake in self.gui.snakes]
            bonus_dict = dict()
            for bonus in self.gui.bonus_dict:
                bonus_dict[bonus] = []
                for el in canvas.find_withtag('bonus,' + bonus):
                    bonus_dict[bonus].append(canvas.coords(el))
            canvas.delete(ALL)
            for i in range(len(heads)):
                x, y = heads[i]
                snake = self.gui.snakes[i]
                r = snake.thickness//2
                tag = 'snake,{},-1'.format(snake.name)
                snake.head_id = canvas.create_oval(x-r, y-r, x+r, y+r,
                                                   fill=snake.color, tag=tag,
                                                   outline=snake.color)
            for name in bonus_dict:
                for x, y in bonus_dict[name]:
                    tag = 'bonus,{}'.format(self.gui.bonus_dict[name].name)
                    canvas.create_image(x, y, tags=tag,
                                        image=self.gui.bonus_dict[name].image)
        elif bonus_ref == 'negative':
            canvas.configure(bg='white')
            add_event(self.gui.events_queue,
                      'self.canvas.configure(bg="black")')
            for snake in self.gui.snakes:
                snake.color = self.invertColor(snake.getColor())
                snake.updateHeadColor()
                add_event(snake.events_queue,
                          'snake.color = snake.color_unchanged; \
                           snake.updateHeadColor()')
        elif bonus_ref == 'shrink_map':
            self.gui.shrinkMap()
        elif bonus_ref == 'swap_position':
            if len(self.gui.snakes) > 1:
                head_angle_list = list()
                for snake in self.gui.snakes:
                    head_angle_list.append((snake.head_coord, snake.angle))
                    snake.invincible = True
                    add_event(snake.events_queue, 'snake.invincible = False')
                save = head_angle_list[:]
                # shuffle(head_angle_list)
                while head_angle_list == save:
                    shuffle(head_angle_list)
                for i in range(len(head_angle_list)):
                    self.gui.snakes[i].head_coord = head_angle_list[i][0]
                    self.gui.snakes[i].angle = head_angle_list[i][1]
        elif bonus_ref == 'penetrating_wall':
            self.gui.canvas_frame.configure(bg='blue')
            add_event(self.gui.events_queue,
                      'self.canvas_frame.configure(bg="grey")')
            for snake in self.gui.snakes:
                snake.penetrate = True

        bonus_name = bonus_ref if bonus_ref[:6] != 'portal' else 'portal'
        add_event = lambda l, f: l.append(self.listFrom(f, bonus_name))
        idx = BonusManager.BONUS_FILES.index(bonus_name)
        if self.ON_ACTION[idx] == ON_SELF:
            exec(self.EXEC_CODE[idx])
            add_event(sender.events_queue, self.TODO_CODE[idx])
        elif self.ON_ACTION[idx] == ON_OTHERS:
            for snake in others:
                exec(self.EXEC_CODE[idx])
                add_event(snake.events_queue, self.TODO_CODE[idx])
