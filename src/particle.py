import tkinter as tk
import math
from src.bullet import Bullet
import random
from shapely.geometry.polygon import Polygon
import itertools


class Particle:

    polygon = None

    x = 0
    y = 0
    vX = 0
    vY = 0

    rot = 0
    rotV = 0
    size = 0

    deathTimer = 0
    parent = None

    def __init__(self, parent, canvas, polygon, x, y, vX, vY, rot, rotV, size, color="white"):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.parent = parent
        self.polygon = polygon
        self.rot = rot
        self.rotV = rotV
        self.size = size
        self.deathTimer = random.randint(500, 1000)
        self.obj = canvas.create_polygon(self.updatedPolygon(self.polygon),
                                         outline=color, width=2, fill="")
        # self.polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
        # figure out the physical shape of the asteroid

    def draw(self, canvas):
        canvas.coords(
            self.obj, *itertools.chain.from_iterable(self.updatedPolygon(self.polygon)))

        # canvas.create_polygon(self.updatedPolygon(self.polygon),
        #                       outline='white', width=2, fill="")
        # self.sP = Polygon(self.updatedPolygon(self.polygon))

    def updatedPolygon(self, poly):
        cosT = math.cos(self.rot)
        sinT = math.sin(self.rot)
        # https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
        return [
            (
                cosT*((x)-(x/2))-sinT *
                ((y)-(self.size/2))+self.x,

                sinT*((x)-(self.size/2))+cosT *
                ((y)-(self.size/2))+self.y
            ) for x, y in poly]

    def tick(self, engine):
        # print(self.x)
        self.move()
        self.draw(engine.canvas)
        self.deathTimer -= 1
        if (self.deathTimer >= 0):
            self.deathTimer -= 1
        else:
            self.parent.remove(self)
            engine.canvas.delete(self.obj)

    def move(self):

        self.rot += self.rotV

        self.x -= min(self.vX, 0.25)
        self.y -= min(self.vY, 0.25)
