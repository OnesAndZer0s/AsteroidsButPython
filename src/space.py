import random
import tkinter as tk
import math
from src.bullet import Bullet
from src.particle import Particle
import pygame

import itertools
from shapely.geometry.polygon import Polygon, Point


class Spaceship:
    scale = 1
    width = 15*scale
    indentHeight = 3*scale
    height = 20*scale
    pivotX = width/2
    pivotY = (2*height)/3
    thrustSpace = 5

    polygon = [(0, height), (width/2, height-indentHeight),
               (width, height), (width/2, 0)]
    thrustPolygon = [(width/4, (2*height-indentHeight)/2+thrustSpace),
                     (width/2, 1.5*height), ((3*width)/4, (2*height-indentHeight)/2+thrustSpace), (width/2,  height-indentHeight+thrustSpace)]
    thrust = False
    t = 0
    tOff = 15

    x = 0
    y = 0
    vX = 0
    vY = 0

    rot = 0
    rotV = 0

    speed = 0.006
    damp = 0.002
    maxSpeed = 0.75
    rotSpeed = 0.03

    projectiles = []
    spaceDown = False

    bSpeed = 1.5
    autofire = False
    bFreq = 25
    bTimer = 0

    thrustObj = None
    pObj = None

    dead = False
    lives = 2
    invincibilityTimer = 0

    deathParticles = []

    activePowerups = {
        "laser": False,
        "shield": False,
        "speed": False,
        "size": False
    }

    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.obj = canvas.create_polygon(self.updatedPolygon(self.polygon),
                                         outline='white', width=2, fill="")
        self.thrustObj = canvas.create_polygon(self.updatedPolygon(self.thrustPolygon),
                                               outline='white', width=2, fill="")
        self.pObj = Polygon(self.updatedPolygon(self.polygon))

    def draw(self, canvas):
        # self.trust = not self.thrust
        canvas.coords(
            self.obj, *itertools.chain.from_iterable(self.updatedPolygon(self.polygon)))
        if self.thrust and self.t and not self.dead:
            canvas.itemconfig(
                self.thrustObj, state=tk.NORMAL)
            canvas.coords(self.thrustObj, *itertools.chain.from_iterable(
                          self.updatedPolygon(self.thrustPolygon)))
        else:
            canvas.itemconfig(
                self.thrustObj, state=tk.HIDDEN)

        self.pObj = Polygon(self.updatedPolygon(self.polygon))

        if(self.invincibilityTimer > 0):
            col = abs(round(math.sin(self.invincibilityTimer/35)*235))
            canvas.itemconfig(self.obj, outline='#%02x%02x%02x' %
                              (col, col, col))
        else:
            canvas.itemconfig(self.obj, outline="white")

    def updatedPolygon(self, poly):
        cosT = math.cos(self.rot)
        sinT = math.sin(self.rot)
        # https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
        return [
            (
                cosT*((x)-self.pivotX)-sinT *
                ((y)-self.pivotY)+self.x,

                sinT*((x)-self.pivotX)+cosT *
                ((y)-self.pivotY)+self.y
            ) for x, y in poly]

    def astCollision(self, engine):
        for a in engine.asteroid:
            for proj in self.projectiles:
                if a.sP.contains(Point(proj.x, proj.y)):
                    for i in range(random.randrange(3, 6)):
                        newVX = random.random()*0.1-0.05
                        newVY = random.random()*0.1-0.05
                        engine.astPart.append(Particle(engine.astPart,
                                                       engine.canvas, [(0, 0)], proj.x, proj.y, newVX, newVY, 0, 0, 1))
                    a.kaboom(proj, engine)
                    proj.deleteSelf(engine)
                    engine.scoreboard.number += a.size*10
            if(not self.dead and self.invincibilityTimer == 0):
                if a.sP.intersects(self.pObj) == True:
                    self.dead = True
                    for i in range(random.randrange(3, 6)):
                        newVX = random.random()*0.1-0.05
                        newVY = random.random()*0.1-0.05
                        engine.astPart.append(Particle(engine.astPart,
                                                       engine.canvas, [(0, 0)], self.x, self.y, newVX, newVY, 0, 0, 1))
                    a.kaboom(self, engine)
                    self.preDeath(self, engine)

    def powerupCollision(self, engine):
        for a in engine.powerup:
            if self.pObj.contains(Point(a.x, a.y)):
                for i in range(random.randrange(3, 6)):
                    newVX = random.random()*0.1-0.05
                    newVY = random.random()*0.1-0.05
                    engine.astPart.append(Particle(engine.astPart,
                                                   engine.canvas, [(0, 0)], a.x, a.y, newVX, newVY, 0, 0, 1, engine.powerupColors[a.pType]))
                # a.kaboom(proj, engine)
                a.runPowerup(engine)
                engine.canvas.delete(a.obj)
                engine.powerup.pop(engine.powerup.index(a))
                engine.scoreboard.number += 100
        pass

    def tick(self, engine):
        self.keyprocess(engine.history, engine.canvas)
        self.readjustPosition(engine)
        self.move()
        self.astCollision(engine)
        self.powerupCollision(engine)
        self.draw(engine.canvas)
        for projectile in self.projectiles:
            projectile.tick(engine)

        if (self.invincibilityTimer > 0):
            self.invincibilityTimer -= 1

        for particle in self.deathParticles:
            particle.tick(engine)

    def keyprocess(self, key, canvas):
        if(not self.dead):
            if 25 in key:
                # rotation
                self.t += 1
                if (self.t > self.tOff):
                    self.thrust = not self.thrust
                    self.t = 0

                self.vX += (math.cos(self.rot+(math.pi/2))*self.speed)
                self.vY += (math.sin(self.rot+(math.pi/2))*self.speed)
            else:
                self.thrust = False
            # backwards
            # elif 39 in key:
            #     self.vX -= math.cos(self.rot+(math.pi/2))*self.speed
            #     self.vY -= math.sin(self.rot+(math.pi/2))*self.speed

            if 40 in key:
                self.rotV = self.rotSpeed
            elif 38 in key:
                self.rotV = -self.rotSpeed
            else:
                self.rotV = 0

            if 65 in key and (not self.spaceDown or self.autofire) and self.bTimer == 0:
                self.bTimer = self.bFreq
                pygame.mixer.music.load("./sounds/fire.wav")
                pygame.mixer.music.play()

                self.projectiles.append(
                    Bullet(canvas, self.x, self.y, self.rot, self.bSpeed))
                # self.vX -= math.cos(self.rot)*self.speed
                # self.vY -= math.sin(self.rot)*self.speed
            elif 65 in key:
                self.spaceDown = True
            else:
                self.spaceDown = False
            if self.bTimer > 0:
                self.bTimer -= 1

    def move(self):
        if(self.vX > self.maxSpeed):
            self.vX = self.maxSpeed
        elif(self.vX < -self.maxSpeed):
            self.vX = -self.maxSpeed

        if(self.vY > self.maxSpeed):
            self.vY = self.maxSpeed
        elif(self.vY < -self.maxSpeed):
            self.vY = -self.maxSpeed

        self.rot += self.rotV

        self.x -= self.vX
        self.y -= self.vY

        self.vX /= 1+self.damp
        self.vY /= 1+self.damp

    def readjustPosition(self, engine):
        if self.x > engine.width:
            self.x = 0
        elif self.x < 0:
            self.x = engine.width

        if self.y > engine.height:
            self.y = 0
        elif self.y < 0:
            self.y = engine.height

    def preDeath(self, ast, engine):
        engine.canvas.itemconfig(
            self.thrustObj, state=tk.HIDDEN)
        engine.canvas.itemconfig(
            self.obj, state=tk.HIDDEN)
        pygame.mixer.music.load("./sounds/bangLarge.wav")
        pygame.mixer.music.play()
        iterArr = self.polygon

        # iterArr = self.updatedPolygon(iterArr)

        for p in iterArr:
            ind = iterArr.index(p)
            if(ind+1 >= len(iterArr)):
                ind = -1
            newVX = ((-ast.vX/2+random.random()*2*self.vX)-self.vX) / \
                random.randrange(5, 10)
            newVY = ((-ast.vY/2+random.random()*2*self.vY)-self.vY) / \
                random.randrange(5, 10)
            rotV = ((random.random()*2*self.rotV)-self.rotV)

            self.deathParticles.append(Particle(self.deathParticles,
                                                engine.canvas, [(p[0], p[1]), (iterArr[ind+1][0], iterArr[ind+1][1])], self.x, self.y, newVX, newVY, self.rot, rotV, self.scale))

        engine.master.after(1000, self.postDeath, engine)

    def postDeath(self, engine):

        if(self.lives > 0):
            self.lives -= 1
            engine.canvas.itemconfig(
                self.thrustObj, state=tk.NORMAL)
            engine.canvas.itemconfig(
                self.obj, state=tk.NORMAL)
            self.x = engine.width/2
            self.y = engine.height/2
            self.rot = 0
            self.vX = 0
            self.vY = 0
            self.dead = False
            self.invincibilityTimer = 1000
        else:
            engine.gameOver()
