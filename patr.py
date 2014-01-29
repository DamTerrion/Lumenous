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

def patr (line, size):
    if line.l < size and line.w < size :
        return (line)
        break
    stack1 = ()
    d = { 'c': size * line.cos, 's': size * line.sin }
    while line.l > size :
        new_line = Line (line.x + line.l*line.c - d['c']/2,
                         line.y + line.l*line.s - d['s'],
                         size, line.w, line.a, line.layer)
        line = Line (line.x - d['c']/2,
                     line.y - d['s'],
                     line.l - size, line.w, line.a, line.layer)
        stack1.append(new_line)
    stack1.append(line)
    stack3 = ()
    for s_line in stack1 :
        stack2 = ()
        while s_line.w > size :
            new_line = Line (s_line.x + s_line.w*s_line.s - d['s']/2,
                             s_line.y + s_line.w*_line.c - d['c'],
                             s_line.l, size, s_line.a, s_line.layer)
            s_line = Line (s_line.x - d['s']/2,
                           s_line.y - d['c']/2,
                           s_line.l,
                           s_line.w - size,
                           s_line.a, s_line.layer)
            stack2.append(new_line)
        stack2.append(s_line)
        for item in stack2 :
            stack3.append(item)
    return stack3
