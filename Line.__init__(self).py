from math import pi
from math import cos
from math import sin

class Line (object):
    def __init__ (self, x, y, lenght, width, angle, layer):
        self.x = x
        self.xr = round(x)
        
        self.y = y
        self.yr = round(y)
        
        self.l = lenght
        self.lr = round(lenght)
        self.ls = str(lenght/1000)
        
        self.w = width
        self.wr = round(width)
        self.ws = str(width/1000)
        
        self.a = angle
        self.ar = round(angle)
        self.rad = (angle * pi / 1800) % (2 * pi)
        
        self.layer = str(layer)
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)
