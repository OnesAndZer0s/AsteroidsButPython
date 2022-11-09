import tkinter as tk
import math


class Bullet:
    x = 0
    y = 0
    vX = 0
    vY = 0
    obj = None

    def __init__(self, canvas, x, y, rot, bSpeed):
        self.x = x
        self.y = y
        self.vX = math.cos(rot+(math.pi/2))*bSpeed
        self.vY = math.sin(rot+(math.pi/2))*bSpeed
        self.obj = canvas.create_oval(self.x, self.y, self.x+2, self.y+2,
                                      fill='white', outline='white')

    def draw(self, canvas):
        canvas.coords(self.obj, *(self.x, self.y, self.x+2, self.y+2))

    def init():
        pass

    def tick(self, engine):
        self.move()
        self.readjustPosition(engine)
        self.draw(engine.canvas)

    def move(self):

        self.x -= self.vX
        self.y -= self.vY

    def readjustPosition(self, engine):
        if self.x > engine.width:
            self.deleteSelf(engine)
        elif self.x < 0:
            self.deleteSelf(engine)

        if self.y > engine.height:
            self.deleteSelf(engine)

        elif self.y < 0:
            self.deleteSelf(engine)

    def deleteSelf(self, engine):
        engine.space.projectiles.pop(engine.space.projectiles.index(self))
        engine.canvas.delete(self.obj)
