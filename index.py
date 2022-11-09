import tkinter as tk
import random
from src.space import Spaceship
from src.asteroid import Asteroid
from src.number import NumberBoard
import pygame


class Game(object):
    asteroid = list()
    space = None
    history = []
    liveGUI = []
    level = 0
    scoreboard = None
    astPart = []

    width = 500
    height = 500

    powerupChances = {
        "laser": 1,
        "shield": 1,
        "life": 1,
        "speed": 1,
        "size": 1
    }

    powerupColors = {
        "laser": "red",
        "shield": "blue",
        "life": "green",
        "speed": "yellow",
        "size": "orange"
    }
    powerup = []

    def __init__(self, **kwargs):
        self.master = tk.Tk()
        self.master.resizable(True, True)

        pygame.init()
        pygame.mixer.init()
        self.master.title("Asteroids")
        self.canvas = tk.Canvas(
            self.master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.master.bind("<Configure>", self.on_resize)

        self.height = self.canvas.winfo_reqheight()
        self.width = self.canvas.winfo_reqwidth()

        self.var = tk.StringVar()

        self.master.bind("<KeyPress>", self.keydown)
        self.master.bind("<KeyRelease>", self.keyup)

        self.space = Spaceship(self.canvas, self.width/2,
                               self.width/2)
        self.scoreboard = NumberBoard(self.canvas, 10, 10)

        self.draw()

        self.master.mainloop()

    def draw(self):
        self.scoreboard.draw(self.canvas)

        if len(self.asteroid) == 0 and not self.space.dead:
            self.level += 1
            for i in range(self.level):
                self.spawnLevelAsteroid()

        self.space.tick(self)

        for a in self.asteroid:
            a.tick(self)
        if not (len(self.liveGUI) == self.space.lives):
            while not (len(self.liveGUI) == self.space.lives):
                if len(self.liveGUI) < self.space.lives:
                    self.liveGUI.append(
                        self.canvas.create_polygon(*[(self.width+(len(self.liveGUI)+1)*-20+x, 10+y) for x, y in self.space.polygon], outline='white', width=2, fill=""))
                else:
                    self.canvas.delete(self.liveGUI.pop())

        for p in self.astPart:
            p.tick(self)

        for p in self.powerup:
            p.tick(self)

        self.master.after(5, self.draw)

    def on_resize(self, event):
        self.width = event.width-2
        self.height = event.height-2
        self.canvas.config(width=self.width, height=self.height)

        for a in self.liveGUI:
            self.canvas.delete(a)
        self.liveGUI = []

        if not (len(self.liveGUI) == self.space.lives):
            while not (len(self.liveGUI) == self.space.lives):
                if len(self.liveGUI) < self.space.lives:
                    self.liveGUI.append(
                        self.canvas.create_polygon(*[(self.width+(len(self.liveGUI)+1)*-20+x, 10+y) for x, y in self.space.polygon], outline='white', width=2, fill=""))
                else:
                    self.canvas.delete(self.liveGUI.pop())

        # rescale all the objects tagged with the "all" tag
        # self.canvas.scale("all", 0, 0, wscale, hscale)

    def keyup(self, e):
        # print e.keycode
        if e.keycode in self.history:
            self.history.pop(self.history.index(e.keycode))

            self.var.set(str(self.history))

    def keydown(self, e):
        if not e.keycode in self.history:
            self.history.append(e.keycode)
            self.var.set(str(self.history))

    def spawnAsteroid(self, x, y, vX, vY, rot, rotV, size):
        self.asteroid.append(
            Asteroid(self.canvas, x, y, vX, vY, rot, rotV, size))
        pass

    # spawns large asteroid on side and let fly in
    def spawnLevelAsteroid(self):
        r = random.randint(0, 3)
        sp = (random.random()+0.5)/5a
        rot = random.random()
        rotV = random.random()/500
        oR = ((random.random()+0.5)*2-2)/100
        if r == 0:  # left
            self.spawnAsteroid(-10, random.randint(0, self.width), sp,
                               oR, rot, rotV, 3)
        elif r == 1:  # right
            self.spawnAsteroid(self.width+10, random.randint(0, self.width), -sp,
                               oR, rot, rotV, 3)
        elif r == 2:  # top
            self.spawnAsteroid(random.randint(0, self.height), -10, oR,
                               sp, rot, rotV, 3)
        elif r == 3:  # bottom
            self.spawnAsteroid(random.randint(0, self.height), self.height+10, oR,
                               -sp, rot, rotV, 3)

    def gameOver(self):
        self.canvas.itemconfig(
            self.space.thrustObj, state=tk.HIDDEN)
        self.canvas.itemconfig(
            self.space.obj, state=tk.HIDDEN)
        self.canvas.create_text(
            self.width/2, self.height/2, text="You Died", fill="white", anchor=tk.CENTER)

    def clearAsteroids(self):
        print(len(self.asteroid))
        while len(self.asteroid) > 0:
            poi = self.asteroid.pop()
            self.canvas.delete(poi.obj)
        self.asteroid = list()


app = Game()
