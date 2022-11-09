import tkinter as tk
import math
import random

from src.bullet import Bullet
from shapely.geometry.polygon import Polygon
import itertools
from src.particle import Particle
from src.powerup import Powerup

import pygame


class Asteroid:
    size = 1

    polygon = None
    sP = None

    x = 0
    y = 0
    vX = 0
    vY = 0

    rot = 0
    rotV = 0

    obj = None

    def __init__(self, canvas, x, y, vX, vY, rot, rotV, size):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.rot = rot
        self.rotV = rotV
        self.size = size

        self.polygon = []

        vert = random.randint(4+(2*self.size), 6+(2*self.size))
        for i in range(0, vert):
            self.polygon.append((math.cos((i/vert)*2*math.pi)*self.size*10+random.randint(-self.size*3, self.size*3),
                                 math.sin((i/vert)*2*math.pi)*self.size*10+random.randint(-self.size*3, self.size*3)))

        self.sP = Polygon(self.polygon)
        self.obj = canvas.create_polygon(self.updatedPolygon(self.polygon),
                                         outline='white', width=2, fill="")
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
                cosT*((x)-(self.size/2))-sinT *
                ((y)-(self.size/2))+self.x,

                sinT*((x)-(self.size/2))+cosT *
                ((y)-(self.size/2))+self.y
            ) for x, y in poly]

    def tick(self, engine):
        # print(self.x)
        self.readjustPosition(engine)
        self.move()
        self.draw(engine.canvas)

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

    def kaboom(self, proj, engine):
        # delete itself from the engine
        engine.canvas.delete(self.obj)
        engine.asteroid.pop(engine.asteroid.index(self))
        # create two smaller asteroids
        if(self.size == 1):
            pygame.mixer.music.load("./sounds/bangSmall.wav")

        elif(self.size == 2):
            pygame.mixer.music.load("./sounds/bangMedium.wav")
        else:
            pygame.mixer.music.load("./sounds/bangLarge.wav")

        pygame.mixer.music.play()
        if self.size > 1:
            for i in range(0, 2):
                engine.asteroid.append(
                    Asteroid(engine.canvas,
                             self.x,
                             self.y,
                             self.vX/1.5+proj.vX/5+(random.random()-0.5)*0.5,
                             self.vY/1.5+proj.vY/5+(random.random()-0.5)*0.5,
                             self.rot,
                             self.rotV+(random.random()-0.01)*0.01,

                             self.size-1))
                pass

        # for p, c in engine.powerupChances.items():
        #     if random.random() <= c:
        #         print(p)
        #         engine.powerup.append(
        #             Powerup(engine.canvas, engine.powerupColors[p], p, self.x, self.y, self.vX+(random.randint(-10, 10)/50)+(proj.vX/random.randint(10, 20)), self.vY+(random.randint(-10, 10)/50)+(proj.vX/random.randint(10, 20)), self.rot*((random.random()*4)-2), self.rotV*((random.random()*4)-2)))
        #         # engine.powerup.append(p[0](engine.canvas, self.x, self.y))
        #         break
