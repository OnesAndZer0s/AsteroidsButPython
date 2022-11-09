import tkinter as tk
import math


class NumberBoard:
    number = 0
    _oldNumber = None
    obj = None

    def __init__(self, canvas, x, y):
        self.x = x
        self.y = y
        self.obj = canvas.create_text(self.x, self.y, text=str(
            self.number), fill="white", anchor="nw")

    def draw(self, canvas):
        if self._oldNumber != self.number:
            canvas.itemconfig(self.obj, text=str(self.number))
            self._oldNumber = self.number

    def setNumber(self, n):
        self.number = n
