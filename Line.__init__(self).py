from math import pi
from math import cos
from math import sin

class Line (object):
    def __init__ (self, x, y, lenght, width, angle, layer):
        self.x = x
        self.rx = round(x)
        self.y = y
        self.ry = round(y)
        self.l = lenght
        self.ls = str(lenght/1000)
        self.w = width
        self.ws = str(width/1000)
        self.a = angle
        self.rad = (angle * pi / 1800) % (2 * pi)
        self.layer = layer
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)
