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

    def polyline (self):
        l = ( self.l * self.cos, self.l * self.sin )
        p1 = ( self.x - l[0], self.y - l[1] ) 
        p2 = ( self.x + l[0], self.y + l[1] )
        out = ( '  0\nPOLYLINE\n'+
                '  8\n'+self.layer+'\n'+
                ' 66\n1\n'+
                ' 40\n'+self.ws+'\n'+
                ' 41\n'+self.ws+'\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1[0]/1000)+'\n'+
                ' 20\n'+str(p1[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p2[0]/1000)+'\n'+
                ' 20\n'+str(p2[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nSEQEND\n'+
                '  8\n'+self.layer+'\n' )
        return { 'out':out,
                 '1':{'x':p1[0], 'y':p1[1]},
                 '2':{'x':p2[0], 'y':p2[1]},
                 'Error':False }
        
    def rectangle (self):
        l = ( self.l * self.cos, self.l * self.sin )
        w = ( self.w * self.sin, self.w * self.cos) 
        p1 = ( self.x - l[0] + w[0], self.y - l[1] + w[1] )
        p2 = ( self.x + l[0] + w[0], self.y + l[1] + w[1] )
        p3 = ( self.x + l[0] - w[0], self.y + l[1] - w[1] )
        p4 = ( self.x - l[0] - w[0], self.y - l[1] - w[1] )
        out = ( '  0\nPOLYLINE\n'+
                '  8\n'+self.layer+'\n'+
                ' 66\n1\n'+
                ' 40\n0.0\n'+
                ' 41\n0.0\n'+
                ' 70\n1\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1[0]/1000)+'\n'+
                ' 20\n'+str(p1[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p2[0]/1000)+'\n'+
                ' 20\n'+str(p2[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p3[0]/1000)+'\n'+
                ' 20\n'+str(p3[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p4[0]/1000)+'\n'+
                ' 20\n'+str(p4[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nSEQEND\n'+
                '  8\n'+self.layer+'\n' )
        return { 'out':out,
                 '1':{'x':p1[0], 'y':p1[1]},
                 '2':{'x':p2[0], 'y':p2[1]},
                 '3':{'x':p3[0], 'y':p3[1]},
                 '4':{'x':p4[0], 'y':p4[1]},
                 'Error':False }
        
    def solid (self):
        l = ( self.l * self.cos, self.l * self.sin )
        w = ( self.w * self.sin, self.w * self.cos ) 
        p1 = ( self.x - l[0] + w[0], self.y - l[1] + w[1] )
        p2 = ( self.x + l[0] + w[0], self.y + l[1] + w[1] )
        p3 = ( self.x - l[0] - w[0], self.y - l[1] - w[1] )
        p4 = ( self.x + l[0] - w[0], self.y + l[1] - w[1] )
        out = ( '  0\nSOLID\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1[0]/1000)+'\n'+
                ' 20\n'+str(p1[1]/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 11\n'+str(p2[0]/1000)+'\n'+
                ' 21\n'+str(p2[1]/1000)+'\n'+
                ' 31\n0.0\n'+
                ' 12\n'+str(p3[0]/1000)+'\n'+
                ' 22\n'+str(p3[1]/1000)+'\n'+
                ' 32\n0.0\n'+
                ' 13\n'+str(p4[0]/1000)+'\n'+
                ' 23\n'+str(p4[1]/1000)+'\n'+
                ' 33\n0.0\n' )
        return { 'out':out,
                 '1':{'x':p1[0], 'y':p1[1]},
                 '2':{'x':p2[0], 'y':p2[1]},
                 '3':{'x':p3[0], 'y':p3[1]},
                 '4':{'x':p4[0], 'y':p4[1]},
                 'Error':False }
