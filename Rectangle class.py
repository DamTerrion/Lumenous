from math import atan
from math import pi

class Rect(x1, y1, x2, y2, x3, y3, x4, y4):
    def __init__ (self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.point1 = {'x': x1, 'y': y1}
        self.point2 = {'x': x2, 'y': y2}
        self.point3 = {'x': x3, 'y': y3}
        self.point4 = {'x': x4, 'y': y4}
        self.point0 = {'x': (x1+x2+x3+x4)/4, 'y': (y1+y2+y3+y4)/4}
        self.point = (self.point0, self.point1, self.point2, self.point3, self.point4)
        self.angle1 = atan((y2-y1)/(x2-x1))
        self.angle2 = self.angle1+pi/2
