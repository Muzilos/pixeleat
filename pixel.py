import pygame
from random import randint
from consts import *

class Pixel:
    def __init__(self, x, y, radius, color, facing, win):
        self.coord = (x, y)
        self.radius = radius
        self.color = color
        self.facing = facing
        self.displacement = RADIUS
        self.win = win

    def draw(self):
        pygame.draw.circle(self.win, self.color.color, self.coord, self.radius)

    def move_forwards(self, x_max=WIDTH, y_max=HEIGHT):
        x, y = self.coord
        if x < x_max:
            x, y = x + self.displacement, y
        else:
            x, y = 0, y + self.displacement
        self.coord = (x, y)

    def move_backwards(self, x_max=WIDTH, y_max=HEIGHT):
        x, y = self.coord
        if x > 0:
            x, y = x - self.displacement, y
        else:
            x, y = WIDTH, y - self.displacement
        self.coord = (x, y)

    def mod_radius(self, modifier):
        self.radius = int(RADIUS * abs(modifier))

    def mod_displacement(self, modifier):
        self.displacement = int(RADIUS * abs(modifier))

class Color:
    def __init__(self, r=0, g=0, b=0, rgb=()):
        self.r = r
        self.g = g
        self.b = b
        if rgb:
            if len(rgb) >= 3:
                self.r, self.g, self.b = rgb[0:3] 
            else:
                raise Exception('RGB should have at least 3 values to unpack')
        self.color = [self.r, self.g, self.b]

    def randomize(self):
        for i in range(len(self.color)):
            primary_color = self.color[i]
            try:
                if primary_color >= 50:
                    primary_color = primary_color % randint(1, 255) 
                else: 
                    primary_color = randint((primary_color + 10) * 2, 255) - primary_color
            except ZeroDivisionError:
                primary_color = randint((primary_color + 10), 255) - primary_color
            self.color[i] = primary_color
        # print(self.color)

