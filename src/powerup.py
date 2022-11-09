import tkinter as tk
import math
from src.bullet import Bullet
import random
from shapely.geometry.polygon import Polygon
import itertools
from src.particle import Particle
import pygame


class Powerup:

    polygon = [(0, 0), (0, 6), (6, 6), (6, 0)]
    sP = None

    x = 0
    y = 0
    vX = 0
    vY = 0

    rot = 0
    rotV = 0

    obj = None

    pType = ""

    def __init__(self, canvas, color, pType, x, y, vX, vY, rot, rotV):
        self.pType = pType
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.rot = rot
        self.rotV = rotV

        # self.polygon = []

        self.sP = Polygon(self.polygon)
        self.obj = canvas.create_polygon(self.updatedPolygon(self.polygon),
                                         outline=color, width=2, fill="")
        # self.polygon = [(0, 0), (0, 10), (10, 10), (10, 0)]
        # figure out the physical shape of the asteroid

    def draw(self, canvas):
        canvas.coords(
            self.obj, *itertools.chain.from_iterable(self.updatedPolygon(self.polygon)))
        self.sP = Polygon(self.updatedPolygon(self.polygon))

        # canvas.create_polygon(self.updatedPolygon(self.polygon),
        #                       outline='white', width=2, fill="")
        # self.sP = Polygon(self.updatedPolygon(self.polygon))

    def updatedPolygon(self, poly):
        cosT = math.cos(self.rot)
        sinT = math.sin(self.rot)
        # https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
        return [
            (
                cosT*((x)-3)-sinT *
                ((y)-3)+self.x,

                sinT*((x)-3)+cosT *
                ((y)-3)+self.y
            ) for x, y in poly]

    def tick(self, engine):
        # print(self.x)
        self.readjustPosition(engine)
        self.move()
        self.draw(engine.canvas)

    def runPowerup(self, engine):
        pass

    def move(self):

        self.rot += self.rotV

        self.x -= min(self.vX, 0.25)
        self.y -= min(self.vY, 0.25)

    def readjustPosition(self, engine):
        if self.x > engine.width:
            self.x = 0
        elif self.x < 0:
            self.x = engine.width

        if self.y > engine.height:
            self.y = 0
        elif self.y < 0:
            self.y = engine.height
